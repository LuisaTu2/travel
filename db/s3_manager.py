import boto3
from botocore.exceptions import ClientError

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
            # TODO: try to figure this one out
            # self.client.put_bucket_acl(ACL=ACL.PUBLIC_READ, Bucket=bucket_name)
        except ClientError as e:
            print(e)

    def get_bucket(self, bucket_name: str):
        try:
            bucket = self.s3.Bucket(bucket_name)
        except ClientError as e:
            print(e)
        else:
            return bucket

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

        # Add policy
        """
        import json

    # Create a bucket policy
    bucket_name = 'BUCKET_NAME'
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': f'arn:aws:s3:::{bucket_name}/*'
        }]
    }

    # Convert the policy from JSON dict to string
    bucket_policy = json.dumps(bucket_policy)

    # Set the new policy
    s3 = boto3.client('s3')
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
    """

    # TODO: fix the content type
    def upload_file(self, file_name: str, bucket_name: str, object_name: str):
        try:
            self.client.upload_file(
                file_name,
                bucket_name,
                object_name,
                ExtraArgs={"ContentType": "image/png"},
            )
        except ClientError as e:
            print(e)
