
from app.config.db import get_db
from app.models import NOTIFS_COLL

async def list_notifications(user_id: str) -> list[dict]:
    db = get_db()
    return await db[NOTIFS_COLL].find({"user_id": user_id}).sort("created_at", -1).to_list(None)
