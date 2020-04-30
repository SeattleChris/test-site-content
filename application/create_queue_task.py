from flask import current_app as app
from google.api_core.exceptions import RetryError, AlreadyExists, GoogleAPICallError
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
from datetime import timedelta, datetime as dt

PROJECT_ID = app.config.get('PROJECT_ID')
PROJECT_REGION = app.config.get('PROJECT_REGION')
REPORT_SERVICE = app.config.get('REPORT_SERVICE')
REPORT_QUEUE = app.config.get('REPORT_QUEUE')
client = tasks_v2.CloudTasksClient()


def _get_report_queue(queue_name):
    """ Creates or gets a queue to process the outcome of capture queues processed by this application.
        May need to refactor to Create or Update a queue.
    """
    if not queue_name:
        queue_name = 'test'
    queue_name = f"{REPORT_QUEUE}-{queue_name}".lower()
    parent = client.location_path(PROJECT_ID, PROJECT_REGION)  # f"projects/{PROJECT_ID}/locations/{PROJECT_REGION}"
    queue_path = client.queue_path(PROJECT_ID, PROJECT_REGION, queue_name)
    routing_override = {'service': REPORT_SERVICE}
    rate_limits = {'max_concurrent_dispatches': 1, 'max_dispatches_per_second': 1}
    retry_config = {'max_attempts': 30, 'min_backoff': '1', 'max_backoff': '3600', 'max_doublings': 10}
    retry_config['max_retry_duration'] = '48h'
    queue_settings = {'name': queue_path, 'app_engine_routing_override': routing_override, 'rate_limits': rate_limits}
    queue_settings['retry_config'] = retry_config
    for queue in client.list_queues(parent):  # TODO: Improve efficiency since queues list is in lexicographical order
        if queue_settings['name'] == queue.name:
            # TODO: Fix q = client.update_queue(queue_settings, retry=capture_retry)
            return queue.name
    try:
        q = client.create_queue(parent, queue_settings)
    except AlreadyExists as exists:
        # TODO: return the existing queue.
        app.logger.debug(f"Already Exists on get/create/update {queue_name} ")
        app.logger.info(exists)
        q = None
    except ValueError as error:
        app.logger.debug(f"Value Error on get/create/update the {queue_name} ")
        app.logger.error(error)
        q = None
    except GoogleAPICallError as error:
        app.logger.debug(f"Google API Call Error on get/create/update {queue_name} ")
        app.logger.error(error)
        q = None
    return queue_path if q else None


def add_to_report(media_type, media_id, answer, queue_name='testing', task_name=None, in_seconds=90):
    """ Will add a task to a Capture Queue with a POST request if given a payload, else with GET request. """
    if not isinstance(task_name, (str, type(None))):
        raise TypeError("Usually the task_name for add_to_capture should be None, but should be a string if set. ")
    if not isinstance(media_type, str) or not isinstance(media_id, (int, str)):
        raise TypeError("At least one of the first two parameters in the add_to_report function where the wrong type. ")
    if not isinstance(answer, dict):
        raise TypeError("Expected a dictionary for the third parameter in add_to_report. ")
    payload = answer.copy()
    parent = _get_report_queue(queue_name)
    report_api_path = f"/capture/report/{str(media_id)}/"
    # report_api_path += f"?url={str(post.permalink)}"
    if len(answer['deleted']) == len(answer['file_list']) + 1:
        del payload['deleted']
    else:
        # TODO: determine which files have issues & handle them.
        pass
    if len(answer['error']) == 0:
        del payload['error']
    else:
        # TODO: determine which files have issues & handle them.
        pass
    if len(answer['file_list']) == len(answer['url_list']):
        del payload['file_list']
    else:
        # TODO: determine which files have issues & handle them.
        pass
    # payload now has key for 'success', 'message', and 'url_list'
    change_vals = {'media_id': str(media_id), 'media_type': media_type.lower()}
    change_vals['saved_media'] = payload.pop('url_list', [])
    payload['changes'] = [change_vals]
    http_method = 'POST' if payload else 'GET'
    task = {
            'app_engine_http_request': {  # Specify the type of request.
                'http_method': http_method,
                'relative_uri': report_api_path
            }
    }
    if payload is not None:
        task['app_engine_http_request']['body'] = payload.encode()  # Add payload to request as required type bytes.
    if task_name:
        task['name'] = task_name.lower()  # The Task API will generate one if it is not set.
    if in_seconds:
        # Convert "seconds from now" into an rfc3339 datetime string, format as timestamp protobuf, add to tasks.
        d = dt.utcnow() + timedelta(seconds=in_seconds)
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)
        task['schedule_time'] = timestamp
    try:
        response = client.create_task(parent, task)
    except ValueError as e:
        app.logger.debug(f"Invalid parameters for creating a task: \n {task}")
        app.logger.error(e)
        response = None
    except RetryError as e:
        app.logger.debug(f"Retry Attempts exhausted for a task: \n {task}")
        app.logger.error(e)
        response = None
    except GoogleAPICallError as e:
        app.logger.debug(f"Google API Call Error on creating a task: \n {task}")
        app.logger.error(e)
        response = None
    if response is not None:
        app.logger.debug(f"Created task: {response.name} ")
        app.logger.debug(response)
    return response  # .name if response else None
