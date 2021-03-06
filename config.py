from os import environ
# from dotenv import load_dotenv
# load_dotenv()

# class Config:
#     """ Flask configuration variables """
SECRET_KEY = environ.get('SECRET_KEY')  # for session cookies & flash messages
FLASK_APP = environ.get('FLASK_APP')
FLASK_ENV = environ.get('FLASK_ENV')
# PROJECT_NAME = environ.get('PROJECT_NAME')
PROJECT_ID = environ.get('GOOGLE_CLOUD_PROJECT', environ.get('PROJECT_ID'))
# PROJECT_NUMBER = environ.get('PROJECT_NUMBER')
IG_EMAIL = environ.get('IG_EMAIL')
IG_PASSWORD = environ.get('IG_PASSWORD')
PROJECT_REGION = environ.get('PROJECT_REGION')
PROJECT_ZONE = environ.get('PROJECT_ZONE')
CLOUD_STORAGE_BUCKET = environ.get('CLOUD_STORAGE_BUCKET')
REPORT_SERVICE = environ.get('REPORT_SERVICE')
REPORT_QUEUE = environ.get('REPORT_QUEUE')
# PROJECT_CONNECTOR_NAME = environ.get('PROJECT_CONNECTOR_NAME')
# INSTANCE_NAME = environ.get('INSTANCE_NAME')
# INSTANCE_ID = environ.get('INSTANCE_ID')
# SERVICE_ACCOUNT = environ.get('SERVICE_ACCOUNT')
CHROME_VERSION = environ.get('CHROME_VERSION')
CHROMEDRIVER_VERSION = environ.get('CHROMEDRIVER_VERSION')
DEV_RUN = True if environ.get('DEV_RUN') == 'True' else False
GAE_SERVICE = environ.get('GAE_SERVICE')
DEBUG = any([DEV_RUN, environ.get('DEBUG') == 'True', GAE_SERVICE in ('dev', 'dev-capture', )])
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
    # URL = 'http://127.0.0.1:8080'
    URL = 'http://127.0.0.1:5000'
    LOCAL_ENV = True
GAE_DEPLOYMENT_ID = environ.get('GAE_DEPLOYMENT_ID')
GAE_INSTANCE = environ.get('GAE_INSTANCE')
GAE_MEMORY_MB = environ.get('GAE_MEMORY_MB')
GAE_RUNTIME = environ.get('GAE_RUNTIME')
GAE_VERSION = environ.get('GAE_VERSION')
