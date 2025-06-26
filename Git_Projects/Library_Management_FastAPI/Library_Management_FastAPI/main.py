from fastapi import FastAPI
from app.routers import book_router, student_router, issue_router

app = FastAPI(
    title="Library Management API",
    description="A simple Library Management System using FastAPI",
    version="1.0.0"
)

# Include routers
app.include_router(book_router.router, prefix="/api/books")
app.include_router(student_router.router, prefix="/api/students")
app.include_router(issue_router.router, prefix="/api/issued")

@app.get("/")
def root():
    return {"message": "Welcome to the Library Management API"}
