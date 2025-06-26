import json
import os
import uuid
from pymongo import MongoClient, UpdateOne

class TrekDBHandler:
    def __init__(self, mongo_uri, db_name='trek_db', collection_name='treks'):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def load_json(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        treks = data.get('data', [])
        # Add uuid to each trek if not present
        for trek in treks:
            if 'uuid' not in trek:
                trek['uuid'] = str(uuid.uuid4())
        return treks

    def upsert_treks(self, treks):
        operations = []
        for trek in treks:
            uid = trek.get('uid')
            if not uid:
                continue
            operations.append(
                UpdateOne(
                    {'uid': uid},
                    {'$set': trek},
                    upsert=True
                )
            )
        if operations:
            result = self.collection.bulk_write(operations)
            return {
                'matched': result.matched_count,
                'modified': result.modified_count,
                'upserted': len(result.upserted_ids)
            }
        return {'matched': 0, 'modified': 0, 'upserted': 0}

    def get_all_treks(self):
        return list(self.collection.find({}, {'_id': 0}))

    def close(self):
        self.client.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sync treks.json with MongoDB.")
    parser.add_argument('--json-path', required=False, default='data/treks.json', help='Path to treks.json')
    args = parser.parse_args()

    mongo_uri = os.environ.get('DB_URI')
    db_name = os.environ.get('DB_NAME', 'trek_db')
    collection_name = os.environ.get('COLLECTION_NAME_V2', 'mountains_data')

    if not mongo_uri:
        raise ValueError("DB_URI environment variable is required.")

    handler = TrekDBHandler(mongo_uri, db_name, collection_name)
    treks = handler.load_json(args.json_path)
    result = handler.upsert_treks(treks)
    print(f"Upserted: {result['upserted']}, Matched: {result['matched']}, Modified: {result['modified']}")
    handler.close()