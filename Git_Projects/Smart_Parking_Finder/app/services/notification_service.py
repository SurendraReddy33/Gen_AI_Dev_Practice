from datetime import datetime
import uuid
from app.utils.mail import send_email

class NotificationService:
    def __init__(self, db):
        self.db = db
        self.notifications_collection = db["notifications"]
    
    async def create_notification(self, user_id: str, notification_type: str, message: str, session=None):
        notification_data = {
            "notification_id": f"NOTIF{str(uuid.uuid4())[:8].upper()}",
            "user_id": user_id,
            "type": notification_type,
            "message": message,
            "status": "unread",
            "created_at": datetime.utcnow()
        }
        
        if session:
            await self.notifications_collection.insert_one(notification_data, session=session)
        else:
            await self.notifications_collection.insert_one(notification_data)
        
        return notification_data
    
    async def get_user_notifications(self, user_id: str):
        return await self.notifications_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).to_list(None)


async def create_notification(self, user_id: str, notification_type: str, message: str, session=None):
# Existing code to create notification in the database
       
    # Send email notification
    user = await self.get_user_by_id(user_id)
    if user and user["email"]:
        await send_email(subject="New Notification", recipient=user["email"], body=message)
   