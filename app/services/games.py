from nba_api.live.nba.endpoints import scoreboard

from datetime import datetime
import pytz
import os

from app.core.dynamodb import get_table

def get_today_us_date():
    """
    Returns today's date in US Eastern Time (format: YYYY-MM-DD).
    """
    est = pytz.timezone("US/Eastern")
    now_est = datetime.now(est)
    return now_est.strftime("%Y-%m-%d")

def get_games_by_date(date_str: str = None):
    """
    Retrieves NBA game data for today (nba_api.live only provides today’s games).
    """
    # scoreboard.ScoreBoard() only returns today’s games, so date_str is not used here
    board = scoreboard.ScoreBoard()
    return board.get_dict()["scoreboard"]["games"]

def get_team_game_today(team: str):
    """
    Returns games involving the specified team for today.
    Matches against team abbreviation or full name (case-insensitive).
    """
    games = get_games_by_date()

    team = team.lower()
    filtered_games = [
        g for g in games
        if team in (g["homeTeam"]["teamTricode"].lower(),
                    g["awayTeam"]["teamTricode"].lower(),
                    g["homeTeam"]["teamName"].lower(),
                    g["awayTeam"]["teamName"].lower())
    ]
    return filtered_games

def get_user_team_games_today(email: str):
    """
    Fetches today’s games for the teams registered by the given user.
    """
    table = get_table(os.getenv("USERS_TABLE_NAME", "users"))
    user = table.get_item(Key={"email": email}).get("Item")

    if not user:
        raise ValueError("User not found")

    team_ids = [team["id"] for team in user.get("teams", [])]
    games = get_games_by_date()

    filtered_games = [
        g for g in games
        if g["homeTeam"]["teamId"] in team_ids or g["awayTeam"]["teamId"] in team_ids
    ]
    return filtered_games