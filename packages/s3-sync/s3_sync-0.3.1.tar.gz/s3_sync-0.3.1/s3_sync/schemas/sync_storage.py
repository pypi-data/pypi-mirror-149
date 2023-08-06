from typing import Optional

from pydantic import BaseModel

from s3_sync.schemas.storage import StorageSchema


class SyncStorageSchema(BaseModel):
    bucket_source: Optional[StorageSchema]
    bucket_target: Optional[StorageSchema]
