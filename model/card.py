from enum import IntEnum


class CardSuite(IntEnum):
	"""
	Familles de carte disponibles.
	"""
	SPADES = 0
	HEARTS = 1
	DIAMONDS = 2
	CLUBS = 3


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
