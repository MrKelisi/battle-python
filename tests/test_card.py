import unittest

from model.card import *


class TestCard(unittest.TestCase):

	def test_members(self):
		c = Card(CardSuite.HEARTS, CardRank.K)
		self.assertEqual(c.get_suite(), CardSuite.HEARTS)
		self.assertEqual(c.get_rank(), CardRank.K)


if __name__ == '__main__':
	unittest.main()
