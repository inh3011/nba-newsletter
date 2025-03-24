from pydantic import BaseModel
from datetime import date, datetime

class GameStat(BaseModel):
    game_id: str
    date: date
    team: str
    opponent: str
    player_name: str
    pts: int
    reb: int
    ast: int
    result: str  # 'W' or 'L'
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()