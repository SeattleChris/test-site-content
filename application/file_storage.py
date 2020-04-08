
from flask import flash, current_app as app
from google.cloud import storage
from .errors import InvalidUsage
from pprint import pprint
import os

gcs = storage.Client()
default_bucket = gcs.get_bucket(app.config.get('CLOUD_STORAGE_BUCKET'))


def setup_local_storage(id, media_type, media_id):
    """ Create, or use existing, directory for temporarily storing the files on the server. """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, 'save', 'posts', str(id))
    name = media_type.lower()
    try:
        os.mkdir(path)
    except FileExistsError as e:
        app.logger.debug(f"Error in test: Directory already exists at {path} ")
        app.logger.error(e)
        name += f"_{str(media_id)}"
    except OSError as e:
        app.logger.debug(f"Error in test function creating dir {path} ")
        app.logger.error(e)
        raise InvalidUsage('Route test OSError. ', status_code=501, payload=e)
    return f"{str(path)}/{name}"


def list_buckets():
    buckets = gcs.list_buckets()
    names = []
    for bucket in buckets:
        names.append(bucket.name)
        pprint(dir(bucket))
    return names


def list_blobs(bucket):
    """Lists all the blobs in a bucket. Input is is either a GCP bucket object, or a string of a bucket name. """
    bucket = default_bucket if bucket is None else bucket
    bucket_name = bucket if isinstance(bucket, str) else bucket.name
    app.logger.info(f"========== got a list of blobs in {bucket_name} =========")
    blobs = gcs.list_blobs(bucket_name)
    return blobs


def upload_blob(source_file_name, destination_blob_name, bucket=default_bucket):
    """Uploads a file to the bucket by creating a blob and uploading the indicated file. """
    # Create a new blob for where to upload the file's content.
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)  # blob.upload_from_file(source_file)
    blob.make_public()  # blob.make_private()
    app.logger.debug(f"File {source_file_name} uploaded to {destination_blob_name} . ")
    # TODO: Plan for return value if we wanted blob.make_private()
    return blob.public_url


def get_or_create_folder(folder, bucket=default_bucket):
    """ If folder does not exist, creates it. Returns a Blob object for this folder. """
    folder = f"posts/{str(folder)}"
    # current_contents = list_blobs(bucket)
    # app.logger.debug('====================== get or create folder: list of contents =====================')
    # for ea in current_contents:
    #     pprint(ea)
    blob = None
    try:
        blob = bucket.get_blob(folder)
        if not blob:
            blob = bucket.blob(folder)
            blob.upload_from_string('')
            blob.make_public()
    except Exception as e:
        app.logger.debug('---------------------- get or create folder Exception ----------------------')
        pprint(e)
        app.logger.debug('---------------------- get or create folder Exception End ------------------')
        raise e
    app.logger.debug(f"********* blob folder is: {blob} *********")
    return blob


def move_captured_to_bucket(answer, path, id):
    """ The answer is a dictionary response from capture.py. The id is an integer directory to store blobs. """
    # answer = {'success': success, 'message': message, 'file_list': files, 'error_files': error_files}
    app.logger.debug('============================= Move Captured to Bucket ==============================')
    folder = get_or_create_folder(id)
    app.logger.debug('------------ List of Files ------------')
    files = answer.get('file_list', [])
    pprint(files)
    stored_urls = []
    for ea in files:
        _before, _orig, name = ea.partition(str(path) + '/')
        blobname = f"{folder}/{name}"
        blob_url = upload_blob(ea, blobname)
        stored_urls.append(blob_url)
    answer['url_list'] = stored_urls
    return answer
