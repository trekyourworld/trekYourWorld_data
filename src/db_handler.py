import os
from pymongo import MongoClient, UpdateOne
from dotenv import load_dotenv

load_dotenv()

# db script to sync data to db on invocation

class DBHandler:
    def __init__(self, data):
        URI = os.getenv('DB_URI')
        DB_NAME = os.getenv('DB_NAME')
        COLLECTION_NAME = os.getenv('COLLECTION_NAME')

        self.client = MongoClient(URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]
        self.input_data = data

    def insert_data(self):
        for trek_data in self.input_data:
            # print(trek_data)
            document = { "org": trek_data["org"], "treks": trek_data["treks"]}
            result = self.collection.insert_one(document)
            print(f"Document inserted with ID: {result.inserted_id}")

    def update_data(self):
        for trek_data in self.input_data:
            updated_document = { "treks": trek_data["treks"]}
            result = self.collection.update_one(
                {"org": trek_data["org"]},
                { 
                    "$set": updated_document,
                    "$setOnInsert": { "org": trek_data["org"] }  # Ensures that 'org' is set if the document is inserted
                },
                upsert=True  # This enables the upsert behavior
            )
        
        # Check if the document was updated or inserted
        if result.matched_count > 0:
            print("Update successful.")
        elif result.upserted_id:
            print(f"New document inserted with id: {result.upserted_id}")
        else:
            print("No operation performed.")

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
    