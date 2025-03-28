from fastapi import APIRouter
from app.services import games as game_service
from app.services import teams as team_service
from app.services import players as player_service

router = APIRouter()

@router.get("/today")
def get_games_today():
    """
    Retrieve NBA game results for today (Eastern Time).
    """
    games = game_service.get_games_by_date()
    return games

@router.get("/today/by-team")
def get_team_game_today(team: str):
    """
    Retrieve today's game(s) for a specific team.
    ex: /games/today/by-team?team=GSW
    """
    result = game_service.get_team_game_today(team)
    return result

@router.get("/{date}")
def get_games_by_date(date: str):
    """
    Retrieve NBA game results for a specific date.
    """
    games = game_service.get_games_by_date(date)
    return games

@router.get("/today/user-teams/{email}")
def get_user_team_games(email: str):
    """
    Get today's games for the teams registered by a user.
    """
    games = game_service.get_user_team_games_today(email)
    return games