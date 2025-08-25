
from fastapi import APIRouter, Header
from app.services.notifications_service import list_notifications
from app.utils.auth import get_bearer_user_id

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=dict)
async def list_notifications_route(Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    data = await list_notifications(user_id)
    return {"notifications": data}
