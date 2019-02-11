import unittest

from model.card import *
from model.battle import *


class TestBattle(unittest.TestCase):

	def test_create_decks(self):
		decks = create_decks(3)
		self.assertTrue(decks[1].number_of_cards() == 17 and
		                (decks[0].number_of_cards() == decks[1].number_of_cards() == decks[2].number_of_cards()))

	def test_compare_cards(self):
		res = compare_cards([Card(CardSuite.DIAMONDS, CardRank.FOUR),
		               Card(CardSuite.DIAMONDS, CardRank.TWO),
		               Card(CardSuite.HEARTS, CardRank.FOUR)])
		self.assertEqual(2, len(res))
		
		res = compare_cards([Card(CardSuite.DIAMONDS, CardRank.A),
		               Card(CardSuite.DIAMONDS, CardRank.TWO),
		               Card(CardSuite.HEARTS, CardRank.FOUR)])

		self.assertEqual(res[0], Card(CardSuite.DIAMONDS, CardRank.A))


if __name__ == '__main__':
	unittest.main()
