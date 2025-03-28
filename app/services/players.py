from nba_api.stats.static import players
from nba_api.live.nba.endpoints import boxscore
from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime
import pytz

def search_players(search: str):
    """
    Search NBA players by full name.
    Returns a list of player dictionaries.
    """
    return players.find_players_by_full_name(search)

def get_today_us_date():
    est = pytz.timezone("US/Eastern")
    return datetime.now(est).strftime("%Y-%m-%d")

def get_today_game_ids():
    board = scoreboard.ScoreBoard()
    games = board.get_dict()["scoreboard"]["games"]
    return [game["gameId"] for game in games]

def get_player_stats_by_id(player_id: int):
    """
    Retrieves today's box score stats for a specific player by their ID.
    """
    for game_id in get_today_game_ids():
        game_box = boxscore.BoxScore(game_id).get_dict()["game"]

        players = game_box["homeTeam"]["players"] + game_box["awayTeam"]["players"]

        for player in players:
            if int(player["personId"]) == player_id:
                stats = player["statistics"]
                return {
                    "name": player["name"],
                    "starter": player["starter"],
                    "points": stats["points"],
                    "rebounds": stats["rebounds"],
                    "assists": stats["assists"],
                    "minutes": stats["minutes"]
                }

    return {"message": "No stats found for the player today."}

def get_player_stats_by_name(player_name: str):
    """
    Retrieves today's box score stats for a player matching the given name.
    """
    player_name = player_name.lower()

    for game_id in get_today_game_ids():
        game_box = boxscore.BoxScore(game_id).get_dict()["game"]
        players = game_box["homeTeam"]["players"] + game_box["awayTeam"]["players"]

        for player in players:
            if player_name in player["name"].lower():
                stats = player["statistics"]
                return {
                    "name": player["name"],
                    "starter": player["starter"],
                    "points": stats["points"],
                    "rebounds": stats["rebounds"],
                    "assists": stats["assists"],
                    "minutes": stats["minutes"]
                }

    return {"message": "No stats found for the player today."}