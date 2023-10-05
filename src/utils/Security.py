from decouple import config
import datetime
import pytz
import jwt

class Security():
  tz = pytz.timezone('America/Bogota')
  secret = config('JWT_KEY')

  @classmethod
  def generate_token(cls, authenticated_user):
    payload = {
      'iat': datetime.datetime.now(tz=cls.tz),
      'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(days=1),
      'username': authenticated_user.username,
      'email': authenticated_user.email
    }
    return jwt.encode(payload, cls.secret, algorithm="HS256")
  
  @classmethod
  def verify_token(cls, headers):
    if 'Authorization' not in headers:
      return False
    header = headers['Authorization']
    encoded_token = header.split(' ')[1]
    try:
      decoded = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
      return decoded
    except jwt.ExpiredSignatureError:
      return False
    except jwt.InvalidTokenError:
      return False