from fastapi import FastAPI
from app.services.user_routes import router
 
app = FastAPI()
 
app.include_router(router, prefix="/api/v1", tags=["User Auth"])