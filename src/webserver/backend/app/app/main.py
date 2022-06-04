from sqlalchemy import inspect
from sqlalchemy.engine import Inspector
from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import FiefAccessTokenInfo, FiefAsync
from fief_client.integrations.fastapi import FiefAuth

# import os
# import sys
# print(sys.path)
# print(os.getcwd())
# print(os.listdir())
# print(os.listdir("./app"))

from crud.settings import get_setting
from database import create_sessionmaker_engine
from routers import install
from utils import OSoarApp


# fief = FiefAsync(
#     "https://example.fief.dev",
#     "YOUR_CLIENT_ID",
#     "YOUR_CLIENT_SECRET",
# )
#
# scheme = OAuth2AuthorizationCodeBearer(
#     "https://example.fief.dev/authorize",
#     "https://example.fief.dev/api/token",
#     scopes={"openid": "openid", "offline_access": "offline_access"},
# )
#
# auth = FiefAuth(fief, scheme)

s, e = create_sessionmaker_engine()
app = OSoarApp(engine=e, session_maker=s, root_path="/api")


@app.get("/")
def read_root():
    return {}


# @app.get("/user")
# async def get_user(
#     access_token_info: FiefAccessTokenInfo = Depends(
#         auth.authenticated(["openid", "required_scope"])
#     ),
# ):
#     return access_token_info


app.include_router(install.get_install_router(app), prefix="", tags=["install"])


def get_db():
    return_db = app.session_maker()
    try:
        yield return_db
    finally:
        return_db.close()


db = app.session_maker()
INSTALLED = None
inspector: Inspector = inspect(app.engine)
if inspector.has_table("settings"):
    INSTALLED = get_setting(db, "installed")
if INSTALLED and INSTALLED.value == "True":
    install.install_routes(app)
