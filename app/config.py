from pydantic import BaseConfig


class Settings(BaseConfig):

    secret: str
    jwt_expiration: int = 1
    jwt_key: str = 'secret'


settings = Settings()
