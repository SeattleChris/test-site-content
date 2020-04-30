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


@app.route('/api/v0/post/<int:id>/<string:media_type>/<int:media_id>/')
def api_0(id, media_type, media_id):
    """ Save content and associate with Post, which may be a story or regular Post. """
    # Passed as query string, we find it in request.args. Passed as form, we find in request.form.to_dict(flat=True)
    ig_url = request.args.get('url')
    app.logger.debug('========== the API was called! ==========')
    path, filename = setup_local_storage(media_type, media_id, id=id)
    answer = capture(ig_url, filename, media_type=media_type.upper())
    # answer = TEST_ANSWER
    # app.logger.debug('---------- Capture gave us an answer ----------')
    # pprint(answer)
    answer = move_captured_to_bucket(answer, path, id=id)
    app.logger.debug('---------- Move to Bucket gave us an answer ----------')
    pprint(answer)
    return jsonify(answer)


@app.route('/api/v1/post/<string:media_type>/<int:media_id>/')
def api(media_type, media_id):
    """ Save content and associate with Post, which may be a story or regular Post. """
    # Passed as query string, we find it in request.args. Passed as form, we find in request.form.to_dict(flat=True)
    # Passed as POST we find the payload in the body.
    ig_url = request.args.get('url')
    app.logger.debug('========== the API was called! ==========')
    path, filename = setup_local_storage(media_type, media_id)
    answer = capture(ig_url, filename, media_type=media_type.upper())
    # app.logger.debug('---------- Capture gave us an answer ----------')
    # pprint(answer)
    answer = move_captured_to_bucket(answer, path)
    app.logger.debug('---------- Move to Bucket gave us an answer ----------')
    pprint(answer)
    # Process the answer to send the needed work to a Task Queue.
    response = add_to_report(media_type, media_id, answer)
    if response is None:
        message = f"Unable to add results to a report queue for media_id: {media_id} "
        app.logger.debug(message)
        return message, 500
    app.logger.debug(f"Created task: {response.name} ")
    app.logger.debug(response)
    return jsonify(answer)

# end of routes.py file
