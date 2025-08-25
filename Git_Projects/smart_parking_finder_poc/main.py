
from fastapi import FastAPI
from app.routes.users_routes import router as users_router
from app.routes.parkings_routes import router as parkings_router
from app.routes.bookings_routes import router as bookings_router
from app.routes.notifications_routes import router as notifications_router

app = FastAPI(title="Smart Parking Finder POC", version="1.0.0")

app.include_router(users_router)
app.include_router(parkings_router)
app.include_router(bookings_router)
app.include_router(notifications_router)

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "service": "smart-parking-finder"}
