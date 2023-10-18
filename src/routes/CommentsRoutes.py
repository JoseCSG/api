from flask import Blueprint, request, jsonify, Response
from datetime import datetime
from src.db.db import db
from bson import ObjectId, json_util
main = Blueprint('comment_blueprint', __name__)


@main.route('/', methods=["GET"])
def get_comments():
  try:
    comments = db.comments.find().sort({"created_at": -1}).limit(5)
    comments = json_util.dumps(comments)
    return Response(comments, mimetype='application/json'), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 401

@main.route('/<id>', methods=["GET"])
def get_comments_pub(id):
  try:
    comments = db.comments.find({"publication_id": ObjectId(id)}).limit(5)
    res = json_util.dumps(comments)
    print(res)
    return Response(res, mimetype='application/json'), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 401

@main.route('/add/<id>', methods=["POST"])
def add_comment(id):
  try:
    data = request.get_json()
    if not data['comment'] or not data['user_id']:
      return jsonify({"error": "Data not completed"})
    user = db.users.find_one({"_id": ObjectId(data["user_id"])})
    comment = {
      "comment": data["comment"],
      "name": user["name"],
      "likes": 0,
      "user_id": data["user_id"],
      "publication_id": ObjectId(id),
      "created_at": datetime.now(),
      "img_url": user["img_url"]
    }
    db.comments.insert_one(comment)
    db.publications.update_one({"_id": ObjectId(id)}, {"$inc": {"comments": 1}})
    return jsonify({"message": "success!"}), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 401

@main.route('/like/<id_like>', methods=["PATCH"])
def like_comment(id_like):
  try:
    db.comments.update_one({"_id": ObjectId(id_like)}, {"$inc": {"likes": 1}})
    return jsonify({"message": "success!"}), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 401
  
@main.route('/dislike/<id_dislike>', methods=["PATCH"])
def dislike_comment(id_dislike):
  try:
    db.comments.update_one({"_id": ObjectId(id_dislike)}, {"$inc": {"likes": -1}})
    return jsonify({"message": "success!"}), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 401