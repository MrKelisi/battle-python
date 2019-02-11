import unittest

from model.card import Card, CardSuite, CardRank
from model.deck import Deck


class TestDeck(unittest.TestCase):

	def setUp(self):
		self.deck = Deck()
		self.deck.add_card(Card(CardSuite.CLUBS, CardRank.A))
		self.deck.add_card(Card(CardSuite.DIAMONDS, CardRank.FOUR))

	def test_add_card(self):
		self.deck.add_card(Card(CardSuite.HEARTS, CardRank.K))
		self.assertEqual(self.deck.get_card(self.deck.number_of_cards() - 1).get_rank(), CardRank.K)

	def test_get_card(self):
		self.assertEqual(self.deck.get_card(0), Card(CardSuite.CLUBS, CardRank.A))

	def test_number_of_cards(self):
		self.assertEqual(self.deck.number_of_cards(), 2)


if __name__ == '__main__':
	unittest.main()
