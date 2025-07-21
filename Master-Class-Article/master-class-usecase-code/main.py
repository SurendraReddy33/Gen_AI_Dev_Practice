from fastapi import FastAPI
from app.routes.prompt_routes import router

app = FastAPI(title = "Master class for vectors, embeddings, token, faiss, MongoDB ", description= "API using GPT2 , sentence embeddings and MOngoDB")

app.include_router(router)

@app.get("/", tags=["Info"])
def root():
    return {"message": "Health Check is working"}

