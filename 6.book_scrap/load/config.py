from pymongo import MongoClient
from pymongo import ReturnDocument


class dbContext:

    def __init__(self):
        MONGO_URI = "mongodb+srv://admin:nhatnlce181840@cluster0.8aba2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(MONGO_URI)
        self.db = self.client["scrap"]
        self.collection = None

    def connect(self, collection_name):
        try:
            # print("connect SUCCESSFUL")
            self.collection = self.db[collection_name]
        except Exception as e:
            print(f"Error accessing collection: {e}")
            return None

    def executeQuery(self, query="", operation="find_one"):
        if self.collection is None:
            print("No collection connected")
            return None
        try:
            if operation == "find" or operation == "find_one":
                return self.collection.find_one(query)
            elif operation == "find_many":
                return list(self.collection.find())
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def executeNonQuery(self, query=None, update=None, operation=None):
        # print("query: ", query, " operation: ", operation)
        if self.collection is None:
            print("No collection connected")
            return None
        try:
            if operation == "insert" or operation == "insert_one":
                result = self.collection.insert_one(query)
                return result.inserted_id
            elif operation == "insert_many":
                result = self.collection.insert_many(query)
                return result.inserted_ids
            elif operation == "upsert":
                result = self.collection.update_one(
                    {
                        "Rank": query["Rank"]
                    },  # Use "Rank" as the unique identifier for matching
                    {"$set": query},
                    upsert=True,  # Ensure that MongoDB either updates or inserts the document
                )
                return (
                    result.upserted_id if result.upserted_id else result.modified_count
                )
            elif operation == "update" or operation == "update_one":
                result = self.collection.update_one(query, update)
            elif operation == "delete" or operation == "delete_one":
                result = self.collection.delete_one(query)
                return result.deleted_count
            elif operation == "find_one_and_update":
                print(update)
                result = self.collection.find_one_and_update(
                    query,
                    update,
                    return_document=ReturnDocument.AFTER,
                )
                return result
        except Exception as e:
            print(f"error {e}")

    def close(self):
        self.client.close()
