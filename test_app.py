import string
from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<table', html)
            self.assertIn('boggle homepage', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            json = response.get_json()
            first_row = json["board"][0]

            self.assertIn(json["gameId"], games)
            self.assertIn("gameId", json)
            self.assertIn("board", json)
            self.assertIsInstance(json["gameId"], str)
            self.assertIsInstance(json["board"], list)
            self.assertIsInstance(first_row, list)

    def test_api_score_word(self):
        """Test if word is valid"""
        
        with app.test_client() as client:
            # create game instance and manually set board
            game_response = client.post('/api/new-game')
            game_id = game_response.get_json()["gameId"]
            row = ["D","O","G","G","O"]
            games[game_id].board = [row, row, row, row, row]

            # checking valid word
            response = client.post(
                '/api/score-word',
                json={
                    "game_id": game_id,
                    "word": "dog"
                })
            json_response = response.get_json()
            self.assertEqual({"result: ok"}, dict_response)

            # checking if word not on board
            response = client.post(
                '/api/score-word',
                json={
                    "game_id": game_id,
                    "word": "cat"
                })
            dict_response = response.get_json()
            self.assertEqual({"result: not-on-board"}, dict_response)

            # checking for duplicate word 
            response = client.post(
                '/api/score-word',
                json={
                    "game_id": game_id,
                    "word": "dog"
                })
            dict_response = response.get_json()
            self.assertEqual({"result: not-word"}, dict_response)


