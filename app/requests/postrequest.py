from typing import Optional
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError

class CreatePostRequest(BaseModel):
    title: str
    description: str

    # Title length
    @field_validator("title")
    @classmethod
    def validate_title_length(cls, v):
        if len(v) > 255:
            raise PydanticCustomError(
                "title_too_long",
                "title field must not be greater than 255"
            )
        return v


class PostSearchRequest(BaseModel):
    keyword: Optional[str] = None
    status: Optional[int] = None
    date: Optional[str] = None


class UpdatePostRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None

    # Title length
    @field_validator("title")
    @classmethod
    def validate_title_length(cls, v):
        if len(v) > 255:
            raise PydanticCustomError(
                "title_too_long",
                "title field must not be greater than 255"
            )
        return v
