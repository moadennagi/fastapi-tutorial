import jwt
from datetime import datetime, timedelta
from users.models import User
from config import settings


def create_bearer_token(user: User) -> str:
    "Return a jwt token"
    payload = {'sub': user.username, 'iat': datetime.utcnow(),
               'exp': datetime.utcnow() + timedelta(minutes=settings.jwt_expiration)}
    token = jwt.encode(payload, settings.jwt_key)
    return token
