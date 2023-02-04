import os
import requests
import google
from google.cloud import storage

os.environ["PROJECT_ID"] = "dosepack-197416"
absolute_path = os.path.dirname(__file__)
relative_path = ("secret_keys")

cwd = os.getcwd()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join('{}/secret_keys'.format(cwd), 'dosepack-b325905c30d0.json')
storage_client = storage.Client()


def bucket_init(bucket_name):
    """
    Instantiate a google cloud storage bucket if exists else create a new bucket with provided name
    :param bucket_name: [str] The name of the bucket to be instantiated. (prefix with dosepack- for new bucket)
    :return:
    """
    bucket = storage_client.bucket(bucket_name)
    if bucket.exists():
        print("Bucket init success")
    else:

        try:
            bucket = storage_client.bucket(bucket_name)
            bucket.storage_class = "COLDLINE"
            bucket = storage_client.create_bucket(bucket, location="us-central1")
            print(
                "Created bucket {} in {} with storage class {}".format(
                    bucket.name, bucket.location, bucket.storage_class
                )
            )
        except google.cloud.exceptions.Conflict:
            print("Bucket already exists")

def download_to_filename_from_gcs(bucket_name, source_blob_name, destination_file_name, chunk_size=None):
    """
    Download the contents of this blob into a named file.
    :param bucket_name: [str] The name of the bucket to be instantiated.
    :param source_blob_name: [str] source blob name or gcs file name
    :param destination_file_name: [str] destination gcs file name
    :param chunk_size: [int] The size of a chunk of data whenever iterating
                        (in bytes). This must be a multiple of 256 KB
                        By default None
    :param timeout: [float] The amount of time, in seconds, to wait for the server response.
                    Can also be passed as a tuple (connect_timeout, read_timeout)
    :return:

    Example:
    download_to_filename_from_gcs("dosepack-dev", "crop_images/1000_12_4_4_18_7106_2020-08-18_23:52:30_t_1.jpg",
                                    "abc.jpg")

    """
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name, chunk_size=chunk_size)
    if blob.exists():
        try:
            blob.download_to_filename(destination_file_name)
            print(
                "Blob {} downloaded to {}.".format(
                    source_blob_name, destination_file_name
                )
            )
        except requests.exceptions.Timeout:
            print("Timeout occured while downloading file")
    else:
        print("File doesnot exists")


def get_file_path(bucket_name, created_date,n):
    bucket = storage_client.bucket(bucket_name)
    file_list = list(storage_client.list_blobs(bucket, prefix="pill_dropping_proxy_vbc/1_"))
    print(file_list)
    file_list = list(storage_client.list_blobs(bucket, prefix="pill_dropping_proxy_vbc/1_{}/{}".format(n , created_date)))
    print(file_list)
    for file in file_list:
        file_name = str(file)
        file_name = file_name[28:-19]
        if file_name.endswith("graph.zip"):
            print(file_name)
            return file_name
    return "None"