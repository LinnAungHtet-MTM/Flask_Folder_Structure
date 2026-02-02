import re
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
    lock_flg: Literal[0, 1]  # control allowed value


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    role: int
    phone: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None

    # Email length
    @field_validator("email")
    @classmethod
    def validate_email_length(cls, v):
        if len(v) > 50:
            raise PydanticCustomError(
                "email_too_long",
                "Email must not be greater than 50 characters"
            )
        return v

    # Password format
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,20}$"

        if not re.match(pattern, v):
            raise PydanticCustomError(
                "password_invalid",
                "Password must be 6–20 characters and include at least "
                "one uppercase, lowercase letter & one digit"
            )

        return v

    # Password Match
    @field_validator("confirm_password", mode="after")
    @classmethod
    def passwords_match(cls, v, info):
        password = info.data.get("password")

        if not password:
            return v

        if v != password:
            raise PydanticCustomError(
                "password_mismatch",
                "Confirm Password and Password must match",
            )
        return v


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[int] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None

    # Email length
    @field_validator("email")
    @classmethod
    def validate_email_length(cls, v):
        if len(v) > 50:
            raise PydanticCustomError(
                "email_too_long",
                "Email must not be greater than 50 characters"
            )
        return v


class ChangePasswordRequest(BaseModel):
    password: str
    confirm_password: str

    # Password format
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,20}$"

        if not re.match(pattern, v):
            raise PydanticCustomError(
                "password_invalid",
                "Password must be 6–20 characters and include at least "
                "one uppercase, lowercase letter & one digit"
            )

        return v

    # Password Match
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        password = info.data.get("password")

        if not password:
            return v
        if v != password:
            raise PydanticCustomError(
                "password_mismatch",
                "Confirm Password and Password must match"
            )
        return v
