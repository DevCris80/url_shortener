from pydantic import BaseModel
from datetime import datetime

class URLBase(BaseModel):
    long_url: str

class URL(URLBase):
    is_active: bool
    clicks: int

    model_config = {"from_attributes": True}

class URLInfo(URL):
    short_url: str
    created_at: datetime
