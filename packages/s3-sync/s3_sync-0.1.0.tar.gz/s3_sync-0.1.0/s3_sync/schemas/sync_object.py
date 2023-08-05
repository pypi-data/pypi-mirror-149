from typing import Optional

from pydantic import BaseModel


class SyncObject(BaseModel):
    source_bucket_name: Optional[str]
    target_bucket_name: Optional[str]
    key: Optional[str]
    size: Optional[int]
    body: Optional[bytes]
