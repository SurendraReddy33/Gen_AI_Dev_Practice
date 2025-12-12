from fastapi import FastAPI
from worker.fetch_news_worker_db import router

app = FastAPI()

app.include_router(router,prefix= "/articles")