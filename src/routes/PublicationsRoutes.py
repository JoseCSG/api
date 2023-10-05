from flask import Blueprint, request, Response, jsonify
from src.utils.Security import Security
from datetime import datetime
from src.db.db import db
from bson import ObjectId, json_util

main = Blueprint('publications_blueprint', __name__)

@main.route('/', methods=['GET'])
def get_publications():
  has_access = Security.verify_token(request.headers)
  if has_access:
    return jsonify({"message": "success!"}), 200
  else:
    return jsonify({"error": "Unauthorized"}), 401
  
@main.route('/add', methods=['POST'])
def create_publication():
  has_access = Security.verify_token(request.headers)
  if has_access:
    data = request.get_json()
    if not data['title'] or not data['description'] or not data['user_id'] or not data['org_id']:
      return jsonify({"error": "Data not completed"})
    pub = {
      "title": data["title"],
      "description": data["description"],
      "img_url": data["img_url"],
      "likes": 0,
      "user_id": data["user_id"],
      "org_id": data["org_id"],
      "created_at": datetime.now(),
    }
    db.publications.insert_one(pub)
    return jsonify({"message": "success!"}), 200
  else:
    return jsonify({"error": "Unauthorized"}), 401

@main.route('/<id>', methods=['GET'])
def get_publication():
  has_access = Security.verify_token(request.headers)
  if has_access:
    pub  = db.publications.find_one({"_id": ObjectId(id)})
    res = json_util.dumps(pub)
    return Response(res, mimetype='application/json'), 200
  else:
    return jsonify({"error": "Unauthorized"}), 401
  
@main.route('/<id>', methods=['DELETE'])
def delete_publication(id):
  has_access = Security.verify_token(request.headers)
  if has_access:
    db.publications.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "success!"}), 200
  else:
    return jsonify({"error": "Unauthorized"}), 401

@main.route('/like/<id>', methods=['PATCH'])
def like_publication(id):
  has_access = Security.verify_token(request.headers)
  if has_access:
    res = db.publications.update_one({"_id": ObjectId(id)}, {"$inc": {"likes": 1}})
    if res.matched_count == 0:
      return jsonify({"error": "Publication not found"}), 404
    else:
      return jsonify({"message": "success!"}), 200
  else:
    return jsonify({"error": "Unauthorized"}), 401

@main.route('/dislike/<id>', methods=['PATCH'])
def dislike_publication(id):
  has_access = Security.verify_token(request.headers)
  if has_access:
    res = db.publications.update_one({"_id": ObjectId(id)}, {"$inc": {"likes": -1}})
    if res.matched_count == 0:
      return jsonify({"error": "Publication not found"}), 404
    else:
      return jsonify({"message": "success!"}), 200
  else:
    return jsonify({"error": "Unauthorized"}), 401
  
@main.route('/org/<id>', methods=['GET'])
def get_publications_org(id):
  has_access = Security.verify_token(request.headers)
  if has_access:
    try:
      pubs = db.publications.find({"org_id": id})
      res = json_util.dumps(pubs)
      return Response(res, mimetype='application/json'), 200
    except Exception as e:
      return {"error": str(e)}, 400
  else:
    return jsonify({"error": "Unauthorized"}), 401