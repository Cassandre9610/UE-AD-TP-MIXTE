import json
import os
from pathlib import Path
from pymongo import MongoClient


def seed_collection(collection, filename, key):
    with open(Path(__file__).parent / "data" / filename, encoding="utf-8") as file:
        documents = json.load(file)[key]

    for source_document in documents:
        document = dict(source_document)
        document_id = document.pop("id")

        legacy_documents = list(collection.find({"id": document_id}))
        if legacy_documents:
            migrated = {
                key: value
                for key, value in legacy_documents[0].items()
                if key not in {"_id", "id"}
            }
            migrated["_id"] = document_id
            collection.delete_many({"id": document_id})
            collection.replace_one(
                {"_id": document_id},
                migrated,
                upsert=True,
            )
        else:
            document["_id"] = document_id
            collection.update_one(
                {"_id": document_id},
                {"$setOnInsert": document},
                upsert=True,
            )


def main():
    mongo_uri = os.getenv(
        "MONGO_URI",
        "mongodb://root:example@localhost:27017/?authSource=admin",
    )
    with MongoClient(mongo_uri) as client:
        database = client["movies"]
        seed_collection(database["movies"], "movies.json", "movies")
        seed_collection(database["actors"], "actors.json", "actors")


if __name__ == "__main__":
    main()
