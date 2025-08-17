from sqlalchemy import create_engine
from models import Base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


# echo=True will log all SQLAlchemy activity—handy for debugging
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

#dependency function for session requests.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
