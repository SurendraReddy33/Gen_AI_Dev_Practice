from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, parking, booking, notification
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.config import settings

app = FastAPI(
    title="Smart Parking Finder API",
    description="API for managing parking lots, bookings, and user accounts",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(parking.router, prefix="/parkings", tags=["Parking"])
app.include_router(booking.router, prefix="/bookings", tags=["Booking"])
app.include_router(notification.router, prefix="/notifications", tags=["Notifications"])

# Database events
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    print("Disconnected from MongoDB")

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Parking Finder API"}
