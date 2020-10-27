import unittest
import stats_grabber

class TestStatsGrabber(unittest.TestCase):

    def setUp(self):
        self.grabber = stats_grabber.StatsGrabber('RGAPI-478416b7-f547-416d-b4d2-440d9a356946') # Deprecated Key. Don't worry :)
        self.unranked_games = self.grabber.get_unranked_games('CrystalJayde')
        self.ranked_games = self.grabber.get_ranked_games('CrystalJayde')
        self.assertIsNotNone(self.grabber)

    def test_ranked_games_have_ranked_id(self):
        self.assertTrue(self.ranked_games != [])
        for game in self.ranked_games:
            self.assertTrue(game['queueId'] in self.grabber._RANKED_QUEUE_IDS.values())

    def test_unranked_games_have_unranked_id(self):
        self.assertTrue(self.unranked_games != [])
        for game in self.unranked_games:
            self.assertTrue(game['queueId'] in self.grabber._UNRANKED_QUEUE_IDS.values())

    def test_unranked_games_have_wins(self):
        for game in self.unranked_games:
            self.assertIn('Win', game)
            self.assertTrue(game['Win'] == 'Fail' or game['Win'] == 'Win')

if __name__ == '__main__':
    unittest.main()
