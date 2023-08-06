from typing import Dict, ClassVar

from s3_sync.schemas import StorageSchema, SyncObject
from s3_sync.services import S3SyncServices
from s3_sync.utils import scan_object


class SyncController:
    def __init__(
        self,
        data_source: StorageSchema,
        data_target: StorageSchema,
        services: S3SyncServices,
    ):
        self.data_source = data_source
        self.data_target = data_target
        self.services = services

    @classmethod
    def sync_cross_account_from_param(
        cls, data_source: Dict[str, str], data_target: Dict[str, str]
    ) -> ClassVar:
        """Create new object model source and target from specified data
        :param data_source: dictionary data source bucket
        :param data_target: dictionary data target bucket
        :return: bucket sync storage
        """
        source = StorageSchema.parse_obj(data_source)
        target = StorageSchema.parse_obj(data_target)
        return cls(source, target, S3SyncServices.init_connection_from(source, target))

    @classmethod
    def sync_server_local_from_param(
        cls, data_source: Dict[str, str], data_target: Dict[str, str]
    ) -> ClassVar:
        """Create new object model source and target from specified data
        :param data_source: dictionary data source bucket
        :param data_target: dictionary data target bucket
        :return: bucket sync storage
        """
        source = StorageSchema.parse_obj(data_source)
        target = StorageSchema.parse_obj(data_target)
        return cls(
            source,
            target,
            S3SyncServices.init_source_connection_from(source),
        )

    @classmethod
    def sync_local_server_from_param(
        cls,
        data_source: Dict[str, str],
        data_target: Dict[str, str],
    ) -> ClassVar:
        """Create new object model source and target from specified data
        :param data_source: dictionary data source bucket
        :param data_target: dictionary data target bucket
        :return: bucket sync storage
        """
        source = StorageSchema.parse_obj(data_source)
        target = StorageSchema.parse_obj(data_target)
        return cls(
            source,
            target,
            S3SyncServices.init_target_connection_from(target),
        )

    def start_sync_cross_account(self, data: Dict[str, SyncObject]) -> None:
        """sync all data from source to target
        fetch all data from source and upload to target
        :return: none
        """

        def fetch_detail_and_sync(sync_data: SyncObject) -> None:
            detail_object = self.services.get_detail_source_object(sync_data.key)
            sync_data.body = detail_object.Body
            # start upload data to target bucket
            self.services.upload_target_files(sync_data)
            return None

        _ = list(map(fetch_detail_and_sync, data.values()))
        return None

    def start_sync_server_to_local(self, data: Dict[str, SyncObject]) -> None:
        """sync all data from source to target
        fetch all data from source and upload to path target
        :return: none
        """

        def sync_server_to_local(sync_data: SyncObject) -> None:
            # start download data from source target bucket to local data
            self.services.download_source_object(sync_data, self.data_target.path)
            return None

        _ = list(map(sync_server_to_local, data.values()))
        return None

    def start_sync_local_to_server(self, data: Dict[str, SyncObject]) -> None:
        """sync all data from source to target
        fetch all data from source path and upload to target
        :return: none
        """

        def sync_local_to_server(sync_data: SyncObject) -> None:
            # start download data from source target bucket to local data
            self.services.upload_target_files(sync_data)
            return None

        _ = list(map(sync_local_to_server, data.values()))
        return None

    def sync(
        self,
        cross_account: bool = False,
        server_to_local: bool = False,
        local_to_server: bool = False,
    ) -> None:
        """entry point to start sync from s3 server to local directory
        :return: none
        """
        if cross_account:
            return self.start_sync_cross_account(self.services.get_source_object())

        if server_to_local:
            return self.start_sync_server_to_local(self.services.get_source_object())

        if local_to_server:
            return self.start_sync_local_to_server(
                scan_object(self.data_source.path, self.data_target.bucket_name)
            )
