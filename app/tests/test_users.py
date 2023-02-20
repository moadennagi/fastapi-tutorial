import bcrypt
import jwt
from config import settings
from users.models import User
from users.utils import create_bearer_token


def test_user_password():
    user = User(username='admin', password='admin')
    assert bcrypt.checkpw('admin'.encode(), user.password)


def test_get_current_user():
    ...


def test_create_bearer_token():
    user = User(username='foo', password='foo')
    token = create_bearer_token(user)
    decoded = jwt.decode(token, settings.jwt_key, algorithms=['HS256'])
    assert decoded['sub'] == user.username
    