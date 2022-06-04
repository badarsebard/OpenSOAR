from typing import Type, Optional, TypeVar
from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result
from src.webserver.backend.app.app import models, schemas

from fastapi_users.db.base import BaseUserDatabase

UD = TypeVar("UD", bound=schemas.UserDB)


class NotSetOAuthAccountTableError(Exception):
    """
    OAuth table was not set in DB adapter but was needed.
    Raised when trying to create/update a user with OAuth accounts set
    but no table were specified in the DB adapter.
    """

    pass


class SQLAlchemyORMUserDatabase(BaseUserDatabase[UD]):
    database: Session

    def __init__(
        self, user_db_schema: Type[UD], database: Session, oauth_accounts=None
    ):
        super().__init__(user_db_schema)
        self.database = database
        self.oauth_accounts = oauth_accounts

    async def get(self, user_id: UUID4) -> Optional[UD]:
        user: Result = (
            self.database.query(models.UserTable)
            .filter(models.UserTable.id == user_id)
            .first()
        )
        return schemas.UserDB(**user.__dict__) if user else None

    async def get_by_email(self, email: str) -> Optional[UD]:
        user = (
            self.database.query(models.UserTable)
            .filter(models.UserTable.email == email)
            .first()
        )
        return schemas.UserDB(**user.__dict__) if user else None

    async def get_by_oauth_account(self, oauth: str, account_id: str) -> Optional[UD]:
        if self.oauth_accounts is not None:
            return
        raise NotSetOAuthAccountTableError()

    async def create(self, user: UD) -> UD:
        user_dict = user.dict(exclude_none=True)
        db_user = models.UserTable(**user_dict)

        number_of_users = self.database.query(models.UserTable).count()
        if number_of_users == 0:
            db_user.is_superuser = True
            user.is_superuser = True

        self.database.add(db_user)
        self.database.commit()
        return user

    async def update(self, user: UD) -> UD:
        user_dict = user.dict(exclude_none=True)
        db_user = models.UserTable(**user_dict)
        self.database.merge(db_user)
        self.database.commit()
        return user

    async def delete(self, user: UD) -> None:
        user_dict = user.dict(exclude_none=True)
        db_user = (
            self.database.query(models.UserTable)
            .filter(models.UserTable.id == user_dict["id"])
            .first()
        )
        self.database.delete(db_user)
        self.database.commit()
