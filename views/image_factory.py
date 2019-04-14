from PIL import Image, ImageTk
from model.card import CardRank, CardSuite


class ImageFactory:
	class __ImageFactory:
		def __init__(self):
			self.__back = Image.open("../resources/cards/back.png")
			self.__border = Image.open("../resources/cards/border.png")
			self.__cards = dict()

			for suite in CardSuite:
				suite = CardSuite(suite).name
				for rank in CardRank:
					rank = CardRank(rank).name
					self.__cards[rank + '_OF_' + suite] = Image.open("../resources/cards/" + rank + '_OF_' + suite + ".png")

		def get(self, card):  # Retourne l'image à partir d'un objet Carte
			r = card.get_rank()
			s = card.get_suite()
			index = CardRank(r).name + "_OF_" + CardSuite(s).name
			return ImageTk.PhotoImage(self.__cards[index])

		def get_back(self):  # Retourne le dos d'une carte
			return ImageTk.PhotoImage(self.__back)

		def get_border(self):  # Retourne la bordure d'une carte
			return ImageTk.PhotoImage(self.__border)

	instance = None

	def __new__(cls):
		if not ImageFactory.instance:
			ImageFactory.instance = ImageFactory.__ImageFactory()
		return ImageFactory.instance


ImageFactory()
