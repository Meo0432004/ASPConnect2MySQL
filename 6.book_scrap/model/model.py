from pydantic import BaseModel
from typing import List


class BookDetails(BaseModel):
    book_UPC: str
    book_description: str
    book_type: str
    availability_number: int


class BookScrap(BaseModel):
    img: str
    title: str
    price: float
    stock: str
    book_link: str
    BookDetails: BookDetails  # Nested BookDetails model
