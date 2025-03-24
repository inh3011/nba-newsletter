from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class UserWatchlist(BaseModel):
    user_id: str
    type: Literal["team", "player"]
    name: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()