from flask import Blueprint, request, Response, jsonify
from src.utils.Security import Security
from datetime import datetime
from src.db.db import db
from bson import ObjectId, json_util
from copy import deepcopy

main = Blueprint('publications_blueprint', __name__)

@main.route('/<id_user>', methods=['GET'])
def get_publications(id_user):
  has_access = Security.verify_token(request.headers)
  if has_access:
    user = db.users.find_one({"_id": ObjectId(id_user)})
    orgs_followed = user.get("orgs_followed", [])
    data = []
    for org in orgs_followed:
      # Iterate over the cursor to append actual documents to the data list
      for pub in db.publications.find({"org_id": org}).sort("created_at", -1).limit(5):        
        data.append(pub)

    pubs = []
    for pub in data:
      pub_copy = deepcopy(pub)
            
      try:
        org = db.organizations.find_one({"_id": ObjectId(pub_copy["org_id"])})
        if org:
          pub_copy["img_org"] = org["img_src"]
        if str(pub_copy["_id"]) in user["liked_pubs"]:
          pub_copy["liked"] = True
        else:
          pub_copy["liked"] = False

        pubs.append(pub_copy)
      except Exception as e:
        print(f"Error: {e}")

    pubs.sort(key=lambda x: x["created_at"], reverse=True)
    res = json_util.dumps(pubs)
    return Response(res, mimetype='application/json'), 200
  else:
    return jsonify({"error": "Unauthorized"}), 401
    
@main.route('/add', methods=['POST'])
def create_publication():
  has_access = Security.verify_token(request.headers)
  if has_access:
    data = request.get_json()
    if not data['title'] or not data['description'] or not data['user_id'] or not data['org_id']:
      return jsonify({"error": "Data not completed"})
    try:
      print(data)
      pub = {
        "title": data["title"],
        "description": data["description"],
        "media_url": data["media_url"],
        "likes": 0,
        "comments": 0,
        "user_id": data["user_id"],
        "org_id": data["org_id"],
        "created_at": datetime.now(),
        "media_type": data["media_type"]
      }
      db.publications.insert_one(pub)
      return jsonify({"message": "success!"}), 200
    except Exception as e:
      return jsonify({"error": str(e)}), 400
  else:
    return jsonify({"error": "Unauthorized"}), 401

@main.route('/<id>', methods=['GET'])
def get_publication(id):
  has_access = Security.verify_token(request.headers)
  if has_access:
    pub  = db.publications.find_one({"_id": ObjectId(id)})
    pub_copy = deepcopy(pub)
    pub_copy["img_org"] = db.organizations.find_one({"_id": ObjectId(pub["org_id"])})["img_src"]
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

@main.route('/like/<id>', methods=['PUT'])
def like_publication(id):
  has_access = Security.verify_token(request.headers)
  if has_access:
    res = db.publications.update_one({"_id": ObjectId(id)}, {"$inc": {"likes": 1}})
    if res.matched_count == 0:
      return jsonify({"error": "Publication not found"}), 404
    else:
      id_user = request.get_json()["user_id"]
      db.users.update_one({"_id": ObjectId(id_user)}, {"$push": {"liked_pubs": id}})
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
      act = db.users.update_one({"_id": ObjectId(request.get_json()["user_id"])}, {"$push": {"disliked_pubs": id}})
      if act.matched_count == 0:
        return jsonify({"error": "User not found"}), 404
      
      return jsonify({"message": "success!"}), 200
  else:
    return jsonify({"error": "Unauthorized"}), 401
  
@main.route('/org/<id>', methods=['GET'])
def get_publications_org(id):
  has_access = Security.verify_token(request.headers)
  if has_access:
    try:
      data = db.publications.find({"org_id": id}).sort("created_at", -1)
      pubs = []
      for pub in data:
        pub_copy = deepcopy(pub)
        org = db.organizations.find_one({"_id": ObjectId(pub["org_id"])})
        if org:
          pub_copy["img_org"] = org["img_src"]
          pubs.append(pub_copy)
        else:
          pass
      res = json_util.dumps(pubs)
      return Response(res, mimetype='application/json'), 200
    except Exception as e:
      return {"error": str(e)}, 400
  else:
    return jsonify({"error": "Unauthorized"}), 401
  
@main.route('/user/<id>', methods=['GET'])
def get_publications_user(id):
  has_access = Security.verify_token(request.headers)
  if has_access:
    try:
      liked_pubs = db.users.find_one({"_id": ObjectId(id)})["liked_pubs"]
      liked_pubs.reverse()
      res = []
      for id_pub in liked_pubs:
        pub = db.publications.find_one({"_id": ObjectId(id_pub)})
        pub["img_org"] = db.organizations.find_one({"_id": ObjectId(pub["org_id"])})["img_src"]
        res.append(pub)
        
      res = json_util.dumps(res)
      return Response(res, mimetype='application/json'), 200
    except Exception as e:
      return {"error": str(e)}, 400
  else:
    return jsonify({"error": "Unauthorized"}), 401