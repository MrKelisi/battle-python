from PIL import Image, ImageTk


class ImageFactory:

	class __ImageFactory:
		WIDTH = 129
		HEIGHT = 185

		def __init__(self):
			self.__cards = Image.open("../resources/cards.png")

		def get(self, i, j):  # Retourne la carte en position (i,j) sur la planche
			i %= 15
			j %= 4
			crop = self.__cards.crop((i * self.WIDTH, j * self.HEIGHT, (i + 1) * self.WIDTH, (j + 1) * self.HEIGHT))
			return ImageTk.PhotoImage(crop)

		def get_c(self, card):  # Retourne la carte en fonction du rang et de la suite
			i = card.get_rank()
			j = card.get_suite()
			return self.get(i, j)

		def get_back(self):  # Retourne le dos d'une carte
			crop = self.__cards.crop((0, 0, self.WIDTH, self.HEIGHT))
			return ImageTk.PhotoImage(crop)

	instance = None

	def __new__(cls):
		if not ImageFactory.instance:
			ImageFactory.instance = ImageFactory.__ImageFactory()
		return ImageFactory.instance


ImageFactory()
