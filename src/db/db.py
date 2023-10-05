from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

MONGO_PORT = config("MONGO_PORT")
MONGO_HOST = config("MONGO_HOST")
MONGO_DBNAME = config("MONGO_DBNAME")

client = MongoClient("mongodb://localhost:27017/")
db = client[MONGO_DBNAME]
