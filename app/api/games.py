from fastapi import APIRouter
from app.services import balldontlie

router = APIRouter()

@router.get("/today")
def get_games_today():
    """
    오늘 날짜 기준으로 경기 결과 조회
    """
    games = balldontlie.get_games_by_date()
    return games


@router.get("/{date}")
def get_games_by_date(date: str):
    """
    특정 날짜(YYYY-MM-DD)의 경기 결과 조회
    """
    games = balldontlie.get_games_by_date(date)
    return games


@router.get("/teams")
def get_teams():
    """
    NBA 전체 팀 목록 조회
    """
    teams = balldontlie.get_team_list()
    return teams


@router.get("/players/search")
def search_players(search: str):
    """
    이름 또는 키워드로 선수 검색
    """
    players = balldontlie.search_players(search)
    return players


@router.get("/players/{player_id}/stats")
def get_player_stats(player_id: int):
    """
    특정 선수의 최근 경기 스탯 조회
    """
    stats = balldontlie.get_player_stats(player_id)
    return stats


@router.get("/today/by-team")
def get_team_game_today(team: str):
    """
    오늘 경기 중 특정 팀의 경기만 조회
    ex: /games/today/by-team?team=GSW
    """
    result = balldontlie.get_team_game_today(team)
    return result