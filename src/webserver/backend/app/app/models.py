import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

from database import Base


# pylint: disable=too-few-public-methods
class UserTable(Base):
    """Table for storing users"""

    __tablename__ = "user"

    id = Column(
        UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4
    )
    email = Column(String, unique=True, index=True)
    display_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    incidents = relationship("IncidentTable", back_populates="owner")


class IncidentTable(Base):
    """Table for storing incidents"""

    __tablename__ = "incident"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(UUIDType(binary=False), ForeignKey("user.id"))

    owner = relationship("UserTable", back_populates="incidents")
    data = Column(JSON, index=True)


class SettingsTable(Base):
    """Table for racking settings of the app"""

    __tablename__ = "settings"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    setting = Column(String, index=True)
    value = Column(String, index=True)
