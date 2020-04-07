
from flask import flash, current_app as app
from google.cloud import storage
from pprint import pprint

gcs = storage.Client()


def list_buckets():
    buckets = gcs.list_buckets()
    names = []
    for bucket in buckets:
        names.append(bucket.name)
        pprint(dir(bucket))

    # names = []
    # for bucket in buckets:
    #     temp = bucket.name
    #     app.logger.debug(temp)
    #     flash(temp)
    #     names.append(temp)
    # app.logger.debug('-------------')
    # app.logger.debug(names[0])
    # env_name = app.config.get('CLOUD_STORAGE_BUCKET')
    # app.logger.debug(env_name)
    # app.logger.debug(env_name == names[0])
    # found = gcs.get_bucket(app.config.get('CLOUD_STORAGE_BUCKET'))
    # app.logger.debug(found in buckets)
    return names


def list_blobs(bucket):
    """Lists all the blobs in a bucket. Input is is either a GCP bucket object, or a string of a bucket name. """
    bucket_name = bucket if isinstance(bucket, str) else bucket.name
    blobs = gcs.list_blobs(bucket_name)
    app.logger.info(f"========== List of blobs in {bucket_name} =========")
    # for blob in blobs:
    #     pprint(blob.name)
    return blobs


def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # Create a new blob for where to upload the file's content.
    bucket = gcs.get_bucket(app.config.get('CLOUD_STORAGE_BUCKET'))
    blob = bucket.blob(destination_blob_name)
    blob.make_public()  # blob.make_private()
    blob.upload_from_filename(source_file_name)  # blob.upload_from_file(source_file)
    app.logger.debug(f"File {source_file_name} uploaded to {destination_blob_name} . ")
    # TODO: Plan for return value if we wanted blob.make_private()
    return blob.public_url


def move_captured_to_bucket(answer, path, id):
    """ The answer dictionary is formatted as expected from capture.py. The blobname is the directory to store files. """
    # answer = {'success': success, 'message': message, 'file_list': files, 'error_files': error_files}
    try:
        blob_url = upload_blob()
    except Exception as e:
        app.logger.debug('------------- Move Captured to Bucket Exception ----------------------')
        pprint(e)
        app.logger.debug('------------- Move Captured to Bucket Exception End ------------------')
        raise e
    files = answer.get('file_list', [])
    app.logger.debug('=================== Move Captured to Bucket ========================')
    pprint(files)
    stored_urls = []
    for ea in files:
        _before, _orig, name = ea.partition(str(path) + '/')
        blobname = f"{str(id)}_{name}"
        blob_url = upload_blob(ea, blobname)
        stored_urls.append(blob_url)
    answer['url_list'] = stored_urls
    return answer
