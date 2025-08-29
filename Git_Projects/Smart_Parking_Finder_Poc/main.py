from fastapi import FastAPI
from app.routes.user_routes import router
from app.routes import user_routes,parking_routes, booking_routes
from seed import seed_initial_data
 
app = FastAPI()

app.include_router(user_routes.router, prefix="/user", tags=["User Management"])

app.include_router(parking_routes.router, prefix="/parking", tags=["Parking Management"])

app.include_router(booking_routes.router, prefix="/booking", tags=["Booking Management"])


# Run seeding at startup
@app.on_event("startup")
async def startup_event():
    await seed_initial_data()