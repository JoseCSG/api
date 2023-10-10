from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config
from pymongo.server_api import ServerApi

MONGO_PORT = config("MONGO_PORT")
MONGO_HOST = config("MONGO_HOST")
MONGO_DBNAME = config("MONGO_DBNAME")

#client = MongoClient("mongodb://localhost:27017/")

uri = "mongodb+srv://jcsg:SKxXLxVQOqdnHjFQ@cluster0.3cptiz2.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tlsAllowInvalidCertificates=True)
client.admin.command('ismaster')
db = client[MONGO_DBNAME]
