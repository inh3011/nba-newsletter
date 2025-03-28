from fastapi import APIRouter
from app.services import teams as team_service

router = APIRouter()

@router.get("")
def get_teams():
    """
    Get the list of all NBA teams.
    """
    teams = team_service.get_team_list()
    return teams

@router.get("/{team_name}")
def get_team(team_name: str):
    """
    Get the list of all NBA teams.
    """
    teams = team_service.get_team_by_name(team_name)
    return teams