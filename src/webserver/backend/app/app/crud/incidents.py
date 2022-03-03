"""CRUD operations for incidents"""
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas


def get_incidents(
    db_conn: Session, skip: int = 0, limit: int = 10, query_filter: str = None
):
    """get incidents based on parameters"""
    if query_filter:
        incidents = (
            db_conn.query(models.IncidentTable)
            .filter(query_filter)
            .options(joinedload(models.IncidentTable.owner))
            .order_by(models.IncidentTable.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        incidents = (
            db_conn.query(models.IncidentTable)
            .options(joinedload(models.IncidentTable.owner))
            .order_by(models.IncidentTable.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    incidents = [
        {**incident.__dict__, "owner": incident.owner} for incident in incidents
    ]
    total = db_conn.query(models.IncidentTable).count()
    return {"incidents": incidents, "total": total}


def get_user_incidents(db_conn: Session, user_id: int, skip: int = 0, limit: int = 10):
    """get incidents for specified user based on parameters"""
    incidents = (
        db_conn.query(models.IncidentTable)
        .filter(models.IncidentTable.owner_id == user_id)
        .options(joinedload(models.IncidentTable.owner))
        .order_by(models.IncidentTable.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    incidents = [
        {**incident.__dict__, "owner": incident.owner} for incident in incidents
    ]
    total = db_conn.query(models.IncidentTable).count()
    return {"incidents": incidents, "total": total}


def create_incident(db_conn: Session, incident: schemas.IncidentCreate):
    """create an incident"""
    db_incident = models.IncidentTable(**incident.dict())
    db_conn.add(db_incident)
    db_conn.commit()
    db_conn.refresh(db_incident)
