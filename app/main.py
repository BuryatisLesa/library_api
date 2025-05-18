from app.routers import test_db, auth, protected, books, readers
from fastapi import FastAPI

app = FastAPI()

app.include_router(test_db.router, tags=["Test DB"])

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(protected.router, tags=["Protected"])

app.include_router(books.router, tags=["Books"])

app.include_router(readers.router, tags=["Readers"])
