from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    email: str
    timezone: str = "Asia/Seoul"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()