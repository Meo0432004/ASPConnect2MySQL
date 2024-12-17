from typing import List


def book_scrap(single_book) -> dict:
    """
    Converts a single book document to a dictionary.
    """
    return {
        "_id": str(single_book["_id"]),
        "img": str(single_book["img"]),
        "title": str(single_book["title"]),
        "price": float(single_book["price"]),
        "stock": str(single_book["stock"]),
        "book_link": str(single_book["book_link"]),
        "BookDetails": {
            "book_UPC": str(single_book["BookDetails"]["book_UPC"]),
            "book_description": str(
                single_book["BookDetails"].get("book_description", "")
            ),
            "book_type": str(single_book["BookDetails"].get("book_type", "")),
            "availability_number": int(
                single_book["BookDetails"].get("availability_number", 0)
            ),
        },
    }


def books_scrap(books_data) -> list:
    """
    Converts a list of book documents to a list of dictionaries.
    """
    return [book_scrap(single_book) for single_book in books_data]
