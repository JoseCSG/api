from flask import Blueprint, request, jsonify, Response
from src.utils.Security import Security
from src.db.db import db
from bson import ObjectId, json_util
main = Blueprint('organization_blueprint', __name__)

@main.route('/<id_user>', methods=["GET"])
def get_orgs(id_user):
  try:
    #find organizations that the user has tags in common
    tags_by_user = db.users.find_one({"_id": ObjectId(id_user)})
    res = []
    for tag in tags_by_user['tags']:
      orgs = db.organizations.find({"tags": tag})
      for org in orgs:
        if org not in res:
          res.append(org)
    response = [] 
    for org in res:
      pubs = db.publications.find({"org_id": str(org['_id'])}).sort("likes", -1).limit(5)
      response.append({
        "org": org,
        "pubs": pubs
      })
    return Response(json_util.dumps(response), mimetype='application/type'), 200

  except Exception as e:
    return jsonify({"error": str(e)}), 401

@main.route('/name/<name>', methods=["GET"])
def get_orgs_name(name):
  try:
    print("Al inicio de la funcion")
    regex_pattern = f".*{name}.*"
    query = { "name": { "$regex": regex_pattern, "$options": "i" } }
    res = db.organizations.find(query)
    if not res:
      return jsonify({"error": "Organization not found"}), 401
    print("Despues de hacer el query")
    response = [] 
    for org in res:
      pubs = db.publications.find({"org_id": str(org['_id'])}).sort("likes", -1).limit(5)
      response.append({
        "org": org,
        "pubs": pubs
      })
    print(response)
    return Response(json_util.dumps(response), mimetype='application/type'), 200

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
      "number": data['number'],
      "img_url": data['img_url'],
    }
    print(org)
    db.organizations.insert_one(org)
    return jsonify({"message": "success"}), 200
  except:
    return jsonify({"error": "Error creating the organization"})

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
