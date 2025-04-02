from fastapi import APIRouter
from app.services import games as game_service
from app.services import teams as team_service
from app.services import players as player_service
from app.models.api import APIResponse

router = APIRouter()

@router.get("/today", response_model=APIResponse[list[dict]])
def get_games_today():
    """
    Retrieve NBA game results for today (Eastern Time).
    """
    try:
        games = game_service.get_games_by_date()
        return APIResponse.success_response(games, "Successfully retrieved today's games")
    except Exception as e:
        return APIResponse.error_response(str(e), "Failed to retrieve today's games")

@router.get("/today/by-team", response_model=APIResponse[dict])
def get_team_game_today(team: str):
    """
    Retrieve today's game(s) for a specific team.
    ex: /games/today/by-team?team=GSW
    """
    try:
        result = game_service.get_team_game_today(team)
        return APIResponse.success_response(result, f"Successfully retrieved today's game for {team}")
    except Exception as e:
        return APIResponse.error_response(str(e), f"Failed to retrieve today's game for {team}")

@router.get("/{date}", response_model=APIResponse[list[dict]])
def get_games_by_date(date: str):
    """
    Retrieve NBA game results for a specific date.
    """
    try:
        games = game_service.get_games_by_date(date)
        return APIResponse.success_response(games, f"Successfully retrieved games for {date}")
    except Exception as e:
        return APIResponse.error_response(str(e), f"Failed to retrieve games for {date}")

@router.get("/today/user-teams/{email}", response_model=APIResponse[list[dict]])
def get_user_team_games(email: str):
    """
    Get today's games for the teams registered by a user.
    """
    try:
        games = game_service.get_user_team_games_today(email)
        return APIResponse.success_response(games, "Successfully retrieved user's team games")
    except Exception as e:
        return APIResponse.error_response(str(e), "Failed to retrieve user's team games")