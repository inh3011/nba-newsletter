from fastapi import APIRouter
from app.services import teams as team_service
from app.models.api import APIResponse

router = APIRouter()

@router.get("", response_model=APIResponse[list[dict]])
def get_teams():
    """
    Get the list of all NBA teams.
    """
    try:
        teams = team_service.get_team_list()
        return APIResponse.success_response(teams, "Successfully retrieved teams list")
    except Exception as e:
        return APIResponse.error_response(str(e), "Failed to retrieve teams list")

@router.get("/{team_name}", response_model=APIResponse[dict])
def get_team(team_name: str):
    """
    Get the list of all NBA teams.
    """
    try:
        teams = team_service.get_team_by_name(team_name)
        return APIResponse.success_response(teams, f"Successfully retrieved team details for {team_name}")
    except Exception as e:
        return APIResponse.error_response(str(e), f"Failed to retrieve team details for {team_name}")