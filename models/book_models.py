from pydantic import BaseModel, Field
from typing import Optional, List

class BookCreateRequest(BaseModel):
    title: str = Field(..., min_length=1)
    edition: str
    author: str
    genre: str
    category: str
    sub_category: str
    language: str
    publication_year: int
    total_copies: int
    available_copies: int
    reserved_copies: int

class BookPatchRequest(BaseModel):
    title: Optional[str] = None
    edition: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    language: Optional[str] = None
    publication_year: Optional[int] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None
    reserved_copies: Optional[int] = None

class BookStatusUpdateRequest(BaseModel):
    target_status: str
    version: int
    rejection_reason: Optional[str] = None

class BulkInventoryUpdateRequest(BaseModel):
    book_ids: List[str]

    available_copies: Optional[int] = None
    total_copies: Optional[int] = None
    reserved_copies: Optional[int] = None