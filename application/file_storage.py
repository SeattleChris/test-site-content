
from flask import current_app as app
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
    filename = f"{str(path)}/{name}"
    return path, filename


def delete_local_files(answer, path):
    """ Delete from the App Engine instance the locally saved copy now that we are done with it. """
    local_files = answer.get('file_list', [])
    deleted_files = []
    for filename in local_files:
        try:
            os.remove(filename)
            deleted_files.append(filename)
        except Exception as e:
            app.logger.info(f"=============== Error in delete_local_files: {filename} ===============")
            app.logger.error(e)
            app.logger.info("=============== Error in delete_local_files - End. ===============")
            raise e
    try:
        os.rmdir(path)
        deleted_files.append(path)
    except Exception as e:
        app.logger.info(f"=============== Error in delete_local_files: {path} ===============")
        app.logger.error(e)
        app.logger.info("=============== Error in delete_local_files - End. ===============")
        raise e
    answer['deleted'] = deleted_files
    return answer


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
    # app.logger.debug(f"File {source_file_name} uploaded to {destination_blob_name} . ")
    # TODO: Plan for return value if we wanted blob.make_private()
    return blob.public_url


def get_or_create_folder(folder_id, bucket=default_bucket):
    """ If folder does not exist, creates it. Returns a Blob object for this folder. """
    folder = f"posts/{str(folder_id)}"
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
    return blob


def move_captured_to_bucket(answer, path, id):
    """ The answer is a dictionary response from capture.py. The id is an integer directory to store blobs. """
    # answer = {'success': success, 'message': message, 'file_list': files, 'error_files': error_files}
    app.logger.debug('============================= Move Captured to Bucket ==============================')
    folder = get_or_create_folder(id)
    files = answer.get('file_list', [])
    app.logger.debug('------------ List of Files ------------')
    pprint(files)
    stored_urls = []
    for ea in files:
        _before, _orig, name = ea.partition(str(path) + '/')
        blobname = f"{folder}/{name}"
        blob_url = upload_blob(ea, blobname)
        stored_urls.append(blob_url)
    answer['url_list'] = stored_urls
    answer = delete_local_files(answer, path)
    return answer
