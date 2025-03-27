from fastapi import APIRouter
from app.services import balldontlie

router = APIRouter()

@router.get("/today")
def get_games_today():
    """
    Retrieve NBA game results for today (Eastern Time).
    """
    games = balldontlie.get_games_by_date()
    return games


@router.get("/{date}")
def get_games_by_date(date: str):
    """
    Retrieve NBA game results for a specific date.
    """
    games = balldontlie.get_games_by_date(date)
    return games


@router.get("/teams")
def get_teams():
    """
    Get the list of all NBA teams.
    """
    teams = balldontlie.get_team_list()
    return teams


@router.get("/players/search")
def search_players(search: str):
    """
    Search NBA players by name or keyword.
    """
    players = balldontlie.search_players(search)
    return players


@router.get("/players/{player_id}/stats")
def get_player_stats(player_id: int):
    """
    Get recent game stats for a specific player.
    """
    stats = balldontlie.get_player_stats(player_id)
    return stats


@router.get("/today/by-team")
def get_team_game_today(team: str):
    """
    Retrieve today's game(s) for a specific team.
    ex: /games/today/by-team?team=GSW
    """
    result = balldontlie.get_team_game_today(team)
    return result