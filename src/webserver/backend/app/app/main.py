from sqlalchemy import inspect
from sqlalchemy.engine import Inspector

from .crud import get_setting
from .database import create_sessionmaker_engine
from .routers import install
from .utils import OSoarApp

s, e = create_sessionmaker_engine()
app = OSoarApp(engine=e, session_maker=s, root_path="/api")


@app.get("/")
def read_root():
    return {'routes': [r.path for r in app.routes]}


app.include_router(install.get_install_router(app), prefix="", tags=["install"])


def get_db():
    return_db = app.session_maker()
    try:
        yield return_db
    finally:
        return_db.close()


db = app.session_maker()
installed = None
inspector: Inspector = inspect(app.engine)
if inspector.has_table("settings"):
    installed = get_setting(db, "installed")
if installed and installed.value == "True":
    install.install_routes(app, get_db)
