from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str

class UserOut(BaseModel):
    email: str
    created_at: datetime
    updated_at: datetime