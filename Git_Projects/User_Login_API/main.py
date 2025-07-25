from fastapi import FastAPI
from app.services import user_routes
 
app = FastAPI()
 
app.include_router(user_routes.router, prefix="/api/v1", tags=["User Auth"])