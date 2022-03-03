"""Creates connection to the database for use by the API"""
import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


def create_sessionmaker_engine():
    """Creates the actual session and engine objects"""
    connection_string = os.environ.get("CONNECTION_STRING")
    url = make_url(connection_string)
    if url.database is None:
        url = url.set(database="opensoar")
    engine = create_engine(url.render_as_string())
    if not database_exists(engine.url):
        create_database(engine.url)

    return sessionmaker(autocommit=False, autoflush=False, bind=engine), engine


Base = declarative_base()
