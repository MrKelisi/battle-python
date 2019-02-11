class Deck:

	def __init__(self):
		self.__cards = []

	def add_card(self, card):
		"""
		Ajoute une carte en haut du paquet.

		:param card: Carte à ajouter.
		:type card: Card

		:return: Rien.
		:rtype: None
		"""
		self.__cards.append(card)

	def insert_card(self, card):
		"""
		Ajoute une carte en dessous du paquet.

		:param card: Carte à ajouter.
		:type card: Card

		:return:
		"""
		self.__cards.insert(0, card)

	def get_card(self, index):
		"""
		:param index: Index de la carte à récupérer.
		:type index: int

		:return: Carte à l'index `index`.
		:rtype: Card
		"""
		return self.__cards[index]

	def number_of_cards(self):
		"""
		:return: Nombre de cartes dans le paquet.
		:rtype: int
		"""
		return len(self.__cards)

	def draw(self):
		"""
		Tire la carte tout en haut du paquet (et donc la retire du paquet).
		:return: Carte tout en haut du paquet.
		:rtype: Card
		"""
		return self.__cards.pop()

	def __repr__(self):
		return str(self.__cards)
