import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "model"))
from model import BookScrap, BookDetails


def serialize_to_book_scrap(
    img: str,
    title: str,
    price: float,
    stock: str,
    book_link: str,
    book_UPC: str,
    book_description: str,
    book_type: str,
    availability_number: int,
) -> BookScrap:
    """
    Serializes provided data into a BookScrap instance.
    """
    return BookScrap(
        img=img,
        title=title,
        price=price,
        stock=stock,
        book_link=book_link,
        BookDetails=BookDetails(
            book_UPC=book_UPC,
            book_description=book_description,
            book_type=book_type,
            availability_number=availability_number,
        ),
    )
