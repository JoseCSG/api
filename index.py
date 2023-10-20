""" from flask import Flask, request, jsonify
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection setup through the SSH tunnel
client = MongoClient("mongodb://localhost:27018/")
db = client["datos"]
collection = db["publications"]

@app.route('/publications/add', methods=['POST'])
def add_publication():
    try:
      pub = {
          "title": "Un titulo genericooooo",
          "img": "A_random_URL",
          "description": "Una descripcion generica",
          "date": "A date",
          "id_org": "An organization id",
          "likes": 30,
          "comments": 10,
      } 
      result = collection.insert_one(pub)
      return jsonify({"success": "Publication added successfully", "id": str(result.inserted_id)}), 200
    except Exception as e:
        return jsonify({"error": "An error happened while uploading the publication", "details:": str(e)}), 500
 """

from src import init_app
from config import config
from flask_cors import CORS

configuration = config["development"]
app = init_app(configuration)
CORS(app)

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
