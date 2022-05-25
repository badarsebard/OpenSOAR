"""CRUD operations for users outside fastapi-users endpoints"""
from sqlalchemy.orm import Session
from .. import models


def read_users(db_conn: Session):
    """get all users"""
    return db_conn.query(models.UserTable).all()
