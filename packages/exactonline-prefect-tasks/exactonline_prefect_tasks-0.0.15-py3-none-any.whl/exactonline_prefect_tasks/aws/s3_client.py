import boto3


class S3Client:
    """Client for AWS S3"""

    _instance = None

    def __init__(self, s3_client, bucket):
        self.s3_client = s3_client
        self.bucket = bucket

    @staticmethod
    def get_instance(access_key, secret_key, region_name='us-west-2', bucket_name='bucket'):
        if S3Client._instance is None:
            s3_client = boto3.resource(
                's3',
                region_name=region_name,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            )
            bucket = s3_client.Bucket(bucket_name)
            S3Client._instance = S3Client(s3_client, bucket)
        return S3Client._instance

    def download_file(self, key, dest):
        self.bucket.download_file(key, dest)

    def upload_file(self, src, key):
        self.bucket.Object(key).put(Body=open(src, 'rb'))

