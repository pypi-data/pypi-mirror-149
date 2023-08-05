# s3-sync

Sync AWS S3 storage from one account to another account in whatever file type.


![S3 Sync](s3_sync/images/example.png)

## Installation
```shell
  pip install s3_sync
```

## S3-Sync can read from various config

### Read from parameters
```shell
    s3-sync \
        --source-bucket-name foo \
        --source-region-name ap-southeast-1 \
        --source-access-key-id bar \
        --source-secret-access foobar \
        
        --target-bucket-name foo \
        --target-region-name ap-southeast-1 \
        --target-access-key-id bar \
        --target-secret-access foobar
```

### Read from json file
* Create example json file as bellow example, you can name this file whatever
```json
    {
      "source": {
        "bucket_name": "foo",
        "region_name": "ap-southeast-1",
        "aws_access_key_id": "bar",
        "aws_secret_access_key": "foobar"
      },
      "target": {
        "bucket_name": "foo",
        "region_name": "ap-southeast-1",
        "aws_access_key_id": "bar",
        "aws_secret_access_key": "foobar"
      }
    }
```
* Then execute command `s3-sync -json ./whatever.json`

### Read from yml or yaml file
* Create example json file as bellow example, you can name this file whatever
```yaml
source:
  bucket_name: foo
  region_name: ap-southeast-1
  aws_access_key_id: bar
  aws_secret_access_key: foobar
target:
  bucket_name: foo
  region_name: ap-southeast-1
  aws_access_key_id: bar
  aws_secret_access_key: foobar
```
* Then execute command `s3-sync -yml ./whatever.yml` or `s3-sync -yaml ./whatever.yaml`

### Pull Request are welcome