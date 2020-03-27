from flask import request, render_template, current_app as app
from .capture import capture
# from flask import redirect, url_for, request, flash
import simplejson as json


@app.route('/')
def home():

    test = {'success': True, 'route': 'home'}
    app.logger.debug(json.dumps(test))
    app.logger.debug(request)
    return 'This is the Home Page!'


@app.route('/hello')
def hello():
    return 'Hello World!'


@app.route('/test')
def test():
    answer = capture()
    return render_template('base.html', result=answer)


# end of routes.py file
