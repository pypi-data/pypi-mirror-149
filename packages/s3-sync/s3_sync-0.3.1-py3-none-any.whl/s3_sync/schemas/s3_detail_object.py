from datetime import datetime
from typing import Dict, Any, Optional

from botocore.response import StreamingBody
from pydantic import BaseModel, Field


class S3DetailObject(BaseModel):
    response_meta_data: Dict[str, Any] = Field(alias="ResponseMetadata")
    accept_ranges: str = Field(alias="AcceptRanges")
    last_modified: datetime = Field(alias="LastModified")
    content_length: int = Field(alias="ContentLength")
    e_tag: str = Field(alias="ETag")
    content_type: str = Field(alias="ContentType")
    meta_data: Dict[str, Any] = Field(alias="Metadata")
    Body: Optional[StreamingBody] = Field(alias="Body")

    class Config:
        arbitrary_types_allowed = True
