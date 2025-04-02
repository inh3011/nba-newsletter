from fastapi import APIRouter
from app.services import players as player_service
from app.models.api import APIResponse

router = APIRouter()

@router.get("/id/{player_id}/stats", response_model=APIResponse[dict])
def get_player_stats_by_id(player_id: int):
    """
    Get recent game stats for a specific player.
    """
    try:
        stats = player_service.get_player_stats_by_id(player_id)
        return APIResponse.success_response(stats, f"Successfully retrieved stats for player {player_id}")
    except Exception as e:
        return APIResponse.error_response(str(e), f"Failed to retrieve stats for player {player_id}")

@router.get("/name/{player_name}/stats", response_model=APIResponse[dict])
def get_player_stats_by_name(player_name: str):
    """
    Get recent game stats for a specific player.
    """
    try:
        stats = player_service.get_player_stats_by_name(player_name)
        return APIResponse.success_response(stats, f"Successfully retrieved stats for player {player_name}")
    except Exception as e:
        return APIResponse.error_response(str(e), f"Failed to retrieve stats for player {player_name}")

@router.get("/search", response_model=APIResponse[list[dict]])
def search_players(search: str):
    """
    Search NBA players by name or keyword.
    """
    try:
        players = player_service.search_players(search)
        return APIResponse.success_response(players, f"Successfully searched for players matching '{search}'")
    except Exception as e:
        return APIResponse.error_response(str(e), f"Failed to search for players matching '{search}'")

