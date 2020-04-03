from flask import request, render_template, jsonify, current_app as app
from .capture import capture
from .errors import InvalidUsage
# from flask import redirect, url_for, request, flash
import simplejson as json
import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(BASE_DIR, 'save')


@app.route('/')
def home():
    test = {'success': True, 'route': 'home'}
    app.logger.debug(json.dumps(test))
    app.logger.debug(request)
    result = 'This is the Home Page!'
    return render_template('base.html', result=result)


@app.route('/hello')
def hello():
    res = {'success': True, 'route': 'hello', 'answer': 'Hello World! '}
    res.update(app.config)
    app.logger.debug(json.dumps(res))
    app.logger.debug(BASE_DIR)
    return jsonify(res)


@app.route('/test')
def test():
    path = os.path.join(BASE_DIR, 'post')
    path = os.path.join(BASE_DIR, 'test')
    app.logger.debug(path)
    try:
        os.mkdir(path)
        filename = path + '/testfile'
    except FileExistsError as e:
        app.logger.debug(f"Error in test: Directory already exists at {path} ")
        app.logger.error(e)
        filename = path + '/testfile_double'
    except OSError as e:
        app.logger.debug(f"Error in test function creating dir {path}")
        app.logger.error(e)
        raise InvalidUsage('Route test OSError. ', status_code=501, payload=e)
    answer = capture(filename=filename)
    return render_template('base.html', result=answer)


@app.route('/call')
def call():
    test_ig = 'https://www.instagram.com/p/B4dQzq8gukI/'
    url = app.config.get('URL')
    id = 1
    media_type = 'faked'
    media_id = 1369
    api_url = f"{url}/api/v1/post/{str(id)}/{media_type}/{str(media_id)}/"
    payload = {'url': test_ig}
    res = requests.get(api_url, params=payload)
    app.logger.debug('---------- Our Call got back: --------------------------')
    app.logger.debug(res.json())
    return render_template('base.html', result=res.json())


@app.route('/api/v1/post/<int:id>/<string:media_type>/<int:media_id>/')
def api(id, media_type, media_id):
    """ Save content and associate with Post, which may be a story or regular Post. """
    # Passed as query string, we find it in request.args
    # Passed as form, we find in request.form.to_dict(flat=True)
    ig_url = request.args.get('url')
    app.logger.debug('========== the API was called! ==========')
    # make sure this is new post id, and make the id directory.
    path = os.path.join(BASE_DIR, 'post')
    path = os.path.join(path, str(id))
    try:
        os.mkdir(path)
        filename = f"{path}/{media_type}"
    except FileExistsError as e:
        app.logger.debug(f"Error in test: Directory already exists at {path} ")
        app.logger.error(e)
        filename = f"{path}/{media_type}_{media_id}"
    except OSError as e:
        app.logger.debug(f"Error in test function creating dir {path}")
        app.logger.error(e)
        raise InvalidUsage('Route test OSError. ', status_code=501, payload=e)
    app.logger.debug(filename)
    answer = capture(url=ig_url, filename=filename)
    app.logger.debug('---------- Capture gave us an answer ----------')
    app.logger.debug(answer)
    answer['url'] = path  # TODO: Update when saving to Bucket.
    app.logger.debug('------------ We can jsonify it --------------')
    app.logger.debug(jsonify(answer))
    return jsonify(answer)


# end of routes.py file
