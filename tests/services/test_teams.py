from app.services.teams import get_team_by_name
from app.services.teams import get_team_list
from nba_api.stats.static import teams

class TestTeams:

    def test_get_team_by_name_1(self):
        """
        Test that get_team_by_name returns the correct team information when given a valid team name.
        """
        team_name = "Los Angeles Lakers"
        result = get_team_by_name(team_name)
        assert result is not None
        assert len(result) == 1
        assert result[0]['full_name'] == team_name
        assert 'id' in result[0]
        assert 'abbreviation' in result[0]

    def test_get_team_by_name_nonexistent_team(self):
        """
        Test that attempting to get a team by a non-existent name returns an empty list.
        """
        result = get_team_by_name("Nonexistent Team")
        assert result == [], "Expected an empty list for a non-existent team name"

    def test_get_team_list_1(self):
        """
        Test that get_team_list() returns the list of all NBA teams.

        This test verifies that the get_team_list function correctly calls
        teams.get_teams() and returns its result without modification.
        """
        expected_teams = teams.get_teams()
        actual_teams = get_team_list()
        assert actual_teams == expected_teams, "get_team_list() should return the result of teams.get_teams()"

    def test_get_team_list_no_teams_available(self):
        """
        Test the behavior of get_team_list when no teams are available from the API.
        This tests the edge case where the API returns an empty list of teams.
        """
        # Mock the teams.get_teams() to return an empty list
        original_get_teams = teams.get_teams
        teams.get_teams = lambda: []

        try:
            result = get_team_list()
            assert len(result) == 0, "Expected an empty list when no teams are available"
        finally:
            # Restore the original function
            teams.get_teams = original_get_teams
