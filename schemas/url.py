
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    long_url: HttpUrl

class URLResponse(URLCreate):
    short_url: str
    clicks: int

class URLInfo(URLResponse):
    id: int
    created_at: datetime
    updated_at: datetime
