from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017/"

client = MongoClient(MONGO_URL)

db = client["articlehubdb"]

users_collection = db["users"]

tokens_collection = db["tokens"]
tokens_collection.create_index("email", unique=True)
