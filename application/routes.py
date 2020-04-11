from flask import request, render_template, url_for, flash, jsonify, current_app as app
from .capture import capture
from .file_storage import setup_local_storage, move_captured_to_bucket, list_buckets, list_blobs
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


@app.route('/call')
def call():
    """ Route used for development testing the API response. """
    # test_ig = 'https://www.instagram.com/p/B4dQzq8gukI/'
    test_ig = 'https://www.instagram.com/stories/chip.reno/2283954400575747388/'
    # https://dev-dot-engaged-builder-257615.appspot.com/data/capture/1946
    url = app.config.get('URL')
    id = 6
    media_type = 'STORY'
    media_id = 1946
    api_url = f"{url}/api/v1/post/{str(id)}/{media_type}/{str(media_id)}/"
    payload = {'url': test_ig}
    app.logger.debug('========== Making a requests to our own API. ===========')
    app.logger.debug(api_url)
    app.logger.debug(payload)
    res = requests.get(api_url, params=payload)
    app.logger.debug('---------- Our Call got back a response. --------------------------')
    app.logger.debug(f"Status code: {res.status_code} ")
    # pprint(dir(res))
    pprint(res.json())
    return render_template('base.html', text=res.json().get('message', 'NO MESSAGE'), results=res.json(), links='dict')


@app.route('/api/v1/post/<int:id>/<string:media_type>/<int:media_id>/')
def api(id, media_type, media_id):
    """ Save content and associate with Post, which may be a story or regular Post. """
    # Passed as query string, we find it in request.args. Passed as form, we find in request.form.to_dict(flat=True)
    ig_url = request.args.get('url')
    app.logger.debug('========== the API was called! ==========')
    path, filename = setup_local_storage(id, media_type, media_id)
    answer = capture(ig_url, filename, media_type=media_type.upper())
    # answer = TEST_ANSWER
    # app.logger.debug('---------- Capture gave us an answer ----------')
    # pprint(answer)
    answer = move_captured_to_bucket(answer, path, id)
    app.logger.debug('---------- Move to Bucket gave us an answer ----------')
    pprint(answer)
    return jsonify(answer)


# end of routes.py file
