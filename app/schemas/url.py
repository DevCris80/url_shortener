from pydantic import BaseModel, HttpUrl, ConfigDict
from datetime import datetime


class URLCreate(BaseModel):
    long_url: HttpUrl
    user_id: int


class URLResponse(URLCreate):
    short_url: str
    clicks: int


class URLInfo(URLResponse):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class URLUpdate(BaseModel):
    long_url: HttpUrl | None = None
