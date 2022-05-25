"""Router for installation endpoints"""
import os
import signal
import sys

from fastapi import Depends, Request, HTTPException, status, APIRouter
from fastapi_users import FastAPIUsers, BaseUserManager
from fastapi_users.authentication import (
    JWTStrategy,
    BearerTransport,
    AuthenticationBackend,
)
from fastapi_users.manager import UserAlreadyExists, InvalidPasswordException
from fastapi_users.router.common import ErrorCode
from sqlalchemy import inspect
from sqlalchemy.engine import Inspector
from sqlalchemy.orm import Session

from .. import schemas, crud, adapter
from ..utils import OSoarApp
from ..database import Base
from .incidents import get_incidents_router

secret = os.environ.get("AUTH_BACKEND_SECRET")
if not secret:
    sys.exit(1)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """Return json web token strategy"""
    return JWTStrategy(secret=secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(BaseUserManager[schemas.UserCreate, schemas.UserDB]):
    """Fastapi Users user manager"""

    user_db_model = schemas.UserDB
    reset_password_token_secret = secret
    verification_token_secret = secret


def install_routes(app: OSoarApp, get_db):
    """Install routers to the app"""

    def get_user_db():
        yield adapter.SQLAlchemyORMUserDatabase(
            schemas.UserDB,
            app.session_maker(),
        )

    async def get_user_manager(
        user_db: adapter.SQLAlchemyORMUserDatabase = Depends(get_user_db),
    ):
        yield UserManager(user_db)

    fastapi_users = FastAPIUsers(
        get_user_manager,
        [auth_backend],
        schemas.User,
        schemas.UserCreate,
        schemas.UserUpdate,
        schemas.UserDB,
    )

    app.users = fastapi_users

    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
    )
    app.include_router(
        fastapi_users.get_register_router(),
        prefix="/auth",
    )
    app.include_router(
        fastapi_users.get_users_router(),
        prefix="/users",
    )
    app.include_router(get_incidents_router(app))

    def read_users(
        session: Session = Depends(get_db),
    ):
        return crud.read_users(session)

    app.add_api_route(
        "/users",
        read_users,
        dependencies=[Depends(fastapi_users.current_user(active=True))],
    )


def get_install_router(app: OSoarApp):
    """Router for the /install endpoints"""
    local_session_maker, engine = app.session_maker, app.engine

    router = APIRouter()

    def get_db():
        return_db = local_session_maker()
        try:
            yield return_db
        finally:
            return_db.close()

    @router.post("/install")
    async def install(request: Request, root_user: schemas.UserCreate):
        # create initial tables
        Base.metadata.create_all(engine)

        db_conn = local_session_maker()
        installed = None
        inspector: Inspector = inspect(engine)
        if inspector.has_table("settings"):
            installed = crud.get_setting(db_conn, "installed")
        if not installed or installed.value != "True":
            # create initial user
            try:
                user_manager = UserManager(
                    adapter.SQLAlchemyORMUserDatabase(
                        schemas.UserDB,
                        app.session_maker(),
                    )
                )
                await user_manager.create(root_user, safe=True, request=request)
            except UserAlreadyExists:
                # todo: don't raise this exception, note it in the response
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
                )
            except InvalidPasswordException as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                        "reason": e.reason,
                    },
                )

            # set as installed
            crud.set_setting(db_conn, "installed", "True")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="INSTALLATION_IS_ALREADY_COMPLETE",
            )
        fastapi_users = install_routes(app, get_db)
        os.kill(1, signal.SIGHUP)

    @router.get("/install")
    async def installation_status(db: Session = Depends(get_db)):
        response = {"status": 0}
        inspector: Inspector = inspect(engine)
        if inspector.has_table("settings"):
            installed = crud.get_setting(db, "installed")
            if installed and installed.value == "True":
                response["status"] = 1
        return response

    return router
