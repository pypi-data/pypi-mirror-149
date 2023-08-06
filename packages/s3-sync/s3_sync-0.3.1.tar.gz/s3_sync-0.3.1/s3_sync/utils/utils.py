import io
import os
from typing import Dict

from s3_sync.schemas import SyncObject


def is_folder(path: str) -> bool:
    """Check is giver string path is folder or not
    :param path: string path
    :return: boolean true or false
    """
    return os.path.isdir(path)


def scan_object(
    path: str, bucket_name: str, result: Dict[str, SyncObject] = None
) -> Dict[str, SyncObject]:
    """Scan all object inside folder and return response and dictionary data object
    :param path: string path that we want to scan please use absolute path
    :param bucket_name: string bucket name for uploading on target s3
    :param result: dictionary data result as temporary store
    :return: dictionary object SyncObject
    """
    if result is None:
        result = dict()

    for root_dir, folders, files in os.walk(path):
        for folder in folders:
            p = "{}/{}".format(root_dir, folder)
            scan_object(p, bucket_name, result)
            continue

        for file in files:
            p = "{}/{}".format(root_dir, file)
            result[p] = SyncObject.parse_obj(
                {
                    "key": p,
                    "size": 0,
                    "body": bytes(0),
                    "target_bucket_name": bucket_name,
                }
            )
            with open(p, "rb") as f:
                result[p].size = os.path.getsize(p)
                result[p].body = io.BytesIO(f.read())

    return result
