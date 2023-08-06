from typing import Optional

import boto3
from pydantic import BaseModel


class BotoWrapperSchema:
    client: boto3.client

    def __init__(self, connection: boto3.client):
        self.client = connection


class StorageSchema(BaseModel):
    connection: Optional[BotoWrapperSchema]
    path: Optional[str]
    bucket_name: Optional[str]
    region_name: Optional[str]
    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]

    class Config:
        arbitrary_types_allowed = True
