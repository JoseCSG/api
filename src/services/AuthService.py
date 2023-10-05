from .models.User import User
from src.db.db import db
class AuthService():
  @classmethod
  def login(cls, _user):
    try:
      authenticated_user = None
      aux = db.users.find_one({"username": _user.username})
      print(_user.username)
      print(_user.password)
      print(aux)
      if aux != None and aux["password"] == _user.password:
        authenticated_user = User(aux["_id"], aux["username"], aux["email"], aux["password"])
      return authenticated_user
    except Exception as e:
      raise Exception("An error ocurred while trying to login the user: " + str(e))