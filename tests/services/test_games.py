import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest
import pytz
from nba_api.live.nba.endpoints import scoreboard

from app.services.games import get_games_by_date
from app.services.games import get_team_game_today
from app.services.games import get_today_us_date
from app.services.games import get_user_team_games_today


class TestGames(unittest.TestCase):

    def test_get_games_by_date_ignores_input(self):
        """
        Test that get_games_by_date ignores the input date_str parameter.
        This is an edge case where the method accepts an input but doesn't use it.
        """
        # Call the method with a non-None date_str
        result_with_date = get_games_by_date("2023-01-01")

        # Call the method with None as date_str
        result_without_date = get_games_by_date()

        # Assert that the results are the same, indicating the input is ignored
        assert result_with_date == result_without_date

    def test_get_games_by_date_returns_todays_games(self):
        """
        Test that get_games_by_date returns today's games from the scoreboard.

        This test verifies that the get_games_by_date function correctly retrieves
        the games from the ScoreBoard's get_dict method and returns the 'games'
        list from the 'scoreboard' dictionary.
        """
        # Mock the ScoreBoard to return a predefined dictionary
        mock_games = [{"id": "1234", "homeTeam": "Team A", "awayTeam": "Team B"}]
        mock_scoreboard = {"scoreboard": {"games": mock_games}}
        scoreboard.ScoreBoard = lambda: type('MockScoreBoard', (), {'get_dict': lambda: mock_scoreboard})()

        # Call the function under test
        result = get_games_by_date()

        # Assert that the function returns the games from the mocked scoreboard
        assert result == mock_games

    def test_get_team_game_today_empty_games_list(self):
        """
        Test get_team_game_today when the games list is empty.
        This is a negative test case where there are no games available.
        """
        with patch('app.services.games.get_games_by_date') as mock_get_games:
            mock_get_games.return_value = []
            result = get_team_game_today("Any Team")
            assert result == [], "Expected an empty list when there are no games available"

    def test_get_team_game_today_no_matching_team(self):
        """
        Test get_team_game_today when no games match the given team.
        This is a negative test case where the input is valid but no games are found.
        """
        with patch('app.services.games.get_games_by_date') as mock_get_games:
            mock_get_games.return_value = [
                {
                    "homeTeam": {"teamTricode": "ABC", "teamName": "Alpha Beta Charlie"},
                    "awayTeam": {"teamTricode": "DEF", "teamName": "Delta Echo Foxtrot"}
                }
            ]
            result = get_team_game_today("XYZ")
            assert result == [], "Expected an empty list when no games match the given team"

    def test_get_team_game_today_returns_correct_games(self):
        """
        Test that get_team_game_today returns the correct games for a given team.
        This test checks if the function correctly filters games based on team name
        or abbreviation, case-insensitively.
        """
        # Assuming we have mocked the get_games_by_date function to return some test data
        test_games = [
            {
                "homeTeam": {"teamTricode": "LAL", "teamName": "Los Angeles Lakers"},
                "awayTeam": {"teamTricode": "GSW", "teamName": "Golden State Warriors"}
            },
            {
                "homeTeam": {"teamTricode": "BOS", "teamName": "Boston Celtics"},
                "awayTeam": {"teamTricode": "NYK", "teamName": "New York Knicks"}
            }
        ]

        # Mock the get_games_by_date function
        with pytest.mock.patch('app.services.games.get_games_by_date', return_value=test_games):
            # Test with full team name (case-insensitive)
            result = get_team_game_today("Los Angeles Lakers")
            assert len(result) == 1
            assert result[0]["homeTeam"]["teamTricode"] == "LAL"

            # Test with team abbreviation (case-insensitive)
            result = get_team_game_today("gsw")
            assert len(result) == 1
            assert result[0]["awayTeam"]["teamTricode"] == "GSW"

            # Test with non-existent team
            result = get_team_game_today("Chicago Bulls")
            assert len(result) == 0

    def test_get_today_us_date_1(self):
        """
        Test that get_today_us_date returns today's date in US Eastern Time
        in the correct format (YYYY-MM-DD).
        """
        result = get_today_us_date()
        est = pytz.timezone("US/Eastern")
        now_est = datetime.now(est)
        expected = now_est.strftime("%Y-%m-%d")
        self.assertEqual(result, expected)

    def test_get_today_us_date_no_edge_cases(self):
        """
        This test verifies that the get_today_us_date function does not handle any specific edge cases.
        The function does not take any inputs and does not explicitly handle any error conditions.
        It simply returns the current date in US Eastern Time.
        """
        result = get_today_us_date()

        # Verify that the result is a string in the format YYYY-MM-DD
        assert isinstance(result, str)
        assert len(result) == 10
        assert result[4] == '-' and result[7] == '-'

        # Verify that the returned date is the current date in US Eastern Time
        est = pytz.timezone("US/Eastern")
        now_est = datetime.now(est)
        expected = now_est.strftime("%Y-%m-%d")
        assert result == expected

    def test_get_user_team_games_today_2(self):
        """
        Test that get_user_team_games_today returns filtered games for a valid user.

        This test verifies that when a valid user is found in the database,
        the function correctly filters and returns games for the user's teams.
        """
        mock_table = MagicMock()
        mock_user = {
            "email": "test@example.com",
            "teams": [{"id": "1"}, {"id": "2"}]
        }
        mock_table.get_item.return_value = {"Item": mock_user}

        mock_games = [
            {"homeTeam": {"teamId": "1"}, "awayTeam": {"teamId": "3"}},
            {"homeTeam": {"teamId": "4"}, "awayTeam": {"teamId": "2"}},
            {"homeTeam": {"teamId": "5"}, "awayTeam": {"teamId": "6"}}
        ]

        with patch('app.services.games.get_table', return_value=mock_table), \
             patch('app.services.games.get_games_by_date', return_value=mock_games):

            result = get_user_team_games_today("test@example.com")

        assert len(result) == 2
        assert result[0]["homeTeam"]["teamId"] == "1"
        assert result[1]["awayTeam"]["teamId"] == "2"

    def test_get_user_team_games_today_user_not_found(self):
        """
        Test get_user_team_games_today when the user is not found.
        This test verifies that a ValueError is raised when the user does not exist.
        """
        non_existent_email = "nonexistent@example.com"

        with pytest.raises(ValueError, match="User not found"):
            get_user_team_games_today(non_existent_email)

    def test_get_user_team_games_today_user_not_found_2(self):
        """
        Test the scenario where the user is not found in the database.
        This should raise a ValueError with the message "User not found".
        """
        with patch('app.services.games.get_table') as mock_get_table:
            mock_table = MagicMock()
            mock_table.get_item.return_value = {"Item": None}
            mock_get_table.return_value = mock_table

            with pytest.raises(ValueError, match="User not found"):
                get_user_team_games_today("nonexistent@example.com")
