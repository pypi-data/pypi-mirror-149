from typing import Dict, ClassVar

import tqdm

from s3_sync.schemas import StorageSchema, SyncObject
from s3_sync.services import S3SyncServices


class SyncController:
    def __init__(self, data_source: StorageSchema, data_target: StorageSchema):
        self.data_source = data_source
        self.data_target = data_target
        self.services = S3SyncServices.init_connection_from(data_source, data_target)

    @classmethod
    def from_dict(
        cls, data_source: Dict[str, str], data_target: Dict[str, str]
    ) -> ClassVar:
        """Create new object model source and target from specified data
        :param data_source: dictionary data source bucket
        :param data_target: dictionary data target bucket
        :return: bucket sync storage
        """
        source = StorageSchema.parse_obj(data_source)
        target = StorageSchema.parse_obj(data_target)
        return cls(source, target)

    def start_sync(self, data: Dict[str, SyncObject]) -> None:
        """sync all data from source to target
        fetch all data from source and upload to target
        :return: none
        """

        def fetch_detail_and_sync(sync_data: SyncObject) -> None:
            detail_object = self.services.get_detail_object(sync_data.key)
            sync_data.body = detail_object.Body

            with tqdm.tqdm(
                total=sync_data.size,
                desc=sync_data.key,
                bar_format="[{desc}]: {percentage:3.0f}% | {elapsed}",
            ) as progress_bar:
                # start upload data to target bucket
                self.services.upload_files(
                    sync_data,
                    callback=lambda bytes_transferred: progress_bar.update(
                        bytes_transferred
                    ),
                )
            return None

        _ = list(map(fetch_detail_and_sync, data.values()))
        return None

    def sync(self) -> None:
        """entry point to start sync
        :return: none
        """
        return self.start_sync(self.services.get_source_object())
