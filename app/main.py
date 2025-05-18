from app.routers import test_db
from fastapi import FastAPI

app = FastAPI()

app.include_router(test_db.router, tags=["Test DB"])