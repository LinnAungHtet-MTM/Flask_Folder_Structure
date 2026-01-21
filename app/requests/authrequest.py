from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core import PydanticCustomError

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyResetTokenRequest(BaseModel):
    token: str

class ResetPasswordRequest(BaseModel):
    token: str
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if v != info.data.get("password"):
            raise PydanticCustomError(
                "password_mismatch",
                "Confirm Password and Password must match"
            )
        return v