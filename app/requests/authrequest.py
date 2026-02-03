import re
from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core import PydanticCustomError


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember: bool

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


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyResetTokenRequest(BaseModel):
    token: str


class ResetPasswordRequest(BaseModel):
    token: str
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
