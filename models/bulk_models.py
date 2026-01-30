from pydantic import BaseModel
from typing import List

class BulkInventoryUpdate(BaseModel):
    book_ids: List[str]
    available_copies: int
    reserved_copies: int
