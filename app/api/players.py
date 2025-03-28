from fastapi import APIRouter
from app.services import players as player_service

router = APIRouter()

@router.get("/id/{player_id}/stats")
def get_player_stats_by_id(player_id: int):
    """
    Get recent game stats for a specific player.
    """
    stats = player_service.get_player_stats_by_id(player_id)
    return stats

@router.get("/name/{player_name}/stats")
def get_player_stats_by_name(player_name: str):
    """
    Get recent game stats for a specific player.
    """
    stats = player_service.get_player_stats_by_name(player_name)
    return stats

@router.get("/search")
def search_players(search: str):
    """
    Search NBA players by name or keyword.
    """
    players = player_service.search_players(search)
    return players

