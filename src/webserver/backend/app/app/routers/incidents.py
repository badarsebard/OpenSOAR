"""Router for handling incident endpoints"""
from typing import Dict, Union, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, crud


def get_incidents_router(app):
    """Produce router to be included by app"""
    local_session_maker, _ = app.session_maker, app.engine

    router = APIRouter()

    def get_db():
        return_db = local_session_maker()
        try:
            yield return_db
        finally:
            return_db.close()

    @router.get(
        "/incidents",
        response_model=Dict[str, Union[List[schemas.IncidentRead], int]],
        # dependencies=[Depends(app.users.current_user(active=True))],
    )
    def read_incidents(
        skip: int = 0,
        limit: int = 10,
        query_filter: str = None,
        db_conn: Session = Depends(get_db),
    ):
        return crud.get_incidents(
            db_conn, skip=skip, limit=limit, query_filter=query_filter
        )

    @router.post(
        "/incidents",
        response_model=schemas.Incident,
        # dependencies=[Depends(app.users.current_user(active=True))],
    )
    def create_incident(
        incident: schemas.IncidentCreate,
        db_conn: Session = Depends(get_db),
    ):
        return crud.create_incident(db_conn, incident)

    # @router.get("/incidents/stream")
    # async def read_incidents_from_stream(
    #     request: Request,
    #     db: Session = Depends(get_db),
    #     user: schemas.User = Depends(app.users.current_user(active=True)),
    # ):
    #     incident_generator = incident_event_generator(db, request)
    #     return EventSourceResponse(incident_generator)

    return router
