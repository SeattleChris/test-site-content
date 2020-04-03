from os import environ
# from dotenv import load_dotenv
# load_dotenv()


# class Config:
#     """ Flask configuration variables """
SECRET_KEY = environ.get('SECRET_KEY')  # for session cookies & flash messages
FLASK_APP = environ.get('FLASK_APP')
FLASK_ENV = environ.get('FLASK_ENV')
PROJECT_NAME = environ.get('PROJECT_NAME')
PROJECT_ID = environ.get('PROJECT_ID')
PROJECT_NUMBER = environ.get('PROJECT_NUMBER')
PROJECT_REGION = environ.get('PROJECT_REGION')
PROJECT_ZONE = environ.get('PROJECT_ZONE')
PROJECT_CONNECTOR_NAME = environ.get('PROJECT_CONNECTOR_NAME')
INSTANCE_NAME = environ.get('INSTANCE_NAME')
INSTANCE_ID = environ.get('INSTANCE_ID')
SERVICE_ACCOUNT = environ.get('SERVICE_ACCOUNT')
DEV_RUN = True if environ.get('DEV_RUN') == 'True' else False
GAE_SERVICE = environ.get('GAE_SERVICE')
DEBUG = any([DEV_RUN, environ.get('DEBUG') == 'True', GAE_SERVICE in ('dev', 'capture', )])
DEPLOYED_URL = environ.get('DEPLOYED_URL', environ.get('URL', ''))
GAE_ENV = environ.get('GAE_ENV')  # Temporary
deploy_options = [environ.get('GAE_ENV') == 'flex',
                  environ.get('GAE_SERVICE') in ('capture', 'dev-capture'),
                  environ.get('COMPUTE_INSTANCE')
                  ]
if any(deploy_options):
    # PREFERRED_URL_SCHEME = 'https'
    URL = DEPLOYED_URL
    LOCAL_ENV = False
else:
    URL = 'http://0.0.0.0:8080'
    LOCAL_ENV = True
