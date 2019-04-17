class BattleBot:
	"""
	Classe qui rassemble le code des robots qui jouent au jeu de la bataille.
	"""
	def __init__(self, battle):
		self.battle = battle  # Objet de jeu.

		# Affectation des callbacks.
		self.battle.on_new_turn = self.__game_new_turn
		self.battle.on_battle = self.__game_turn_battle
		self.battle.on_turn_finished = self.__game_turn_finished
		self.battle.on_turn_par = self.__game_turn_par
		self.battle.on_game_won = self.__game_won
		self.battle.on_game_par = self.__game_par

	def __game_new_turn(self):
		"""
		Lancé lorsqu'un nouveau tour va être joué.
		"""
		if self.battle.is_game_ended:  # Le jeu est indiqué comme terminé, on ne doit plus tirer de cartes.
			print("Jeu terminé pour moi, points des autres : " + str(self.battle.others_points()))
		else:  # On est encore en jeu, on doit tirer une carte.
			print("Mes points : " + str(self.battle.my_points()))
			print("Points des autres : " + str(self.battle.others_points()))
			self.battle.draw_card()

	def __game_turn_battle(self, in_battle, other_members_names):
		"""
		Lancé lorsqu'une bataille est engagée entre les joueurs indiqués en paramètre.
		:param in_battle: Vrai si on est dans la bataille, faux sinon.
		:type in_battle: bool
		:param other_members_names: Les autres membres dans la bataille.
		:type other_members_names: str[]
		"""
		if in_battle:  # On est dans la bataille, on tire deux cartes (celle masquée et celle montrée).
			print("Bataille : je suis dedans !")
			self.battle.draw_card()
			self.battle.draw_card()
		else:  # On n'est pas dans la bataille, on attend la fin du tour.
			print("Bataille : je ne suis pas dedans.")

	def __game_turn_finished(self, winner_name):
		"""
		Lancé lorsque le tour est terminé et qu'UN gagnant est déclaré.
		On ramasse les cartes si on a gagné.
		:param winner_name: Nom du gagnant. None si on est le gagnant.
		:type winner_name: str
		"""
		if winner_name is None:  # On a gagné ! On doit récupérer les cartes des autres joueurs.
			print("J'ai gagné ce tour !")
			for card in self.battle.my_cards_to_pick():
				self.battle.pick_card(card)
		else:  # On a perdu, on attend que le gagnant récupère ses cartes.
			print(winner_name + " a gagné ce tour.")

	def __game_turn_par(self):
		"""
		Lancé lorsque le tour est terminé et qu'il n'a pas été possible de déterminer de gagnant (égalité).
		"""
		print("Égalité ! Tout le monde récupère les cartes jouées.")
		for card in self.battle.my_cards_to_pick():
			self.battle.pick_card(card)

	def __game_won(self, winner_name):
		"""
		Lancé lorsque le jeu de la bataille a été gagné par quelqu'un.
		:param winner_name: Le nom du gagnant.
		:type winner_name: str
		"""
		print("Le gagnant est " + winner_name + " ! Bravo !")

	def __game_par(self, winners_names):
		"""
		Lancé lorsque le jeu de la bataille a mené à une égalité de points (parties courtes).
		:param winners_names: Noms des gagnants.
		:type winners_names: str[]
		"""
		print("Égalité, il y a plusieurs gagnants : " + str(winners_names))
