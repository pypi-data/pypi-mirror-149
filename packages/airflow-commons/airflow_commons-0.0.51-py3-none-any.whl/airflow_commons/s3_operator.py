import boto3
import botocore
import time
from datetime import datetime
import pyarrow as pa
import pyarrow.parquet as pq
from s3transfer import S3UploadFailedError
from s3fs import S3FileSystem
from airflow_commons.logger import LOGGER

DEFAULT_RETRY_COUNT = 3


def get_param(key, region_name: str = "eu-west-1"):
    ssm = boto3.client("ssm", region_name=region_name)
    parameter = ssm.get_parameter(Name=key, WithDecryption=True)
    return parameter["Parameter"]["Value"]


def upload_file_to_s3_bucket(path_to_file: str, bucket_name: str, file_name: str):
    """
    Uploads the given file to the given s3 bucket.

    :param path_to_file: Path to file that will be uploaded to s3 bucket.
    :param bucket_name: Name of the bucket that file will be uploaded to.
    :param file_name: Name of the file (key of the file in s3).
    """
    LOGGER.info(f"Upload to {bucket_name} started")
    upload_start = datetime.now()
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(path_to_file, bucket_name, file_name)
    except S3UploadFailedError as e:
        LOGGER.error(f"Upload to {bucket_name} failed")
        raise e
    upload_end = datetime.now()
    LOGGER.info(
        "Upload finished in {duration} seconds".format(
            duration=round((upload_end - upload_start).total_seconds())
        )
    )


def write_into_s3_file(
    bucket_name: str,
    file_name: str,
    data: str,
    key: str = None,
    secret: str = None,
    retry_count: int = DEFAULT_RETRY_COUNT,
):
    """
    Writes the given string data into the specified file in the specified bucket. If file does not exists create one, if
    exists overrides it. If the aws key and secret is not given, method uses the environmental variables as credentials.

    :param bucket_name: Name of the bucket that the target file is stored
    :param file_name: Name of the file that will be overridden
    :param data: A string contains the content of the file
    :param key: AWS access key id, default is None
    :param secret: AWS secret access key, default is None
    :param retry_count: retry count for S3 upload equals to three on default
    """

    LOGGER.info(f"Writing to {bucket_name}/{file_name} started")
    writing_start = datetime.now()
    total_upload_tries = 0
    while total_upload_tries <= retry_count:
        if key is not None and secret is not None:
            s3 = S3FileSystem(key=key, secret=secret)
        else:
            s3 = S3FileSystem()
        with s3.open(bucket_name + "/" + file_name, "w") as f:
            try:
                f.write(data)
                break
            except botocore.exceptions.NoCredentialsError as e:
                total_upload_tries = total_upload_tries + 1
                if total_upload_tries == retry_count:
                    LOGGER.error(
                        f"Writing into {bucket_name}/{file_name} failed, message {e}"
                    )
                    raise e
                time.sleep(1)
    writing_end = datetime.now()
    LOGGER.info(
        f"Writing finished in {round((writing_end - writing_start).total_seconds())} seconds"
    )


def write_to_s3_with_parquet(bucket_name: str, container_name: str, table: pa.Table):
    """
    Writes the given string data into the specified file in the specified bucket.
    :param bucket_name: Name of the bucket that the target file is stored
    :param container_name: Name of the container that will be overridden
    :param table: Table that will be written to the dataset whose filepath created by bucket_name and container_name
    """
    output_file = f"s3://{bucket_name}/{container_name}"
    s3 = S3FileSystem()
    pq.write_to_dataset(table=table, root_path=output_file, filesystem=s3)


def read_from_s3_file(
    bucket_name: str,
    file_name: str,
    key: str = None,
    secret: str = None,
    retry_count: int = DEFAULT_RETRY_COUNT,
):
    """
    Read data from the specified file in the specified bucket. If file does not exists it raises a FileNotFoundError.
    If the aws key and secret is not given, method uses the environmental variables as credentials.

    :param bucket_name: Name of the bucket that the target file is stored
    :param file_name: Name of the file that will be read
    :param key: AWS access key id, default is None
    :param secret: AWS secret access key, default is None
    :param retry_count: retry count for S3 reading equals to three on default
    :return: content of the target file in string format
    """

    LOGGER.info(f"Reading from {bucket_name}/{file_name} started")
    reading_start = datetime.now()
    total_read_tries = 0
    while total_read_tries <= retry_count:
        if key is not None and secret is not None:
            s3 = S3FileSystem(key=key, secret=secret)
        else:
            s3 = S3FileSystem()
        with s3.open(bucket_name + "/" + file_name, "rb") as f:
            try:
                data = f.read()
                break
            except botocore.exceptions.NoCredentialsError as e:
                total_read_tries = total_read_tries + 1
                if total_read_tries == retry_count:
                    LOGGER.error(
                        f"Reading from {bucket_name}/{file_name} failed, message {e}"
                    )
                    raise e
                time.sleep(1)
    reading_end = datetime.now()
    LOGGER.info(
        f"Reading finished in {round((reading_end - reading_start).total_seconds())} seconds"
    )
    return data.decode("utf-8")


def move_s3_file(
    source_path: str,
    destination_path: str,
    key: str = None,
    secret: str = None,
    retry_count: int = DEFAULT_RETRY_COUNT,
):
    """
    Move the file in the source path to the destination path. If the file does not exist in the specified
    source path, it raises a FileNotFoundError.
    If the aws key and secret is not given, method uses the environmental variables as credentials.

    :param source_path: The path where the file locates
    :param destination_path: The path where the file will be moved
    :param key: AWS access key id, default is None
    :param secret: AWS secret access key, default is None
    :param retry_count: retry count for S3 moving equals to three on default
    """

    LOGGER.info(f"Moving from {source_path} to {destination_path} started")
    moving_start = datetime.now()
    total_move_tries = 0
    while total_move_tries <= retry_count:
        if key is not None and secret is not None:
            s3 = S3FileSystem(key=key, secret=secret)
        else:
            s3 = S3FileSystem()
        try:
            s3.move(source_path, destination_path)
            break
        except botocore.exceptions.NoCredentialsError as e:
            total_move_tries = total_move_tries + 1
            if total_move_tries == retry_count:
                LOGGER.error(
                    f"Reading from {source_path} to {destination_path} failed, message {e}"
                )
                raise e
            time.sleep(1)
    moving_end = datetime.now()
    LOGGER.info(
        f"Moving finished in {round((moving_end - moving_start).total_seconds())} seconds"
    )
