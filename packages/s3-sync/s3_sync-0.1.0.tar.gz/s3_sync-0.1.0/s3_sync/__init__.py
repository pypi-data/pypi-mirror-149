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
        "bucket_name": args.source_bucket_name,
        "region_name": args.source_region_name,
        "aws_access_key_id": args.source_access_key_id,
        "aws_secret_access_key": args.source_secret_access,
    }
    target_param = {
        "bucket_name": args.target_bucket_name,
        "region_name": args.target_region_name,
        "aws_access_key_id": args.target_access_key_id,
        "aws_secret_access_key": args.target_secret_access,
    }
    return source_param, target_param


def main():
    parser = argparse.ArgumentParser(description="s3 sync script")
    parser.add_argument("-sbn", "--source-bucket-name", type=str, default="")
    parser.add_argument("-srn", "--source-region-name", type=str, default="")
    parser.add_argument("-sak", "--source-access-key-id", type=str, default="")
    parser.add_argument("-ssa", "--source-secret-access", type=str, default="")

    parser.add_argument("-tbn", "--target-bucket-name", type=str, default="")
    parser.add_argument("-trn", "--target-region-name", type=str, default="")
    parser.add_argument("-tak", "--target-access-key-id", type=str, default="")
    parser.add_argument("-tsa", "--target-secret-access", type=str, default="")
    parser.add_argument("-json", "--read-json", type=str, default="")
    parser.add_argument("-yml", "--read-yml", type=str, default="")
    parser.add_argument("-yaml", "--read-yaml", type=str, default="")

    args = parser.parse_args()

    source_param, target_param = parse_arguments(args)
    cls = SyncController.from_dict(source_param, target_param)
    cls.sync()
