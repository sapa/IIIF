import json
import boto3


class S3Client:
    default_bucket: str

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        default_bucket: str = "performing-arts-iiif-source",
        endpoint_url: str = "https://os.zhdk.cloud.switch.ch",
    ) -> None:
        self.default_bucket = default_bucket
        s3_session = boto3.session.Session()
        self.client = s3_session.client(
            service_name="s3",
            aws_access_key_id=client_id,
            aws_secret_access_key=client_secret,
            endpoint_url=endpoint_url,
        )

    def upload(self, path: str, body: any, bucket=None):
        if bucket is None:
            bucket = self.default_bucket
        self.client.put_object(Body=body, Bucket=bucket, Key=path)

    def upload_as_json(self, obj: any, path: str, bucket=None):
        self.upload(
            path, bytes(json.dumps(obj, ensure_ascii=False).encode("utf-8")), bucket
        )
