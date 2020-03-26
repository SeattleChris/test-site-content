from os import environ


# class Config:
#     """ Flask configuration variables """
SECRET_KEY = environ.get('SECRET_KEY')  # for session cookies & flash messages
FLASK_APP = environ.get('FLASK_APP')
FLASK_ENV = environ.get('FLASK_ENV')
DEBUG = environ.get('DEBUG') == 'True'
PROJECT_NAME = environ.get('PROJECT_NAME')
PROJECT_ID = environ.get('PROJECT_ID')
PROJECT_NUMBER = environ.get('PROJECT_NUMBER')
PROJECT_REGION = environ.get('PROJECT_REGION')
INSTANCE_NAME = environ.get('INSTANCE_NAME')
INSTANCE_ID = environ.get('INSTANCE_ID')
SERVICE_ACCOUNT = environ.get('SERVICE_ACCOUNT')
DEPLOYED_URL = environ.get('DEPLOYED_URL')
LOCAL_URL = 'http://127.0.0.1:8080'
PREFERRED_URL_SCHEME = 'https'
if environ.get('GAE_INSTANCE'):
    URL = DEPLOYED_URL
    LOCAL_ENV = False
else:
    environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    URL = LOCAL_URL
    LOCAL_ENV = True
