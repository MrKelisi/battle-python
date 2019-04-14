import random

from model.deck import Deck
from model.card import Card, CardRank, CardSuite
from math import floor


def all_french_cards():
	cards = []

	def gen_cards_for_suite(card_suite):
		for i in range(2, 15):
			cards.append(Card(card_suite, CardRank(i)))

	gen_cards_for_suite(CardSuite.SPADES)
	gen_cards_for_suite(CardSuite.HEARTS)
	gen_cards_for_suite(CardSuite.DIAMONDS)
	gen_cards_for_suite(CardSuite.CLUBS)

	return cards


def create_decks(decks_number):

	all_cards = all_french_cards()

	cards_in_deck = floor(len(all_cards)/decks_number)

	decks = [Deck() for i in range(decks_number)]

	for deck in decks:
		for i in range(cards_in_deck):
			deck.add_card(all_cards.pop(random.randint(0, len(all_cards)) - 1))

	return decks


def compare_cards(cards):
	max_cards = [cards[0]]

	for c in cards[1:]:
		if c > max_cards[0]:  # La carte c est strictement plus grande que la carte maximum connue.
			max_cards = [c]
		elif not(c < max_cards[0]):
			# La carte c n'est pas strictement plus petite que la carte maximum connue, elle est donc = en rang.
			max_cards.append(c)

	return max_cards


class Battle:
	def __init__(self, players_number):
		self.__draw = []
		self.__decks = create_decks(players_number)
		self.__wins = [[] for _ in range(players_number)]

	def draw(self):
		self.__draw = []

		for deck in self.__decks:
			self.__draw.append(deck.draw())

		for c in self.__draw:
			self.__wins[self.turn_winner()].append(c)

		return self.__draw[:]

	def current_draw(self):
		return self.__draw[:]

	def nb_players(self):
		return len(self.__decks)

	def nb_cards(self, id_player):
		return self.__decks[id_player].number_of_cards()

	def is_battle(self):
		return len(compare_cards(self.__draw)) > 1

	def turn_winner(self):
		return self.__draw.index(compare_cards(self.__draw)[0])

	def nb_cards_won(self, player):
		return len(self.__wins[player])

	def nb_points(self, player):
		points = 0
		for card in self.__wins[player]:
			points += card.get_rank()
		return points
