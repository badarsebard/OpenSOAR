from typing import List, Optional

from pydantic import BaseModel, UUID4, EmailStr


class IncidentBase(BaseModel):
    title: str
    status: Optional[str] = None
    description: Optional[str] = None


class Incident(IncidentBase):
    id: int
    owner_id: UUID4

    class Config:
        orm_mode = True


class User(BaseModel):
    id: Optional[UUID4] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    incidents: Optional[List[Incident]]
    display_name: Optional[str]
    email: EmailStr

    class Config:
        orm_mode = True


class IncidentCreate(IncidentBase):
    owner_id: UUID4


class IncidentRead(Incident):
    owner: User


class SettingBase(BaseModel):
    setting: str
    value: str


class SettingCreate(SettingBase):
    pass


class Setting(SettingBase):
    id: str

    class Config:
        orm_mode = True
