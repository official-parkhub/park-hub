import boto3
from loguru import logger
from settings import SETTINGS
import asyncio
from botocore.exceptions import ClientError

from src.modules.shared.enums.bucket import BucketNames

client = None


def get_client():
    global client
    if client is None:
        client = boto3.client(
            "s3",
            aws_access_key_id=SETTINGS.aws_access_key_id,
            aws_secret_access_key=SETTINGS.aws_secret_access_key,
            region_name=SETTINGS.aws_region,
            endpoint_url=getattr(SETTINGS, "aws_s3_endpoint", None),
        )

        for bucket in BucketNames:
            ensure_bucket_exists(client, bucket.value)

    return client


def ensure_bucket_exists(client, bucket_name: str):
    try:
        client.head_bucket(Bucket=bucket_name)
    except ClientError as error:
        if error.response["Error"]["Code"] == "404":
            logger.info(f"Bucket {bucket_name} does not exist. Creating it.")
            client.create_bucket(Bucket=bucket_name)
        else:
            logger.error(f"Error checking/creating bucket: {error}")
            raise


async def upload_file_object(file_object: bytes, bucket_name: str, object_name: str):
    loop = asyncio.get_event_loop()
    s3_client = get_client()
    await loop.run_in_executor(
        None, s3_client.upload_fileobj, file_object, bucket_name, object_name
    )


async def get_presigned_url(
    bucket_name: str, object_name: str, expiration: int = 3600
) -> str:
    loop = asyncio.get_event_loop()
    s3_client = get_client()
    try:
        url = await loop.run_in_executor(
            None,
            lambda: s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": object_name},
                ExpiresIn=expiration,
            ),
        )
    except ClientError as error:
        logger.error(f"Error generating presigned URL: {error}")
        return None
    return url


async def delete_file_object(bucket_name: str, object_name: str):
    loop = asyncio.get_event_loop()
    s3_client = get_client()
    await loop.run_in_executor(
        None, lambda: s3_client.delete_object(Bucket=bucket_name, Key=object_name)
    )
