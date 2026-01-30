from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)
    organization: str
    role: Literal["ADMIN", "AUTHOR", "USER", "REVIEWER"]


class UserLoginRequest(BaseModel):
    username: str
    password: str
