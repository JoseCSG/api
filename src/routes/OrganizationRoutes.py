from flask import Blueprint, request, jsonify, Response
from src.utils.Security import Security
from src.db.db import db
from bson import ObjectId, json_util
main = Blueprint('organization_blueprint', __name__)

@main.route('/', methods=["GET"])
def get_orgs():
  try:
    data = db.organizations.find()
    res = json_util.dumps(data)
    return Response(res, mimetype='application/json'), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 401

@main.route('/<id>', methods=["GET"])
def get_organization(id):
  try:
    res = db.organizations.find_one({"_id": ObjectId(id)})
    org = json_util.dumps(res)
    return Response(org, mimetype='application/type'), 200
  except Exception as e:
    return jsonify({"error": "Organization not found"}), 401

@main.route('/add', methods=["POST"])
def add_organization():
  try:
    data = request.get_json()
    print(data)
    org = {
      "name": data['name'],
      "description": data['description'],
      "number": data['number']
    }
    print(org)
    db.organizations.insert_one(org)
    return jsonify({"message": "success"}), 200
  except:
    return jsonify({"error": "Error creating the organization"})