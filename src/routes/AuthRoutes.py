from flask import Blueprint, request, jsonify

from src.services.models.Publication import Publication
from src.services.models.User import User
from src.services.AuthService import AuthService
from src.utils.Security import Security
from src.db.db import db

main = Blueprint('auth_blueprint', __name__)

@main.route('/', methods=['POST'])
def login():
  username = request.json['username']
  password = request.json['password']
  if not username:
    return jsonify({"error": "Missing username or password"}), 400
  
  _user = User(0, username, "email@outlook.com", password)
  auth_user = AuthService.login(_user)
  if auth_user != None:
    encoded_jwt = Security.generate_token(auth_user)
    return jsonify({"token": encoded_jwt, "message": "success!"}), 200
  else: 
    return jsonify({"error": "Invalid username or password"}), 401
  
@main.route('/sign-up/user', methods=['POST'])
def signup():
  try:
    data = {
      "name": request.json["name"],
      "last_name": request.json['last_name'],
      "email": request.json['email'],
      "number": request.json['number'],
      "password": request.json['password']
    }
    res = db.users.insert_one(data)
    return jsonify({"success": "User created succesfully"}), 200
  except Exception as e:
    return jsonify({"error": "Invalid params", "error_msg": e.args}), 401
