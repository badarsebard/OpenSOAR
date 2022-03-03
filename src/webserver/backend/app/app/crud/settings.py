"""CRUD operations for settings"""
from sqlalchemy.orm import Session
from .. import models, schemas


def get_setting(db_conn: Session, attribute: str = None):
    """read setting value from database"""
    if attribute:
        return (
            db_conn.query(models.SettingsTable)
            .filter(models.SettingsTable.setting == attribute)
            .first()
        )
    return db_conn.query(models.SettingsTable).all()


def set_setting(db_conn: Session, attribute: str, value: str):
    """create or update setting value in database"""
    setting = (
        db_conn.query(models.SettingsTable)
        .filter(models.SettingsTable.setting == attribute)
        .first()
    )
    if setting:
        setting.value = value
        db_conn.commit()
    else:
        setting = models.SettingsTable(
            **(schemas.SettingCreate(setting=attribute, value=value).dict())
        )
        db_conn.add(setting)
        db_conn.commit()
    return db_conn.refresh(setting)
