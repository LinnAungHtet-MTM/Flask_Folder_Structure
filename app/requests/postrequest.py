from typing import Optional
from pydantic import BaseModel

class CreatePostRequest(BaseModel):
    title: str
    description: str

class PostSearchRequest(BaseModel):
    keyword: Optional[str] = None
    status: Optional[int] = None
    date: Optional[str] = None

class UpdatePostRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None