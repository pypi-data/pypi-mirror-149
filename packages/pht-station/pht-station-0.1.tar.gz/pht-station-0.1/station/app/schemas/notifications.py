from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class DBSchema(BaseModel):
    class Config:
        orm_mode = True

class NotificationBase(BaseModel):
    topic: str
    message: str
    target_user: Optional[str] = "all"


class NotificationCreate(NotificationBase):
     pass


class NotificationUpdate(NotificationBase):
    is_read: bool


class Notification(DBSchema):
    id: int
    message: str
    topic: Optional[str] = "trains"
    target_user: Optional[str] = "all"


