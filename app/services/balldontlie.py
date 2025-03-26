from balldontlie import BalldontlieAPI
from datetime import datetime, timedelta, timezone
import pytz

import os


api = BalldontlieAPI(api_key=os.getenv("BALLDONTLIE_API_KEY", ""))

def get_today_us_date():
    """
    현재 미국 동부 기준 날짜 반환 (YYYY-MM-DD)
    """
    est = pytz.timezone("US/Eastern")
    now_est = datetime.now(est)
    return now_est.date().isoformat()

def get_games_by_date(date_str: str = None):
    """
    주어진 날짜(YYYY-MM-DD)의 NBA 경기 데이터를 조회합니다.
    date_str가 없으면 오늘 날짜 기준으로 조회합니다.
    """
    if not date_str:
        date_str = get_today_us_date()

    response = api.nba.games.list(start_date=date_str, end_date=date_str)
    return response.data

def get_team_list():
    """
    전체 NBA 팀 목록을 반환합니다.
    """
    response = api.nba.teams.list()
    return response.data

def search_players(search: str):
    """
    이름 또는 키워드로 선수 검색합니다.
    """
    response = api.nba.players.list(search=search, per_page=25)
    return response.data

def get_player_stats(player_id: int):
    """
    특정 선수의 경기 스탯을 조회합니다.
    """
    response = api.nba.stats.list(player_ids=[player_id], per_page=10)
    return response.data

def get_team_game_today(team: str):
    """
    오늘 날짜 기준으로 특정 팀의 경기만 필터링
    team: 팀 이름 일부, 약어, 또는 전체 이름
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