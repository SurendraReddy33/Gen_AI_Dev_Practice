from fastapi import FastAPI
from app.services.user_routes import router
 
app = FastAPI()
 
# router
app.include_router(router, prefix="/api/user", tags=["User Management"])