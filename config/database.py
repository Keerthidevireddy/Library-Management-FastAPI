from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URL)
db = client["library_db"]

users_collection = db["users"]
books_collection = db["books"]
roles_collection = db["roles"]
audit_collection = db["book_audit"]
