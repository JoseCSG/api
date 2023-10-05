from flask import Blueprint, request, jsonify

from src.services.models.Publication import Publication
from src.services.models.User import User
from src.services.AuthService import AuthService
from src.utils.Security import Security

main = Blueprint('auth_blueprint', __name__)

@main.route('/', methods=['POST'])
def login():
  print(request.json)
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