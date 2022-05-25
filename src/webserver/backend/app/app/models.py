"""Models for the database tables"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship

from .database import Base


# pylint: disable=too-few-public-methods
class UserTable(Base):
    """Table for storing users"""

    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    display_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    incidents = relationship("IncidentTable", back_populates="owner")


class IncidentTable(Base):
    """Table for storing incidents"""

    __tablename__ = "incident"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    owner = relationship("UserTable", back_populates="incidents")
    data = Column(JSON, index=True)


class SettingsTable(Base):
    """Table for racking settings of the app"""

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    setting = Column(String, index=True)
    value = Column(String, index=True)
