from pymongo import MongoClient
from bson.objectid import ObjectId

#MONGO_PORT = config("MONGO_PORT")
#MONGO_HOST = config("MONGO_HOST")
#MONGO_DBNAME = config("MONGO_DBNAME")

client = MongoClient("mongodb://localhost:27018/")
db = client["datos"]
