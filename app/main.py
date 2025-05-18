from app.routers import test_db, auth, protected
from fastapi import FastAPI

app = FastAPI()

app.include_router(test_db.router, tags=["Test DB"])

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(protected.router, tags=["Protected"])
