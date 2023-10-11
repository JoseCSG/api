from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config

#MONGO_PORT = config("MONGO_PORT")
#MONGO_HOST = config("MONGO_HOST")
MONGO_DBNAME = config("MONGO_DBNAME")

#client = MongoClient("mongodb://localhost:27018/")

uri = "mongodb+srv://jcsg:SKxXLxVQOqdnHjFQ@cluster0.3cptiz2.mongodb.net/?retryWrites=true&w=majority"
#ssh -L 27018:localhost:27017 admin01@10.14.255.180 -N

client = MongoClient(uri, tlsAllowInvalidCertificates=True)
db = client[MONGO_DBNAME]
