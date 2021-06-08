from typing import Final
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.settings import settings
from backend.common.utils import get_conn_str, is_development

SQLALCHEMY_DATABASE_URL: Final[str] = get_conn_str(
    settings.postgres_protocol,
    settings.postgres_host,
    settings.postgres_port,
    settings.postgres_username,
    settings.postgres_password,
    settings.postgres_db
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=is_development(),
    echo_pool='debug' if is_development() else 'error'
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
