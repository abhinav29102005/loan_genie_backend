from pymongo import MongoClient
from pymongo.database import Database
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "loan_system"

client = MongoClient(MONGODB_URI)
db: Database = client[DB_NAME]

customers_collection = db["customers"]
offers_collection = db["offers"]

client.admin.command("ping")
print(f"Connected to Mongo baby: {DB_NAME}")
