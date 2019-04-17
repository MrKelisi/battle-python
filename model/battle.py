import random
import time
from abc import abstractmethod

from model.deck import Deck
from model.card import Card, CardRank, CardSuite
from math import floor


def all_french_cards():
	"""
	Génère un jeu complet de cartes françaises.
	:return: La liste complète des cartes du jeu.
	:rtype: Card[]
	"""
	cards = []

	def gen_cards_for_suite(card_suite):
		"""
		Génère toutes les valeurs des cartes pour une suite donnée.
		:param card_suite: La suite pour laquelle générer les cartes.
		:type card_suite: CardSuite
		:return: La liste des cartes générées.
		:rtype: Card[]
		"""
		for i in range(2, 15):
			cards.append(Card(card_suite, CardRank(i)))

	gen_cards_for_suite(CardSuite.SPADES)
	gen_cards_for_suite(CardSuite.HEARTS)
	gen_cards_for_suite(CardSuite.DIAMONDS)
	gen_cards_for_suite(CardSuite.CLUBS)

	return cards


def create_decks(decks_number):
	"""
	Crée un certain nombre de decks avec le même nombre de cartes issues d'un jeu de cartes françaises complet.
	:param decks_number: Le nombre de decks à créer.
	:type decks_number: int
	:return: La liste des decks créés.
	:rtype: Deck[]
	"""
	all_cards = all_french_cards()

	cards_in_deck = floor(len(all_cards)/decks_number)

	decks = [Deck() for i in range(decks_number)]  # Création de `decks_number` decks indépendants.

	for deck in decks:  # On remplit chaque deck de cartes aléatoirement choisies dans la liste complète des cartes.
		for i in range(cards_in_deck):
			deck.add_card(all_cards.pop(random.randint(1, len(all_cards)) - 1))

	return decks


def compare_cards(cards):
	"""
	Compare les cartes et renvoie la liste des cartes les plus grosses.
	:param cards: La liste des cartes à comparer.
	:type cards: Card[]
	:return: La liste des cartes les plus grandes.
	:rtype: Card[]
	"""
	max_cards = [cards[0]]

	for c in cards[1:]:
		if c > max_cards[0]:  # La carte c est strictement plus grande que la carte maximum connue.
			max_cards = [c]
		elif not(c < max_cards[0]):
			# La carte c n'est pas strictement plus petite que la carte maximum connue, elle est donc = en rang.
			max_cards.append(c)

	return max_cards


def compare_players_cards(players_cards):
	"""
	Compare les cartes jouées par les joueurs, et retourne la liste des joueurs ayant joué les plus grosses cartes.
	:param players_cards: Dictionnaire des cartes jouées par les joueurs (joueur => carte jouée).
	:type players_cards: dict
	:return: La liste des joueurs ayant joué les plus grosses cartes.
	:rtype: str[]
	"""
	players = list(players_cards.keys())
	max_players = [players[0]]

	for player in players[1:]:
		if players_cards[player] > players_cards[max_players[0]]:
			# La carte du joueur courant est strictement plus grande que la carte maximum connue.
			max_players = [player]
		elif not(players_cards[player] < players_cards[max_players[0]]):
			# La carte du joueur courant n'est pas strictement plus petite que la carte maximum connue, elle est donc = en rang.
			max_players.append(player)

	return max_players


def default_callback(*args):
	"""
	Callback par défaut, ne fait rien.
	"""
	pass


class Battle:
	"""
	Classe du jeu de la bataille abstraite.
	"""
	def __init__(self):
		"""
		Initialise les callbacks et les données nécessaires du jeu de la bataille.
		"""
		self.turn = 0
		self.is_game_ended = False

		self.on_new_turn = default_callback
		self.on_card_drawn = default_callback

		self.on_battle = default_callback
		self.on_turn_finished = default_callback
		self.on_turn_par = default_callback
		self.on_player_picked_card = default_callback

		self.on_game_ended = default_callback
		self.on_game_won = default_callback
		self.on_game_par = default_callback

	@abstractmethod
	def draw_card(self):
		"""
		Tire une carte.
		"""
		pass

	@abstractmethod
	def my_cards_to_pick(self):
		"""
		Renvoie les cartes à récupérer.
		:return: La liste des cartes à récupérer.
		:rtype: Card[]
		"""
		pass

	@abstractmethod
	def pick_card(self, card):
		"""
		Récupère une carte.
		:param card: La carte à récupérer.
		:type card: Card
		"""
		pass

	@abstractmethod
	def my_points(self):
		"""
		Renvoie le nombre de points du joueur.
		:return: Le nombre de points du joueur.
		:rtype: int
		"""
		pass

	@abstractmethod
	def points_of(self, player_name):
		"""
		Renvoie le nombre de points d'un joueur donné.
		:param player_name: Le joueur pour lequel renvoyer les points.
		:type player_name: str
		:return: Les points du joueur.
		:rtype: int
		"""
		pass

	@abstractmethod
	def others_points(self):
		"""
		Renvoie un dictionnaire contenant les points des autres joueurs.
		:return: Le dictionnaire contenant les points des autres joueurs (joueur => nombre de points).
		:rtype: dict
		"""
		pass


class ServerBattle(Battle):
	def __init__(self, battle_net_server, short_rule=True):
		"""
		Initialise les callbacks et les données nécessaires du jeu de la bataille pour un serveur.
		:param battle_net_server: Le NetHandler du serveur.
		:type battle_net_server: BattleNetServer
		:param short_rule: Vrai si la règle courte doit être utilisée, faux si la règle longue doit être utilisée.
		:type short_rule: bool
		"""
		Battle.__init__(self)

		# Valeurs en paramètre.
		self.__game_server = battle_net_server
		self.__short_rule = short_rule

		# Initialisation des joueurs dans le jeu : tous les joueurs connectés aux serveur + le serveur lui-même.
		self.__players_in_game = []
		for player in self.__game_server.players:
			self.__players_in_game.append(player.agent_name)
		self.__players_in_game.append(self.__game_server.name)

		# Les points des joueurs dans le jeu.
		self.__players_points = {}
		for player_name in self.__players_in_game:
			self.__players_points[player_name] = 0

		# Initialisation des paquets en fonction du nombre de joueurs dans la partie.
		decks = create_decks(len(self.__players_in_game))
		# Attribution des paquets générés pour chaque joueur du jeu.
		self.__players_decks = {}
		for i in range(0, len(self.__players_in_game)):
			self.__players_decks[self.__players_in_game[i]] = decks[i]

		# Initialisation de la liste des cartes à récupérer (vide au départ).
		self.__cards_to_pick = {}
		for player in self.__game_server.players:
			self.__cards_to_pick[player.agent_name] = []
		self.__cards_to_pick[None] = []

		# Callbacks.
		self.__game_server.on_player_draw_card = self.__card_drawn_by_player
		self.__game_server.on_player_picked_card = self.__card_picked

		# On indique aux clients que la partie commence.
		self.__game_server.game_begin()
		time.sleep(1)  # Attente d'une seconde avant de commencer le premier tour.
		self.__new_turn()

	def __new_turn(self):
		"""
		Commence un nouveau tour de bataille.
		"""
		self.turn += 1

		# On vérifie qui sont les joueurs qui restent en jeu (tous ceux qui ont encore des cartes dans leur paquet).
		players_in_game = []
		for player_name, deck in self.__players_decks.items():
			if deck.number_of_cards() >= 1:  # Il reste des cartes dans le paquet.
				players_in_game.append(player_name)
			elif player_name in self.__players_in_game:  # Si le joueur jouait jusqu'à maintenant.
				if player_name == self.__game_server.name:
					# Le joueur ayant perdu est le serveur, on lui signale.
					self.is_game_ended = True
					self.on_game_ended()
				else:
					# Le joueur ayant perdu est un client, on lui signale.
					self.__game_server.game_ended(player_name)
		self.__players_in_game = players_in_game  # Mise à jour des joueurs dans la partie.

		if len(self.__players_in_game) > 1:  # S'il reste plus d'une personne dans la partie, on doit continuer à jouer.
			self.__players_in_turn = self.__players_in_game.copy()

			# Remise à zéro des cartes jouées.
			self.__cards_played = {}
			for player_name in self.__players_in_turn:
				self.__cards_played[player_name] = []

			# Les joueurs de la partie doivent jouer 1 carte.
			self.__number_of_cards_to_play = {}
			for player_name in self.__players_in_turn:
				self.__number_of_cards_to_play[player_name] = 1

			self.__game_server.game_new_turn()
			self.on_new_turn()
		else:  # Il reste une personne ou moins dans la partie.
			if self.__short_rule:
				# Dans le cas de la règle courte, il peut rester 0 ou 1 personne. S'il reste une personne seule, on rajoute
				# les cartes qu'il lui reste à ses points, puis on termine la partie.

				if len(self.__players_in_game) == 1:
					# Il reste des cartes au dernier joueur, on lui ajoute le nombre de cartes au score.
					self.__players_points[self.__players_in_game[0]] += \
						self.__players_decks[self.__players_in_game[0]].number_of_cards()

				# On cherche maintenant à établir la liste des gagnants.
				players_points_names = list(self.__players_points.keys())
				winners = [players_points_names[0]]
				for player_name in players_points_names[1:]:
					# Pour chaque joueur, on regarde s'il fait mieux ou aussi bien que le(s) gagnant(s) précédemment sélectionné(s).
					if self.__players_points[player_name] > self.__players_points[winners[0]]:
						# Le joueur courant a un score supérieur au(x) gagnant(s) précédent(s),
						# on le désigne donc comme unique gagnant jusque là.
						winners = [player_name]
					elif not(self.__players_points[player_name] < self.__players_points[winners[0]]):
						# Le joueur courant a un score égal au(x) gagnant(s) précédent(s), on l'ajoute à la liste des gagnants.
						winners.append(player_name)

				if len(winners) == 1:
					# Il n'y a qu'un gagnant dans la liste, on a donc un vainqueur.
					self.__game_server.game_won(winners[0])
					self.on_game_won(winners[0])
					self.__game_server.stop()
				else:
					# Plusieurs personnes ont le même score, on a donc une égalité.
					self.__game_server.game_par(winners)
					self.on_game_par(winners)
					self.__game_server.stop()
			else:
				# Dans le cas de la règle longue, il ne peut pas y avoir d'égalité,
				# et il y a forcément une personne qui possède les cartes de tous ses adversaires au bout du compte.
				winner = self.__players_in_game[0]
				self.__game_server.game_won(winner)
				self.on_game_won(winner)
				self.__game_server.stop()

	def draw_card(self):
		# Le tirage d'une carte n'est possible que si le joueur en question a encore une carte à tirer.
		if self.__number_of_cards_to_play[self.__game_server.name] > 0:
			card = self.__players_decks[self.__game_server.name].draw()
			self.__cards_played[self.__game_server.name].append(card)  # Ajout aux cartes jouées par le joueur.
			self.__number_of_cards_to_play[self.__game_server.name] -= 1  # On réduit de 1 les cartes qu'il lui reste à jouer.
			self.__game_server.game_turn_card_drawn(self.__game_server.name, str(card))  # Envoi de la carte tirée aux clients.
			self.on_card_drawn(self.__game_server.name, card)
			self.__turn_handle_results()  # Vérification de la fin de la période de tirage des cartes.

	def __card_drawn_by_player(self, player_name):
		# Le tirage d'une carte n'est possible que si le joueur en question a encore une carte à tirer.
		if self.__number_of_cards_to_play[player_name] > 0:
			card = self.__players_decks[player_name].draw()
			self.__cards_played[player_name].append(card)  # Ajout aux cartes jouées par le joueur.
			self.__number_of_cards_to_play[player_name] -= 1  # On réduit de 1 les cartes qu'il lui reste à jouer.
			self.__game_server.game_turn_card_drawn(player_name, str(card))  # Envoi de la carte tirée aux clients.
			self.on_card_drawn(player_name, card)
			self.__turn_handle_results()  # Vérification de la fin de la période de tirage des cartes.

	def __turn_handle_results(self):
		"""
		S'occupe de vérifier et traiter la fin de la période de tirage.
		"""
		all_played = True

		# Vérification que toutes les cartes devant être tirées l'ont été.
		for _, number_of_cards_to_play in self.__number_of_cards_to_play.items():
			if number_of_cards_to_play > 0:
				all_played = False
				break

		if all_played:  # Toutes les cartes ont été tirées.
			# On récupère uniquement les cartes du dessus pour la comparaison.
			top_cards = {}
			for player_name, played_cards in self.__cards_played.items():
				if player_name in self.__players_in_turn:
					top_cards[player_name] = played_cards[-1]  # La dernière carte posée.

			# Comparaison des cartes.
			max_players = compare_players_cards(top_cards)
			if len(max_players) == 1:  # Il n'y a qu'un seul joueur qui a la plus grosse carte, il remporte la manche.
				winner_name = max_players[0]
				if winner_name == self.__game_server.name:
					winner_name = None  # Si on est le gagnant, on ne passe pas le nom du gagnant en argument mais None.

				for _, played_cards in self.__cards_played.items():
					self.__cards_to_pick[winner_name] += played_cards  # Le gagnant reprend toutes les cartes du joueur.

				self.__game_server.game_turn_won(max_players[0])
				self.on_turn_finished(winner_name)
			else:  # Il y a plusieurs joueurs qui ont les cartes les plus grosses, on entre dans une bataille entre eux.
				par = False  # Définit si on se trouve dans le cas d'une égalité (impossibilité de mener la bataille à bien).
				in_battle = False  # Définit si le serveur est dans la bataille.
				other_members_names = []  # Liste des autres joueurs que le serveur faisant partie de la bataille.

				# Pour chaque joueur jouant le tour, on regarde s'il lui reste assez de cartes pour continuer.
				# Si ce n'est pas le cas, on déclare une égalité.
				for player_name in self.__players_in_turn:
					if player_name in max_players:
						if self.__players_decks[player_name].number_of_cards() >= 2:
							# Le joueur courant a suffisamment de cartes pour continuer.
							self.__number_of_cards_to_play[player_name] += 2
							if player_name == self.__game_server.name:  # Le joueur courant = le serveur.
								in_battle = True
							else:  # Le joueur courant = un autre joueur.
								other_members_names.append(player_name)
						else:
							# Le joueur courant n'a pas suffisamment de cartes pour continuer.
							par = True
							break

				if par:
					# Cas d'une égalité : on arrête la manche et on demande aux joueurs en jeu de récupérer leurs cartes engagées.
					for player_name, played_cards in self.__cards_played.items():
						if player_name == self.__game_server.name:
							player_name = None
						self.__cards_to_pick[player_name] = played_cards.copy()

					self.__game_server.game_turn_par()
					self.on_turn_par()
				else:
					# La bataille peut se dérouler, on demande donc aux joueurs de la bataille de continuer à jouer ce tour.
					self.__players_in_turn = max_players

					self.__game_server.game_turn_battle(max_players)
					self.on_battle(in_battle, other_members_names)

	def my_cards_to_pick(self):
		"""
		Renvoie les cartes à récupérer.
		:return: La liste des cartes à récupérer.
		:rtype: Card[]
		"""
		cards_to_pick = self.__cards_to_pick[None].copy()
		random.shuffle(cards_to_pick)  # Pour éviter de se trouver dans des parties bloquées, on mélange avant de retourner.
		return cards_to_pick

	def pick_card(self, card):
		"""
		Récupère une carte.
		:param card: La carte à récupérer.
		:type card: Card
		"""
		# Recherche de la carte à récupérer dans la liste des cartes à récupérer du joueur.
		for i in range(0, len(self.__cards_to_pick[None])):
			if card == self.__cards_to_pick[None][i]:
				self.__cards_to_pick[None].pop(i)  # On supprime la carte de la liste des cartes à récupérer.
				self.__game_server.game_turn_card_pick(str(card))  # On indique aux autres qu'on a récupéré la carte.
				self.__players_points[self.__game_server.name] += 1
				if not self.__short_rule:  # Dans la règle longue, on remet la carte récupérée en dessous du paquet.
					self.__players_decks[self.__game_server.name].insert_card(card)
				self.on_player_picked_card(card)
				break

		self.__turn_handle_card_picked()  # Vérification de la fin de la période de récupération des cartes.

	def __card_picked(self, player_name, card_desc):
		card = Card.parse(card_desc)
		# Recherche de la carte à récupérer dans la liste des cartes à récupérer du joueur.
		for i in range(0, len(self.__cards_to_pick[player_name])):
			if card == self.__cards_to_pick[player_name][i]:
				self.__cards_to_pick[player_name].pop(i)  # On supprime la carte de la liste des cartes à récupérer.
				self.__players_points[player_name] += 1
				if not self.__short_rule:  # Dans la règle longue, on remet la carte récupérée en dessous du paquet.
					self.__players_decks[player_name].insert_card(card)
				self.on_player_picked_card(card)
				break

		self.__turn_handle_card_picked()  # Vérification de la fin de la période de récupération des cartes.

	def __turn_handle_card_picked(self):
		"""
		S'occupe de vérifier la fin de la période de récupération des cartes.
		"""
		all_empty = True
		# On vérifie que la liste des cartes à récupérer de chaque joueur est vide.
		for _, cards in self.__cards_to_pick.items():
			if cards:
				all_empty = False

		if all_empty:  # Toutes les cartes on été récupérées, on peut jouer un nouveau tour.
			self.__new_turn()

	def my_points(self):
		return self.points_of(self.__game_server.name)

	def points_of(self, player_name):
		return self.__players_points[player_name]

	def others_points(self):
		others_points = {}
		for player_name, points in self.__players_points.items():
			if player_name is not self.__game_server.name:
				others_points[player_name] = points
		return others_points


class ClientBattle(Battle):
	def __init__(self, battle_net_client):
		"""
		Initialise les callbacks et les données nécessaires du jeu de la bataille pour un client.
		:param battle_net_client: Le NetHandler du client.
		:type battle_net_client: BattleNetClient
		"""
		Battle.__init__(self)

		# Valeurs en paramètre.
		self.__game_client = battle_net_client

		# Initialisation des points des joueurs dans le jeu : tous les joueurs aussi connectés + le client lui-même.
		self.__players_points = {}
		for player_name in self.__game_client.players_names:
			self.__players_points[player_name] = 0
		self.__players_points[None] = 0

		# Initialisation des listes des cartes jouées par tous les joueurs aussi connectés + le client lui-même.
		self.__cards_played = {}
		for player_name in self.__game_client.players_names:
			self.__cards_played[player_name] = []
		self.__cards_played[None] = []

		# Initialisation des listes des cartes à récupérer par tous les joueurs aussi connectés + le client lui-même.
		self.__cards_to_pick = {}
		for player_name in self.__game_client.players_names:
			self.__cards_to_pick[player_name] = []
		self.__cards_to_pick[None] = []

		# Callbacks.
		self.__game_client.on_game_new_turn = self.__new_turn
		self.__game_client.on_my_card_drawn = self.__my_card_drawn
		self.__game_client.on_player_card_drawn = self.__player_card_drawn
		self.__game_client.on_turn_battle_with = self.__battle_with
		self.__game_client.on_turn_finished = self.__turn_finished
		self.__game_client.on_player_picked_card = self.__card_picked
		self.__game_client.on_game_ended = self.__game_ended
		self.__game_client.on_game_won = self.__game_won
		self.__game_client.on_game_par = self.__game_par

	def __new_turn(self):
		self.turn += 1

		# Remise à zéro des cartes jouées.
		self.__cards_played = {}
		for player_name in self.__game_client.players_names:
			self.__cards_played[player_name] = []
		self.__cards_played[None] = []

		self.on_new_turn()

	def draw_card(self):
		self.__game_client.game_turn_draw_card()  # Envoi de la demande de tirage de la carte au serveur.

	def __my_card_drawn(self, card_desc):
		"""
		Réception de la carte tirée par le client.
		:param card_desc: La description de la carte tirée.
		:type card_desc: str
		"""
		card = Card.parse(card_desc)
		self.__cards_played[None].append(card)
		self.on_card_drawn(None, card)

	def __player_card_drawn(self, player_name, card_desc):
		"""
		Réception de la carte tirée par un autre joueur.
		:param player_name: Le joueur ayant tiré la carte.
		:type player_name: str
		:param card_desc: La description de la carte tirée.
		:type card_desc: str
		"""
		card = Card.parse(card_desc)
		self.__cards_played[player_name].append(card)
		self.on_card_drawn(player_name, card)

	def __battle_with(self, in_battle, other_members_names):
		self.on_battle(in_battle, other_members_names)

	def __turn_finished(self, winner_name):
		if winner_name is None:  # Égalité ! Tout le monde récupère ses cartes.
			self.__cards_to_pick = self.__cards_played.copy()
			self.on_turn_par()
		else:  # Quelqu'un a gagné, c'est ce joueur qui récupère toutes les cartes jouées.
			if winner_name == self.__game_client.name:
				winner_name = None  # Si on est le gagnant, on ne passe pas le nom du gagnant en argument mais None.

			for _, played_cards in self.__cards_played.items():
				self.__cards_to_pick[winner_name] += played_cards

			self.on_turn_finished(winner_name)

	def my_cards_to_pick(self):
		"""
		Renvoie les cartes à récupérer.
		:return: La liste des cartes à récupérer.
		:rtype: Card[]
		"""
		cards_to_pick = self.__cards_to_pick[None].copy()
		random.shuffle(cards_to_pick)  # Pour éviter de se trouver dans des parties bloquées, on mélange avant de retourner.
		return cards_to_pick

	def pick_card(self, card):
		"""
		Récupère une carte.
		:param card: La carte à récupérer.
		:type card: Card
		"""
		# Recherche de la carte à récupérer dans la liste des cartes à récupérer du joueur.
		for i in range(0, len(self.__cards_to_pick[None])):
			if card == self.__cards_to_pick[None][i]:
				self.__cards_to_pick[None].pop(i)  # On supprime la carte de la liste des cartes à récupérer.
				self.__game_client.game_turn_card_pick(str(card))  # On indique aux autres qu'on a récupéré la carte.
				self.__players_points[None] += 1
				self.on_player_picked_card(card)
				break

	def __card_picked(self, player_name, card_desc):
		card = Card.parse(card_desc)
		# Recherche de la carte à récupérer dans la liste des cartes à récupérer du joueur.
		for i in range(0, len(self.__cards_to_pick[player_name])):
			if card == self.__cards_to_pick[player_name][i]:
				self.__cards_to_pick[player_name].pop(i)  # On supprime la carte de la liste des cartes à récupérer.
				self.__players_points[player_name] += 1
				self.on_player_picked_card(card)
				break

	def my_points(self):
		return self.points_of(None)

	def points_of(self, player_name):
		return self.__players_points[player_name]

	def others_points(self):
		others_points = {}
		for player_name, points in self.__players_points.items():
			if player_name is not None:
				others_points[player_name] = points
		return others_points

	def __game_ended(self):
		self.is_game_ended = True

	def __game_won(self, winner_name):
		self.on_game_won(winner_name)
		self.__game_client.stop()

	def __game_par(self, winners_names):
		self.on_game_par(winners_names)
		self.__game_client.stop()
