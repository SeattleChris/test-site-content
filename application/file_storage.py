
from flask import current_app as app
from google.cloud import storage
from .errors import InvalidUsage
from pprint import pprint
import os
import time

gcs = storage.Client()
default_bucket = gcs.get_bucket(app.config.get('CLOUD_STORAGE_BUCKET'))


def setup_local_storage(mod, media_type, media_id, id=None):
    """ Create, or use existing, directory for temporarily storing the files on the server. """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if mod == 'post':
        mod = 'posts'
    path = os.path.join(BASE_DIR, 'save', mod, str(media_id))
    if id:
        path = os.path.join(BASE_DIR, 'save', mod, str(id))
    name = media_type.lower()
    try:
        os.mkdir(path)
    except FileExistsError as e:
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        name += f"_{timestamp}"
    except OSError as e:
        raise InvalidUsage("OSError in setup_local_storage. ", status_code=501, payload=e)
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
    """ List all buckets this app has access and awareness about. """
    buckets = gcs.list_buckets()
    names = []
    for bucket in buckets:
        names.append(bucket.name)
    return names


def list_blobs(bucket):
    """ Lists all the blobs in a bucket. Input is is either a GCP bucket object, or a string of a bucket name. """
    bucket = default_bucket if bucket is None else bucket
    bucket_name = bucket if isinstance(bucket, str) else bucket.name
    blobs = gcs.list_blobs(bucket_name)
    return blobs


def upload_blob(source_file_name, destination_blob_name, bucket=default_bucket):
    """ Uploads a file to the bucket by creating a blob and uploading the indicated file. """
    # TODO: Save time compared to the following code of Blob name check?
    if bucket.get_blob(destination_blob_name):
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        blob_name, seperator, file_ext = destination_blob_name.rpartition('.')
        destination_blob_name = f"{blob_name}_{timestamp}{seperator}{file_ext}"
    # Create a new blob for where to upload the file's content.
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)  # blob.upload_from_file(source_file)
    blob.make_public()  # blob.make_private()
    # app.logger.debug(f"File {source_file_name} uploaded to {destination_blob_name} . ")
    # TODO: Plan for return value if we wanted blob.make_private()
    return blob.public_url


def summary_blob(url_list, destination_blob_folder, bucket=default_bucket):
    """ Deprecated. This is no longer required for our API response.
        Creates, or updates, a blob to hold a list of all the files in this blob directory.
    """
    destination_blob_name = destination_blob_folder + '/summary.txt'
    blob = bucket.get_blob(destination_blob_name)
    if blob:
        # read current data, then add data.
        original = blob.download_as_string().decode()
        app.logger.debug('----------- Found existing summary blob ----------')
        pprint(original)
        blob.upload_from_string(str(original) + '\n' + '\n'.join(url_list))
    else:
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string('\n'.join(url_list))
    blob.make_public()
    return blob.public_url


def get_or_create_blob_folder(folder_id, bucket=default_bucket):
    """ Deprecated. Does not seem needed for making and using folders or sub-folders.
        If Storage bucket folder does not exist, creates it. Returns a Blob object for this folder.
    """
    folder = f"posts/{str(folder_id)}"
    blob = None
    try:
        blob = bucket.get_blob(folder)
        if not blob:
            blob = bucket.blob(folder)
    except Exception as e:
        app.logger.debug('---------------------- get or create folder Exception ----------------------')
        pprint(e)
        app.logger.debug('---------------------- get or create folder Exception End ------------------')
        raise e
    return blob


def move_captured_to_bucket(answer, path, folder_id=None):
    """ The answer is a dictionary response from capture.py. The folder_id is an integer directory to store blobs. """
    # answer = {'success': True|False, 'message': 'some text. ', 'file_list': [], 'error_files': []}
    # Below will add answer['url_list'] and answer['deleted] which are both lists.
    folder_name = f"posts/{str(folder_id)}"
    files = answer.get('file_list', [])
    stored_urls = []
    for ea in files:
        _before, _orig, name = ea.partition(str(path) + '/')
        blobname = f"{folder_name}/{name}"
        blob_url = upload_blob(ea, blobname)
        stored_urls.append(blob_url)
    answer['url_list'] = stored_urls
    # answer['url'] = summary_blob(stored_urls, folder_name)
    answer = delete_local_files(answer, path)
    return answer
