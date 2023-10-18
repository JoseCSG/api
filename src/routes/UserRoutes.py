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
  
@main.route('/following/<id>', methods=['GET'])
def get_following(id):
  try:
    following = db.users.find_one({"_id": ObjectId(id)})["orgs_followed"]
    res = []
    for id in following:
      org = db.organizations.find_one({"_id": ObjectId(id)})
      res.append({
        "id": id,
        "name": org["name"],
        "img_src": org["img_src"]
      })
    return jsonify(res), 200
  except Exception as e:
    return jsonify({"error": "An error happened while getting the following", "details": str(e)}), 500
  

@main.route('/follow/<id_org>/<id_usuario>', methods=['PATCH'])
def follow_org(id_org, id_usuario):
  has_access = Security.verify_token(request.headers)
  if has_access:
    try:
      db.users.update_one({"_id": ObjectId(id_usuario)}, {"$push": {"orgs_followed": id_org}})
      db.organizations.update_one({"_id": ObjectId(id_org)}, {"$inc": {"followers": 1}})
      return jsonify({"message": "success"}), 200
    except Exception as e:
      return jsonify({"error": str(e)}), 401
    

@main.route('/unfollow/<id_org>/<id_usuario>', methods=['PATCH'])
def unfollow_org(id_org, id_usuario):
  has_access = Security.verify_token(request.headers)
  if has_access:
    try:
      db.users.update_one({"_id": ObjectId(id_usuario)}, {"$pull": {"orgs_followed": id_org}})
      db.organizations.update_one({"_id": ObjectId(id_org)}, {"$inc": {"followers": -1}})
      return jsonify({"message": "success"}), 200
    except Exception as e:
      return jsonify({"error": str(e)}), 401



