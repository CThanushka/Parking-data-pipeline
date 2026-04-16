import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne
from pymongo.errors import PyMongoError

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_PATH = BASE_DIR / "data" / "parking_data_transformed.csv"


def load_to_mongodb(
    input_path: Path = PROCESSED_DATA_PATH,
    database_name: str = "smart_parking",
    collection_name: str = "parking_events",
) -> int:
    load_dotenv()
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

    df = pd.read_csv(input_path)
    df["entry_time"] = pd.to_datetime(df["entry_time"])
    df["exit_time"] = pd.to_datetime(df["exit_time"])

    records = df.to_dict(orient="records")
    operations = []
    for record in records:
        operations.append(
            UpdateOne(
                {"event_id": record["event_id"]},
                {"$set": record},
                upsert=True,
            )
        )

    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)

    try:
        client.admin.command("ping")
        collection = client[database_name][collection_name]

        if operations:
            collection.bulk_write(operations, ordered=False)
    except PyMongoError as exc:
        raise RuntimeError(
            "Could not connect to MongoDB. Check that MongoDB is running and "
            "that MONGODB_URI is set correctly."
        ) from exc
    finally:
        client.close()

    return len(records)


if __name__ == "__main__":
    inserted_count = load_to_mongodb()
    print(f"Loaded {inserted_count} records into MongoDB")
