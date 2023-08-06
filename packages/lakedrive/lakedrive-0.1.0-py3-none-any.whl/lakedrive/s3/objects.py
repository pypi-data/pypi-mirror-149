from dataclasses import dataclass


@dataclass
class S3Bucket:
    name: str
    region: str
    endpoint_url: str
    exists: bool = True
