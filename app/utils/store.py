import os, boto3
from urllib.parse import urljoin
class ArtifactStore:
    def __init__(self):
        self.bucket = os.getenv("S3_BUCKET")
        self.endpoint_url = os.getenv("S3_ENDPOINT_URL") or None
        self.region = os.getenv("S3_REGION", "us-east-1")
        self._client = None
        if self.bucket:
            self._client = boto3.client("s3", region_name=self.region, endpoint_url=self.endpoint_url)
        self.local_dir = "/tmp/artifacts"
        os.makedirs(self.local_dir, exist_ok=True)
    def put_bytes(self, key: str, data: bytes) -> str:
        if self._client:
            self._client.put_object(Bucket=self.bucket, Key=key, Body=data, ACL="public-read")
            if self.endpoint_url:
                base = self.endpoint_url.rstrip("/") + "/" + self.bucket + "/"
                return urljoin(base, key)
            return f"https://{self.bucket}.s3.amazonaws.com/{key}"
        path = os.path.join(self.local_dir, key.replace("/", "_"))
        with open(path, "wb") as f:
            f.write(data)
        return f"file://{path}"
