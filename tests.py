import os
import unittest

#from config import basedir
from app import app
from app import api
from sports import MatchOutcomeAPI


class TestCase(unittest.TestCase):
	def test_match_outcome(self):
		match = MatchOutcomeAPI()
		result = match.get(1)
		assert 65 <= result['outcome']['home_score'] <= 125
		assert 65 <= result['outcome']['away_score'] <= 125

	def test_no_game_tie(self):
		match = MatchOutcomeAPI()
		results = [match.get(1) for x in xrange(10)]
		comparisons = [cmp(result['outcome']['home_score'], result['outcome']['away_score']) != 0 for result in results]
		assert all(comparisons), (result['outcome']['home_score'], result['outcome']['away_score'])
		


''' write a test that verifies that the MatchOutcomeAPI get 
    method returns a tuple of scores in the correct range(no ties allowed!'''






if __name__ == "__main__":
	unittest.main()