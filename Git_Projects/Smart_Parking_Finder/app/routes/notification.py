from fastapi import APIRouter, Depends
from app.models.notification import NotificationResponse
from app.services.notification_service import NotificationService
from app.utils.auth import get_current_user
from app.database.mongodb import get_database

router = APIRouter()

@router.get("/", response_model=NotificationResponse)
async def get_notifications(current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = NotificationService(db)
    
    notifications = await service.get_user_notifications(current_user["_id"])
    return {"notifications": notifications}
