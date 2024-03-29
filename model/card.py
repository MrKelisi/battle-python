import re
from enum import IntEnum


class CardSuite(IntEnum):
	"""
	Familles de carte disponibles.
	"""
	CLUBS = 0
	DIAMONDS = 1
	SPADES = 2
	HEARTS = 3


class CardRank(IntEnum):
	"""
	Rangs de carte disponibles.
	"""
	A = 14
	K = 13
	Q = 12
	J = 11
	TEN = 10
	NINE = 9
	EIGHT = 8
	SEVEN = 7
	SIX = 6
	FIVE = 5
	FOUR = 4
	THREE = 3
	TWO = 2


class Card:

	def __init__(self, card_suite, card_rank):
		"""
		Crée une carte à partir de sa famille et son rang.

		:param card_suite: Famille de la carte.
		:type card_suite: CardSuite

		:param card_rank: Rang de la carte.
		:type card_rank: CardRank
		"""
		self.__suite = card_suite
		self.__rank = card_rank

	def get_suite(self):
		"""
		Retourne la famille de la carte.

		:return: Famille de la carte.
		:rtype: CardSuite
		"""
		return self.__suite

	def get_rank(self):
		"""
		Retourne le rang de la carte.

		:return: Rang de la carte.
		:rtype: CardRank
		"""
		return self.__rank

	def __repr__(self):
		return str(self.__suite.name) + "(" + str(self.__rank.name) + ")"

	@staticmethod
	def parse(card_desc):
		"""
		Convertit la représentation en chaîne de caractères de description, donnée par __repr__, en un objet Card.

		:param card_desc: La chaîne de caractères qui décrit la carte.
		:type card_desc: str
		:return: La carte, ou None si la description n'a pas pu être lue.
		:rtype: Card
		"""
		matches = re.compile("([A-Z]+)\\(([A-Z]+)\\)").fullmatch(card_desc)  # Regex de découpage de la description.
		if matches is not None:  # La description de la carte est valide.
			# On peut construire la carte à partir des informations obtenues par le découpage.
			return Card(CardSuite[matches.group(1)], CardRank[matches.group(2)])
		else:  # La description de la carte est invalide.
			return None

	### OPÉRATEURS DE COMPARAISON ###

	def __eq__(self, other):
		return self.__suite == other.get_suite() and self.__rank == other.get_rank()

	def __ne__(self, other):
		return not(self.__eq__(other))

	def __lt__(self, other):
		return self.__rank < other.get_rank()

	def __gt__(self, other):
		return self.__rank > other.get_rank()

	def __le__(self, other):
		return self.__rank <= other.get_rank()

	def __ge__(self, other):
		return self.__rank < other.get_rank()
