import boto3

from constants import S3


class S3Manager:
    def __init__(self) -> None:
        self.client = boto3.client(S3)
        self.s3 = boto3.resource(S3)

    def create_bucket(self, bucket_name: str):
        try:
            self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": "us-east-2",
                },
            )
        except Exception as e:
            print(e)

    def get_bucket(self, bucket_name: str):
        try:
            bucket = self.s3.Bucket(bucket_name)
        except Exception as e:
            print(e)
        else:
            return bucket

    def delete_bucket(self, bucket_name: str):
        try:
            self.client.delete_bucket(Bucket=bucket_name)
        except Exception as e:
            print(e)
