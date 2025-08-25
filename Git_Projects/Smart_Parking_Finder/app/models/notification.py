from typing import List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    BOOKING = "booking"
    RELEASE = "release"
    CANCELLATION = "cancellation"

class NotificationStatus(str, Enum):
    READ = "read"
    UNREAD = "unread"

class Notification(BaseModel):
    notification_id: str
    type: NotificationType
    message: str
    status: NotificationStatus
    created_at: datetime

class NotificationResponse(BaseModel):
    notifications: List[Notification]
