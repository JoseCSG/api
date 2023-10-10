from flask import Blueprint, request, jsonify, Response
from src.utils.Security import Security
from src.db.db import db
from bson import ObjectId, json_util
main = Blueprint('comment_blueprin', __name__)

@main.route('/<id>', methods=["GET"])
def get_orgs(id):
  try:
    data = db.comments.find({"publication_id": ObjectId(id)}).sort({"created_at": -1}).limit(5)
    for comment in data:
      user = db.users.find_one({"_id": ObjectId(comment['user_id'])})
      comment['user'] = user
    res = json_util.dumps(data)
    return Response(res, mimetype='application/json'), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 401
