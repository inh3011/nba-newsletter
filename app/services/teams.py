from nba_api.stats.static import teams

def get_team_list():
    """
    Returns a list of all NBA teams.
    """
    return teams.get_teams()

def get_team_by_name(team_name: str):
    """
    Retrieves NBA team information by team ID.
    """
    team = teams.find_teams_by_full_name(team_name)
    return team