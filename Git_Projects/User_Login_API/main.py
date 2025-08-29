from fastapi import FastAPI
from app.routes.user_routes import router
from app.routes import user_routes,parking_routes
from seed import seed_initial_data
 
app = FastAPI()

print("Ex")
app.include_router(user_routes.router, prefix="/api/user", tags=["User Management"])


app.include_router(parking_routes.router, prefix="/api/parking", tags=["Parking Management"])

print("ex")




# Run seeding at startup
@app.on_event("startup")
async def startup_event():
    await seed_initial_data()