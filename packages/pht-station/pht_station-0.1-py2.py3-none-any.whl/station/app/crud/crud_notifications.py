from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from .base import CRUDBase

from station.app.models.notification import Notification
from station.app.schemas.notifications import NotificationCreate, NotificationUpdate



class CRUDNotifications(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):

    def read_notifications_for_user(self, db: Session, user: str) -> List[Notification]:
        return db.query(Notification).filter(Notification.target_user == user).all()



notifications = CRUDNotifications(Notification)
