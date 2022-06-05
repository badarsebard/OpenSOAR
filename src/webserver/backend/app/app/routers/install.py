"""Router for installation endpoints"""
import os
import signal

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import inspect
from sqlalchemy.engine import Inspector
from sqlalchemy.orm import Session

from crud.settings import get_setting, set_setting
from utils import OSoarApp
from database import Base
from routers.incidents import get_incidents_router


def install_routes(app: OSoarApp):
    """Install routers to the app"""
    app.include_router(get_incidents_router(app))


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
    async def install():
        # create initial tables
        Base.metadata.create_all(engine)

        db_conn = local_session_maker()
        installed = None
        inspector: Inspector = inspect(engine)
        if inspector.has_table("settings"):
            installed = get_setting(db_conn, "installed")
        if not installed or installed.value != "True":
            # create initial user

            # set as installed
            set_setting(db_conn, "installed", "True")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="INSTALLATION_IS_ALREADY_COMPLETE",
            )
        os.kill(1, signal.SIGHUP)

    @router.get("/install")
    async def installation_status(db: Session = Depends(get_db)):
        response = {"status": 0}
        inspector: Inspector = inspect(engine)
        if inspector.has_table("settings"):
            installed = get_setting(db, "installed")
            if installed and installed.value == "True":
                response["status"] = 1
        return response

    return router
