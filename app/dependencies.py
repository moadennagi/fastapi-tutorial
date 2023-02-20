from models import Maker


def get_session():
    try:
        session = Maker()
        yield session
    finally:
        session.close()
