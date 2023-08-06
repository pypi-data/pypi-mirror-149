import argparse
import json
from typing import Dict, Tuple

import yaml

from s3_sync.controllers import SyncController


def parse_arguments(
    args: argparse.ArgumentParser.parse_args,
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Parse parameter input to dictionary parameter
    :param args: parser object
    :return:tuple of dictionary
    """
    if args.read_json:
        with open(args.read_json, "r") as f:
            data = json.loads(f.read())
        return data["source"], data["target"]

    if args.read_yml or args.read_yaml:
        with open(args.read_yml) as file:
            data = yaml.full_load(file)
        return data["source"], data["target"]

    source_param = {
        "path": args.source_local_path,
        "bucket_name": args.source_bucket_name,
        "region_name": args.source_region_name,
        "aws_access_key_id": args.source_access_key_id,
        "aws_secret_access_key": args.source_secret_access,
    }
    target_param = {
        "path": args.target_local_path,
        "bucket_name": args.target_bucket_name,
        "region_name": args.target_region_name,
        "aws_access_key_id": args.target_access_key_id,
        "aws_secret_access_key": args.target_secret_access,
    }
    return source_param, target_param


def main():
    parser = argparse.ArgumentParser(description="s3 sync script")
    # parse data source
    parser.add_argument("-sbn", "--source-bucket-name", type=str, default="")
    parser.add_argument("-srn", "--source-region-name", type=str, default="")
    parser.add_argument("-sak", "--source-access-key-id", type=str, default="")
    parser.add_argument("-ssa", "--source-secret-access", type=str, default="")
    parser.add_argument("-slp", "--source-local-path", type=str, default="")

    # parse data target
    parser.add_argument("-tbn", "--target-bucket-name", type=str, default="")
    parser.add_argument("-trn", "--target-region-name", type=str, default="")
    parser.add_argument("-tak", "--target-access-key-id", type=str, default="")
    parser.add_argument("-tsa", "--target-secret-access", type=str, default="")
    parser.add_argument("-tlp", "--target-local-path", type=str, default="")

    # parse config
    parser.add_argument("-json", "--read-json", type=str, default="")
    parser.add_argument("-yml", "--read-yml", type=str, default="")
    parser.add_argument("-yaml", "--read-yaml", type=str, default="")

    # parse default syncing
    parser.add_argument("-sca", "--sync-cross-account", type=bool, default=False)
    parser.add_argument("-ssl", "--sync-server-local", type=bool, default=False)
    parser.add_argument("-sls", "--sync-local-server", type=bool, default=False)

    args = parser.parse_args()

    source_param, target_param = parse_arguments(args)

    # if parameter is sync cross account
    if args.sync_cross_account:
        cls = SyncController.sync_cross_account_from_param(source_param, target_param)
        cls.sync(cross_account=args.sync_cross_account)

    # if parameter is sync from server to local
    if args.sync_server_local:
        cls = SyncController.sync_server_local_from_param(source_param, target_param)
        cls.sync(server_to_local=args.sync_server_local)

    # if parameter is sync from local to server
    if args.sync_local_server:
        cls = SyncController.sync_local_server_from_param(source_param, target_param)
        cls.sync(local_to_server=args.sync_local_server)
