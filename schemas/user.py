from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserRead(BaseModel):
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8)