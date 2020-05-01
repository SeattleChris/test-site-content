from flask import request, render_template, url_for, flash, jsonify, current_app as app
from .capture import capture
from .file_storage import setup_local_storage, move_captured_to_bucket, list_buckets, list_blobs
from .create_queue_task import add_to_report
from .errors import InvalidUsage
import simplejson as json
import requests
from pprint import pprint

TEST_ANSWER = {'success': True,
               'message': 'Files Saved! ',
               'file_list': ['/home/chris/newcode/test-site-content/save/post/1/faked_full.png',
                             '/home/chris/newcode/test-site-content/save/post/1/faked_1.png',
                             '/home/chris/newcode/test-site-content/save/post/1/faked_2.png',
                             '/home/chris/newcode/test-site-content/save/post/1/faked_3.png'
                             ],
               'error_files': []
               }


@app.route('/')
def home():
    test = {'success': True, 'route': 'home'}
    app.logger.debug(json.dumps(test))
    app.logger.debug(request)
    message = 'This is the Home Page!'
    flash("Loaded Home Page. ")
    app.logger.debug('=============================== Home Route ===============================')
    return render_template('base.html', text=message, results=None, links=False)


@app.route('/bucket_list')
def bucket_list():
    bucket_names = list_buckets()
    buckets = [(name, url_for('blob_list', bucket_name=name)) for name in bucket_names]
    return render_template('base.html', text="Bucket List", results=buckets, links=True)


@app.route('/blob_list/<string:bucket_name>')
def blob_list(bucket_name):
    bucket_name = app.config.get('CLOUD_STORAGE_BUCKET') if bucket_name == 'default' else bucket_name
    blobs = list_blobs(bucket_name)
    results = [(blob.name, blob.public_url) for blob in blobs]
    return render_template('base.html', text="Blob List", results=results, links=True)


@app.route('/hello')
def hello():
    res = {'success': True, 'route': 'hello', 'answer': 'Hello World! '}
    res.update(app.config)
    removed_val = res.pop('PERMANENT_SESSION_LIFETIME', 'NOT FOUND')
    app.logger.debug(f"PERMANENT_SESSION_LIFETIME: {removed_val} ")
    removed_val = res.pop('SEND_FILE_MAX_AGE_DEFAULT', 'NOT FOUND')
    app.logger.debug(f"SEND_FILE_MAX_AGE_DEFAULT: {removed_val} ")
    app.logger.debug(json.dumps(res))
    return jsonify(res)


@app.route('/call/<string:media_type>/')
def call(media_type):
    """ Route used for development testing the API response. """
    default_ig_url = 'https://www.instagram.com/p/B4dQzq8gukI/'
    story_url = 'https://www.instagram.com/stories/noellereno/2284310497111265707/'
    default_url = story_url if media_type.upper() == 'STORY' else default_ig_url
    ig_url = request.args.get('url', default_url)
    app.logger.debug(f"Testing media type {media_type} call with IG url: ")
    app.logger.debug(ig_url)
    url = app.config.get('URL')
    id = 7
    media_id = 1946
    api_url = f"{url}/api/v1/post/{str(id)}/{media_type}/{str(media_id)}/"
    payload = {'url': ig_url}
    app.logger.debug('========== Making a requests to our own API. ===========')
    app.logger.debug(api_url)
    app.logger.debug(payload)
    res = requests.get(api_url, params=payload)
    app.logger.debug('---------- Our Call got back a response. --------------------------')
    app.logger.debug(f"Status code: {res.status_code} ")
    if res.status_code == 500:
        raise InvalidUsage('The test call got a 500 status code. ', payload=res)
    pprint(res.json())
    return render_template('base.html', text=res.json().get('message', 'NO MESSAGE'), results=res.json(), links='dict')


@app.route('/api/v1/post/<int:id>/<string:media_type>/<int:media_id>/')
def api_0(id, media_type, media_id):
    """ Save content and associate with Post, which may be a story or regular Post. """
    mod = 'post'
    # Passed as query string, we find it in request.args. Passed as form, we find in request.form.to_dict(flat=True)
    ig_url = request.args.get('url')
    app.logger.debug('========== the API ver. 0 was called! ==========')
    path, filename = setup_local_storage(mod, media_type, media_id, id=id)
    answer = capture(ig_url, filename, media_type=media_type.upper())
    # answer = TEST_ANSWER
    # app.logger.debug('---------- Capture gave us an answer ----------')
    # pprint(answer)
    answer = move_captured_to_bucket(answer, path, id=id)
    app.logger.debug('---------- Move to Bucket gave us an answer ----------')
    pprint(answer)
    return jsonify(answer)


@app.route('/api/v1/<string:mod>/', methods=['GET', 'POST'])
def api(mod):
    """ Save content and associate with Post, which may be a story or regular Post. """
    if mod != 'post':
        return "Unknown Data Type in Request", 404
    # The query string is in request.args, a form is in request.form.to_dict(flat=True), body is request.to_json()
    app.logger.debug('========== the API v1 was called! ==========')
    args = request.args
    req_body = request.json if request.is_json else request.data
    head = {}
    head['x_queue_name'] = request.headers.get('X-AppEngine-QueueName', None)
    head['x_task_id'] = request.headers.get('X-CloudTasks-TaskName', None)
    head['x_retry_count'] = request.headers.get('X-CloudTasks-TaskRetryCount', None)
    head['x_response_count'] = request.headers.get('X-AppEngine-TaskExecutionCount', None)
    head['x_task_eta'] = request.headers.get('X-AppEngine-TaskETA', None)
    head['x_task_previous_response'] = request.headers.get('X-AppEngine-TaskPreviousResponse', None)
    head['x_task_retry_reason'] = request.headers.get('X-AppEngine-TaskRetryReason', None)
    head['x_fail_fast'] = request.headers.get('X-AppEngine-FailFast', None)
    pprint(args)
    pprint(req_body)
    app.logger.debug('-----------------------------------------')
    # report_settings = {'service': environ.get('GAE_SERVICE', 'dev'), 'relative_uri': '/capture/report/'}
    # source = {'queue_type': queue_name, 'queue_name': parent, 'object_type': mod}
    # data = {'target_url': post.permalink, 'media_type': post.media_type, 'media_id': post.media_id}
    # req_body = {'report_settings': report_back, 'source': source, 'dataset': [data]}
    report_settings = req_body.get('report_settings', {})
    dataset = req_body.get('dataset', [])
    source = req_body.get('source', {})
    source.update(head)
    pprint(source)
    app.logger.debug('-----------------------------------------')
    results, had_error = [], False
    for data in dataset:
        media_type = data.get('media_type', '')
        media_id = data.get('media_id')
        payload = process_one(mod, media_type, media_id, data.get('target_url', ''))
        payload['source'] = source
        response = add_to_report(payload, report_settings)
        if response is None:
            had_error = True
            message = f"Unable to add results to a report queue for {mod} data with media_id {media_id} "
            app.logger.debug(message)
            pprint(payload)
            response = {'error': message, 'status_code': 500}
        else:
            app.logger.debug(f"Created task: {response.name} ")
            pprint(response)
        results.append(response)
    status_code = 500 if had_error else 201
    return jsonify(results), status_code


def process_one(mod, media_type, media_id, ig_url):
    """ Executes all the steps to process a request for one capture page. """
    path, filename = setup_local_storage(mod, media_type, media_id)
    answer = capture(ig_url, filename, media_type=media_type.upper())
    answer = move_captured_to_bucket(answer, path)
    app.logger.debug('---------- Answer after Setup, Capture, AND Move to Bucket ----------')
    pprint(answer)
    return prepare_payload_from_answer(media_type, media_id, answer)


def prepare_payload_from_answer(media_type, media_id, answer):
    """ Used to manage odd outcomes during our setup_local_storage, capture, and move_capture_to_bucket stages """
    if len(answer['deleted']) == len(answer['file_list']) + 1:
        del answer['deleted']
    else:
        # TODO: determine which files have issues & handle them.
        pass
    if len(answer['error']) == 0:
        del answer['error']
    else:
        # TODO: determine which files have issues & handle them.
        pass
    if len(answer['file_list']) == len(answer['url_list']):
        del answer['file_list']
    else:
        # TODO: determine which files have issues & handle them.
        pass
    # If all went well: answer now has key for 'success', 'message', and 'url_list'
    payload = {'success': answer.pop('success', False), 'message': answer.pop('message', '')}
    change_vals = {'media_type': media_type.lower(), 'media_id': str(media_id)}
    change_vals['saved_media'] = answer.pop('url_list', [])
    payload['changes'] = [change_vals]
    if answer:
        payload['error'] = answer
    app.logger.debug('============== Payload built from Answer =================')
    pprint(payload)
    return payload

# end of routes.py file
