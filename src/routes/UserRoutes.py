from flask import Blueprint, request, jsonify, Response
from src.utils.Security import Security
from src.db.db import db
from bson import ObjectId, json_util
main = Blueprint('user_blueprint', __name__)

@main.route('/')
def index():
  return jsonify({"message": "Hello World!"}), 200

@main.route('/add', methods=['POST'])
def create_user():
  try:
    data = request.get_json()
    db.users.insert_one(data)
    return jsonify({"message": "success!"}), 200
  except:
    return jsonify({"error": "An error happened while creating the user"}), 500
  
@main.route('/<id>', methods=['GET'])
def get_user(id):
  try:
    user = db.users.find_one({"_id": ObjectId(id)})
    res = json_util.dumps(user)
    return Response(res, mimetype='application/json'), 200
  except:
    return jsonify({"error": "An error happened while getting the user"}), 500
  
@main.route('/get', methods=['GET'])
def get_users():
  try:
    users = db.users.find()
    res = json_util.dumps(users)
    return Response(res, mimetype='application/json'), 200
  except Exception as e:
    return jsonify({"error": "An error happened while getting the users", "details": str(e)}), 500
  
@main.route('/<id>', methods=['DELETE'])
def delete_user(id):
  try:
    db.users.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "success!"}), 200
  except:
    return jsonify({"error": "An error happened while deleting the user"}), 500
