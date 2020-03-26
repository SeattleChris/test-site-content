from flask import request, current_app as app
# from flask import render_template, redirect, url_for, request, flash  # , abort
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

# end of routes.py file
