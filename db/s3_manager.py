from os import listdir
from os.path import isfile, join

import boto3
from botocore.exceptions import ClientError

from constants import S3, S3_REGION
from db.bucket_policy import get_bucket_policy


class S3Manager:
    def __init__(self) -> None:
        self.client = boto3.client(S3)
        self.s3 = boto3.resource(S3)
        self.region = S3_REGION

    def create_bucket(self, bucket_name: str):
        try:
            self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": self.region,
                },
            )
        except ClientError as e:
            print(e)

    def get_bucket(self, bucket_name: str):
        try:
            bucket = self.s3.Bucket(bucket_name)
        except ClientError as e:
            print(e)
        else:
            return bucket

    def add_bucket_policy(self, bucket_name):
        try:
            bucket_policy = get_bucket_policy(bucket_name)
            self.client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        except ClientError as e:
            print(e)

    def empty_bucket(self, bucket_name: str):
        try:
            self.get_bucket(bucket_name).objects.all().delete()
        except ClientError as e:
            print(e)

    def delete_bucket(self, bucket_name: str):
        try:
            # first delete all objects
            self.empty_bucket(bucket_name)
            self.client.delete_bucket(Bucket=bucket_name)
        except ClientError as e:
            print(e)

    def upload_file(self, file_path: str, bucket_name: str, object_name: str):
        try:
            self.client.upload_file(
                file_path,
                bucket_name,
                object_name,
                # ExtraArgs={
                #     "ContentType": "image/jpeg",
                # },
            )
        except ClientError as e:
            print(e)

    def upload_files(self, folder_path: str, bucket_name: str):
        try:
            file_names = [
                file
                for file in listdir(f"{folder_path}")
                if isfile(join(f"{folder_path}", file)) and not file.endswith(".json")
            ]
            for file_name in file_names:
                self.upload_file(folder_path + "/" + file_name, bucket_name, file_name)
        except ClientError as e:
            print(e)

    def list_files(self, bucket_name: str):
        try:
            bucket = self.get_bucket(bucket_name)
            collection = bucket.objects.all()
            files = [file.key for file in collection]
        except ClientError as e:
            print(e)
        else:
            return files

    def get_file_url(self, bucket_name, file_name):
        return f"https://{bucket_name}.s3.{self.region}.amazonaws.com/{file_name}"
