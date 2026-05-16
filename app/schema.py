
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime 

    class Config:
        from_attributes = True



class UserBase(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_must_fit_bcrypt_limit(cls, value: str):
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be 72 bytes or fewer for bcrypt.")
        return value


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserOutWithPassword(UserOut):
    password: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


