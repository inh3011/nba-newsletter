from fastapi import FastAPI
from app.api import users, newsletter

app = FastAPI()

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(newsletter.router, prefix="/api/newsletter", tags=["newsletter"])