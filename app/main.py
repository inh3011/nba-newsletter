from fastapi import FastAPI
from app.api import users, newsletters, games, teams, players

app = FastAPI()
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(newsletters.router, prefix="/api/newsletters", tags=["newsletters"])
app.include_router(games.router, prefix="/api/games", tags=["games"])
app.include_router(teams.router, prefix="/api/teams", tags=["teams"])
app.include_router(players.router, prefix="/api/players", tags=["players"])