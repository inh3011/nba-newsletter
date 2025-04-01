from datetime import datetime
from unittest.mock import patch, MagicMock

import pytz
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import players

from app.services.players import get_player_stats_by_id
from app.services.players import get_player_stats_by_name
from app.services.players import get_today_game_ids
from app.services.players import get_today_us_date
from app.services.players import search_players


class TestPlayers:

    def test_get_player_stats_by_id_1(self):
        """
        Test that get_player_stats_by_id returns correct player stats when a matching player is found.
        """
        mock_game_id = '1234567'
        mock_player_id = 123
        mock_player_data = {
            "personId": str(mock_player_id),
            "name": "John Doe",
            "starter": "1",
            "statistics": {
                "points": 20,
                "rebounds": 10,
                "assists": 5,
                "minutes": "30:00"
            }
        }
        mock_game_box = {
            "game": {
                "homeTeam": {"players": [mock_player_data]},
                "awayTeam": {"players": []}
            }
        }

        with patch('app.services.players.get_today_game_ids', return_value=[mock_game_id]):
            with patch('nba_api.live.nba.endpoints.boxscore.BoxScore') as mock_boxscore:
                mock_boxscore.return_value.get_dict.return_value = mock_game_box

                result = get_player_stats_by_id(mock_player_id)

                assert result == {
                    "name": "John Doe",
                    "starter": "1",
                    "points": 20,
                    "rebounds": 10,
                    "assists": 5,
                    "minutes": "30:00"
                }

    def test_get_player_stats_by_id_2(self):
        """
        Test get_player_stats_by_id when no player matches the given ID.

        This test mocks the get_today_game_ids and boxscore.BoxScore to simulate
        a scenario where no player in any game matches the given player_id.
        It verifies that the function returns the correct message when no stats are found.
        """
        with patch('app.services.players.get_today_game_ids') as mock_get_game_ids, \
             patch('app.services.players.boxscore.BoxScore') as mock_boxscore:

            mock_get_game_ids.return_value = ['1']
            mock_boxscore.return_value.get_dict.return_value = {
                'game': {
                    'homeTeam': {'players': [{'personId': '1', 'name': 'Player 1'}]},
                    'awayTeam': {'players': [{'personId': '2', 'name': 'Player 2'}]}
                }
            }

            result = get_player_stats_by_id(3)
            assert result == {"message": "No stats found for the player today."}

    def test_get_player_stats_by_id_no_games_today(self):
        """
        Test the scenario where there are no games today, resulting in no stats found for any player.
        """
        with patch('app.services.players.get_today_game_ids', return_value=[]):
            result = get_player_stats_by_id(123)
            assert result == {"message": "No stats found for the player today."}

    def test_get_player_stats_by_id_player_not_found(self):
        """
        Test the scenario where the player with the given ID is not found in any of today's games.
        """
        mock_game_ids = [1]
        mock_boxscore = {
            "game": {
                "homeTeam": {"players": []},
                "awayTeam": {"players": []}
            }
        }

        with patch('app.services.players.get_today_game_ids', return_value=mock_game_ids):
            with patch('app.services.players.boxscore.BoxScore') as mock_boxscore_class:
                mock_boxscore_instance = mock_boxscore_class.return_value
                mock_boxscore_instance.get_dict.return_value = mock_boxscore

                result = get_player_stats_by_id(999)
                assert result == {"message": "No stats found for the player today."}

    def test_get_player_stats_by_name_1(self):
        """
        Test that get_player_stats_by_name returns correct player stats when a matching player is found.
        """
        with patch('app.services.players.get_today_game_ids') as mock_get_game_ids, \
             patch('nba_api.live.nba.endpoints.boxscore.BoxScore') as mock_boxscore:

            mock_get_game_ids.return_value = ['1234']

            mock_boxscore_instance = mock_boxscore.return_value
            mock_boxscore_instance.get_dict.return_value = {
                "game": {
                    "homeTeam": {
                        "players": [
                            {
                                "name": "John Doe",
                                "starter": True,
                                "statistics": {
                                    "points": 20,
                                    "rebounds": 10,
                                    "assists": 5,
                                    "minutes": "30:00"
                                }
                            }
                        ]
                    },
                    "awayTeam": {
                        "players": []
                    }
                }
            }

            result = get_player_stats_by_name("John Doe")

            assert result == {
                "name": "John Doe",
                "starter": True,
                "points": 20,
                "rebounds": 10,
                "assists": 5,
                "minutes": "30:00"
            }

    def test_get_player_stats_by_name_2(self):
        """
        Tests that get_player_stats_by_name returns a message when no player is found.

        This test simulates a scenario where the player name is not found in any of the
        game box scores. It mocks the get_today_game_ids and BoxScore to return test data
        that doesn't include the searched player name.
        """
        with patch('app.services.players.get_today_game_ids') as mock_get_game_ids, \
             patch('app.services.players.boxscore.BoxScore') as mock_boxscore:

            mock_get_game_ids.return_value = ['1234']
            mock_boxscore.return_value.get_dict.return_value = {
                "game": {
                    "homeTeam": {"players": [{"name": "Player One"}]},
                    "awayTeam": {"players": [{"name": "Player Two"}]}
                }
            }

            result = get_player_stats_by_name("Nonexistent Player")
            assert result == {"message": "No stats found for the player today."}

    def test_get_player_stats_by_name_player_not_found(self):
        """
        Test the scenario where no player stats are found for the given name.
        This tests the edge case explicitly handled in the method where no matching player is found.
        """
        with patch('app.services.players.get_today_game_ids', return_value=['game1']):
            with patch('nba_api.live.nba.endpoints.boxscore.BoxScore') as mock_boxscore_class:
                # Mock된 BoxScore 인스턴스와 get_dict 리턴값 설정
                mock_instance = MagicMock()
                mock_instance.get_dict.return_value = {
                    'game': {
                        'homeTeam': {'players': []},
                        'awayTeam': {'players': []}
                    }
                }
                mock_boxscore_class.return_value = mock_instance

                # 테스트 실행
                result = get_player_stats_by_name("NonexistentPlayer")
                assert result == {"message": "No stats found for the player today."}

    def test_get_today_game_ids_no_games(self):
        """
        Test the scenario where there are no games scheduled for today.
        This tests the edge case of an empty list being returned.
        """
        # Mock the ScoreBoard to return an empty games list
        scoreboard.ScoreBoard = lambda: type('MockScoreBoard', (), {'get_dict': lambda: {"scoreboard": {"games": []}}})


        result = get_today_game_ids()
        assert result == [], "Expected an empty list when no games are scheduled"

    def test_get_today_game_ids_returns_list_of_game_ids(self):
        """
        Test that get_today_game_ids returns a list of game IDs from the scoreboard.

        This test verifies that the function correctly retrieves the game IDs from
        the ScoreBoard API and returns them as a list.
        """
        # Mock the ScoreBoard API response
        mock_games = [{"gameId": "1234"}, {"gameId": "5678"}]
        with patch('nba_api.live.nba.endpoints.scoreboard.ScoreBoard') as mock_scoreboard_class:
            mock_instance = MagicMock()
            mock_instance.get_dict.return_value = {
                "scoreboard": {"games": mock_games}
            }
            mock_scoreboard_class.return_value = mock_instance

            # Call the function
            result = get_today_game_ids()

            # Assert the result
            assert result == ["1234", "5678"]

    def test_get_today_us_date_1(self):
        """
        Test that get_today_us_date returns the current date in US Eastern Time
        in the format 'YYYY-MM-DD'.
        """
        est = pytz.timezone("US/Eastern")
        expected_date = datetime.now(est).strftime("%Y-%m-%d")
        actual_date = get_today_us_date()
        assert expected_date == actual_date

    def test_search_players_1(self):
        """
        Test that search_players returns the correct list of players when given a valid search string.
        This test verifies that the function correctly calls players.find_players_by_full_name
        and returns its result.
        """
        search_term = "LeBron James"
        expected_result = players.find_players_by_full_name(search_term)
        actual_result = search_players(search_term)
        assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"

    def test_search_players_empty_string(self):
        """
        Test the behavior of search_players when given an empty string input.
        This is an edge case that is implicitly handled by the underlying 
        find_players_by_full_name method.
        """
        result = search_players("")
        assert result == [], "Expected an empty list for empty string input"

    def test_search_players_non_existent_name(self):
        """
        Test the behavior of search_players when given a name that doesn't exist.
        This is an edge case that is implicitly handled by the underlying 
        find_players_by_full_name method.
        """
        result = search_players("NonExistentPlayer")
        assert result == [], "Expected an empty list for non-existent player name"

    def search_players(search: str):
        """
        Search NBA players by full name.
        Returns a list of player dictionaries.
        """
        return players.find_players_by_full_name(search)
