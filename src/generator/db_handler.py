import os
from pymongo import MongoClient, UpdateOne
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

class DBHandler:
    def __init__(self):
        URI = os.getenv('DB_URI')
        DB_NAME = os.getenv('DB_NAME')
        COLLECTION_NAME = os.getenv('COLLECTION_NAME')

        self.client = MongoClient(URI, server_api=ServerApi('1'))
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def builk_upsert(self, data, unique_key):
        operations = [
            UpdateOne(
                {unique_key: doc[unique_key]},
                {"$set": doc},
                upsert=True
            )
            for doc in data
        ]

        result = self.collection.bulk_write(operations)
        return  {
            "mathced_count": result.matched_count,
            "modified_count": result.modified_count,
            "upserted_count": len(result.upserted_ids)
        }
    