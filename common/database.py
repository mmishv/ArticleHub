import os

from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017/"

TOKEN_COLLECTION_NAME = 'tokens'
ARTICLE_COLLECTION_NAME = 'users'
USER_COLLECTION_NAME = 'users'

client = MongoClient(MONGO_URL)

test_db_name = "test_articlehub_db"
test_database = client[test_db_name]

main_db_name = "articlehubdb"
main_db = client[main_db_name]


def get_test_mode():
    a = os.environ.get("TEST_MODE", "").lower()
    print("feg vdbgt gd" + a)
    return os.environ.get("TEST_MODE", "").lower() == "true"


def get_database():
    if get_test_mode():
        return client[test_db_name]
    else:
        return client[main_db_name]


db = get_database()


def get_user_collection():
    return get_database()[USER_COLLECTION_NAME]


def get_article_collection():
    return db[ARTICLE_COLLECTION_NAME]


def get_token_collection():
    return db[TOKEN_COLLECTION_NAME]
