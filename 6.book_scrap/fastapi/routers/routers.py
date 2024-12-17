from fastapi import APIRouter
import os
import sys
from fastapi import HTTPException
from pymongo.errors import PyMongoError

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "load"))
)
from config import dbContext

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "model"))
)
from model import BookScrap

from convert.convert import book_scrap, books_scrap
from bson import ObjectId

endPoints = APIRouter()


@endPoints.get("/")
def home():
    return {"status": "Ok", "message": "My fast API is running"}


@endPoints.get("/all/books")
def getAllBlogs():
    bookDB = dbContext()
    bookDB.connect("book_scrap")
    books_data = bookDB.executeQuery(operation="find_many")
    convertedBooks = books_scrap(books_data)
    return {"status": "Ok", "data": convertedBooks}


@endPoints.get("/get/book/{id}")
def geBook(id: str):
    bookDB = dbContext()
    bookDB.connect("book_scrap")
    try:
        query = {"_id": ObjectId(id)}  # Convert id to ObjectId
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ObjectId: {e}")

    book_data = bookDB.executeQuery(query, operation="find_one")

    if not book_data:
        raise HTTPException(status_code=404, detail="Book not found")

    convertedBook = book_scrap(book_data)
    return {"status": "Ok", "data": convertedBook}


@endPoints.post("/create/book")
def createBook(book_data: BookScrap):
    bookDB = dbContext()
    bookDB.connect("book_scrap")
    book_dict = book_data.dict()

    result = bookDB.executeNonQuery(query=book_dict, operation="insert_one")

    return {"status": "201", "data": "inserted"}


@endPoints.delete("/delete/{id}")
def deleteBook(id: str):
    try:
        bookDB = dbContext()
        bookDB.connect("book_scrap")
        query = {"_id": ObjectId(id)}
        conversation_delete = bookDB.executeQuery(query=query, operation="find_one")
        if conversation_delete is not None:
            bookDB.executeNonQuery(query=query, operation="delete_one")
            return {"status": "Ok", "message": "the book is deleted"}
        else:
            raise Exception
    except Exception as e:
        return {"status": "not found", "message": "the book is not found"}


@endPoints.patch("/update/{id}")
def updateBook(id: str, book_data: BookScrap):
    bookDB = dbContext()
    bookDB.connect("book_scrap")
    query = {"_id": ObjectId(id)}

    # Convert the Pydantic model to a dictionary
    book_dict = book_data.dict()  # This will convert the Pydantic model to a dict

    # Check if BookDetails is a Pydantic model or already a dictionary
    if isinstance(book_dict["BookDetails"], dict):
        # If it's already a dictionary, no need to convert it
        pass
    else:
        # If it's a Pydantic model, convert it to a dictionary
        book_dict["BookDetails"] = book_dict["BookDetails"].dict()

    # Prepare the update data using the $set operator
    update_data = {"$set": book_dict}

    # Execute the update query
    result = bookDB.executeNonQuery(
        query=query, update=update_data, operation="find_one_and_update"
    )

    if result:
        return {"status": "Ok", "message": "Data have been updated"}
    else:
        return {"status": "Error", "message": "No book found with the provided ID"}
