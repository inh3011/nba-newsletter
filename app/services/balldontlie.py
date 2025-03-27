from balldontlie import BalldontlieAPI
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import pytz

import os

load_dotenv()
api = BalldontlieAPI(api_key=os.getenv("BALLDONTLIE_API_KEY"))

def get_today_us_date():
    """
    Returns today's date in US Eastern Time (format: YYYY-MM-DD).
    """
    est = pytz.timezone("US/Eastern")
    now_est = datetime.now(est)
    return now_est.date().isoformat()

def get_games_by_date(date_str: str = None):
    """
    Retrieves NBA game data for the specified date (YYYY-MM-DD).
    If no date is provided, defaults to today's date (US Eastern).
    """
    if not date_str:
        date_str = get_today_us_date()

    response = api.nba.games.list(start_date=date_str, end_date=date_str)
    return response.data

def get_team_list():
    """
    Returns a list of all NBA teams.
    """
    response = api.nba.teams.list()
    return response.data

def get_team_by_id(team_id: int):
    """
    Retrieves NBA team information by team ID.
    """
    response = api.nba.teams.get(team_id)
    return response.data

def search_players(search: str):
    """
    Searches NBA players by name or keyword.
    """
    response = api.nba.players.list(search=search, per_page=25)
    return response.data

def get_player_stats(player_id: int):
    """
    Retrieves recent game stats for a specific player.
    """
    response = api.nba.stats.list(player_ids=[player_id], per_page=10)
    return response.data

def get_team_game_today(team: str):
    """
    Filters today's games and returns only those involving the specified team.

    Args:
        team (str): Team abbreviation (e.g. "GSW"), full name, or partial match.

    Returns:
        list: Games where the specified team is either home or visitor.
    """
    games = get_games_by_date()
    filtered = []

    for game in games:
        if (
            game.home_team.abbreviation.lower() == team.lower()
            or game.visitor_team.abbreviation.lower() == team.lower()
            or game.home_team.full_name.lower() == team.lower()
            or game.visitor_team.full_name.lower() == team.lower()
        ):
            filtered.append(game)

    return filtered