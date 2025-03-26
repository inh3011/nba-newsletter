from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Team(BaseModel):
    id: int
    name: str
    abbreviation: str

class Player(BaseModel):
    id: int
    name: str

class UserCreate(BaseModel):
    email: str

class UserOut(BaseModel):
    email: str
    teams: Optional[List[Team]] = []
    players: Optional[List[Player]] = []
    created_at: datetime
    updated_at: datetime