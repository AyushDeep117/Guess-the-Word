import unittest

from services.game_service import MAX_DAILY_GAMES


class TestGameService(unittest.TestCase):

    def test_daily_game_limit(self):
        self.assertEqual(MAX_DAILY_GAMES, 3)


if __name__ == "__main__":
    unittest.main()