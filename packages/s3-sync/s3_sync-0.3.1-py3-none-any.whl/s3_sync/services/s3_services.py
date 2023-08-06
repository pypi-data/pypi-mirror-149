from pathlib import Path
from typing import ClassVar
from typing import Dict

import boto3
import tqdm

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
        self.bar_format = "[{desc}]: {percentage:3.0f}% | {elapsed}"

    @classmethod
    def init_source_connection_from(cls, source: StorageSchema) -> ClassVar:
        """Initialize aws object connection from specified source and target
        :param source: object source storage schema object
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
        return cls(
            SyncStorageSchema.parse_obj(
                {
                    "bucket_source": source,
                }
            )
        )

    @classmethod
    def init_target_connection_from(cls, target: StorageSchema) -> ClassVar:
        """Initialize aws object connection from specified source and target
        :param target: object target storage schema object
        :return: current object
        """
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
                    "bucket_target": target,
                }
            )
        )

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
            p = {
                "key": o["Key"],
                "size": o["Size"],
            }
            if self.bucket.bucket_source is not None:
                p["source_bucket_name"] = self.bucket.bucket_source.bucket_name

            if self.bucket.bucket_target is not None:
                p["target_bucket_name"] = self.bucket.bucket_target.bucket_name

            tmp[o["Key"]] = SyncObject.parse_obj(p)
        return tmp

    def get_detail_source_object(self, file_name: str) -> S3DetailObject:
        """fetch detail source from specified bucket and filename
        :param file_name: string file name
        :return: dictionary data
        """
        resp = self.bucket.bucket_source.connection.client.get_object(
            Bucket=self.bucket.bucket_source.bucket_name, Key=file_name
        )
        return S3DetailObject.parse_obj(resp)

    def upload_target_files(self, file: SyncObject) -> None:
        """Upload files to s3 services
        :param file: object detail for SyncStorageSchema
        :return: none
        """
        with tqdm.tqdm(
            total=file.size,
            desc=file.key,
            bar_format=self.bar_format,
        ) as progress_bar:
            self.bucket.bucket_target.connection.client.upload_fileobj(
                file.body,
                file.target_bucket_name,
                file.key,
                Callback=lambda bytes_transferred: progress_bar.update(
                    bytes_transferred
                ),
            )

    def download_source_object(self, file: SyncObject, path: str) -> None:
        """Download all s3 files and sync to local file
        :param file: object sync object
        :param path: string path to sync with
        :return: none value
        """
        p = "{}/{}".format(path, file.key)
        # if this type file is directory then create directory
        if file.key.endswith("/"):
            Path(p).mkdir(parents=True, exist_ok=True)
            return None

        with open(p, "wb") as f:
            with tqdm.tqdm(
                total=file.size,
                desc=file.key,
                bar_format=self.bar_format,
            ) as progress_bar:
                self.bucket.bucket_source.connection.client.download_fileobj(
                    self.bucket.bucket_source.bucket_name,
                    file.key,
                    f,
                    Callback=lambda bytes_transferred: progress_bar.update(
                        bytes_transferred
                    ),
                )
