from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core import PydanticCustomError
from datetime import date

class UserSearchRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class LockUsersRequest(BaseModel):
    user_ids: list[int]
    lock_flg: Literal[0, 1]    #control allowed value

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    role: int
    phone: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None

    # Password Match
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if v != info.data.get("password"):
            raise PydanticCustomError(
                "password_mismatch",
                "Confirm Password and Password must match"
            )
        return v

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[int] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None