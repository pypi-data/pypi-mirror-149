from typing import ClassVar, Callable
from typing import Dict, Any

import boto3

from s3_sync.schemas import (
    SyncStorageSchema,
    StorageSchema,
    SyncObject,
    S3DetailObject,
    BotoWrapperSchema,
)


class S3SyncServices:
    def __init__(
        self,
        bucket: SyncStorageSchema,
    ):
        """Initialize source and target s3 sync
        :param bucket: object configuration for source and target bucket
        """
        self.bucket = bucket

    @classmethod
    def init_connection_from(
        cls, source: StorageSchema, target: StorageSchema
    ) -> ClassVar:
        """Initialize aws object connection from specified source and target
        :param source: object source storage schema object
        :param target: object target storage schema object
        :return: current object
        """
        source.connection = BotoWrapperSchema(
            boto3.client(
                "s3",
                region_name=source.region_name,
                aws_access_key_id=source.aws_access_key_id,
                aws_secret_access_key=source.aws_secret_access_key,
            )
        )
        target.connection = BotoWrapperSchema(
            boto3.client(
                "s3",
                region_name=target.region_name,
                aws_access_key_id=target.aws_access_key_id,
                aws_secret_access_key=target.aws_secret_access_key,
            )
        )
        return cls(
            SyncStorageSchema.parse_obj(
                {
                    "bucket_source": source,
                    "bucket_target": target,
                }
            )
        )

    def get_source_object(self) -> Dict[str, SyncObject]:
        """Get all resource from source bucket in  s3 object
        :return: dictionary sync storage schema
        """
        tmp = dict()
        objects = self.bucket.bucket_source.connection.client.list_objects(
            Bucket=self.bucket.bucket_source.bucket_name
        )
        for o in objects["Contents"]:
            tmp[o["Key"]] = SyncObject.parse_obj(
                {
                    "source_bucket_name": self.bucket.bucket_source.bucket_name,
                    "target_bucket_name": self.bucket.bucket_target.bucket_name,
                    "key": o["Key"],
                    "size": o["Size"],
                }
            )
        return tmp

    def get_detail_object(self, file_name: str) -> S3DetailObject:
        """fetch detail source from specified bucket and filename
        :param file_name: string file name
        :return: dictionary data
        """
        resp = self.bucket.bucket_source.connection.client.get_object(
            Bucket=self.bucket.bucket_source.bucket_name, Key=file_name
        )
        return S3DetailObject.parse_obj(resp)

    def upload_files(
        self, file: SyncObject, callback: Callable = None
    ) -> Dict[str, Any]:
        """Upload files to s3 services
        :param file: object detail for SyncStorageSchema
        :param callback: function callable
        :return: response upload
        """
        if callback is None:
            return self.bucket.bucket_target.connection.client.upload_fileobj(
                file.body, file.target_bucket_name, file.key
            )

        return self.bucket.bucket_target.connection.client.upload_fileobj(
            file.body,
            file.target_bucket_name,
            file.key,
            Callback=callback,
        )
