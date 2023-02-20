import items.router
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_session
from sqlalchemy.orm import Session
from sqlalchemy import select
from users.models import User
from users.schemas import UserCreateSchema
from sqlalchemy.exc import NoResultFound
from users.utils import create_bearer_token

app = FastAPI()

auth_scheme = OAuth2PasswordBearer(tokenUrl='login')


@app.post('/login')
def login(
    data: UserCreateSchema,
    session: Session = Depends(get_session)
):
    # get the user from the database
    stmt = select(User).where(User.username==data.username)
    try:
        user = session.execute(stmt).scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail='Not Found'
        )
    # Create an auth token
    token = create_bearer_token(user)
    return token


@app.get('/')
def home():
    return {'res': 'hello world'}


app.include_router(items.router.router, prefix='/items', tags=['items'])