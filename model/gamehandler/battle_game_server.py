from model.gamehandler.battle_game_handler import BattleGameHandler


def default_callback(*args):
	pass


class BattleGameServer(BattleGameHandler):
	def __init__(self, room_name):
		self.room_name = room_name
		self.players = []
		self.game_started = False

		self.on_new_player = default_callback  # client_name
		self.on_player_draw_card = default_callback  # client_name
		self.on_player_picked_card = default_callback  # client_name, card_desc

		BattleGameHandler.__init__(self)

	# Envoi de messages. #

	def room(self):
		self.send_msg("room: " + self.room_name + ".")

	def players_list(self):
		players_list_cmd = "players_list [" + self.agent_name + ", "
		for player_agent in self.players:
			players_list_cmd += player_agent.agent_name + ", "
		self.send_msg(players_list_cmd + "].")

	def game_begin(self):
		self.game_started = True
		self.send_msg("game_begin.")

	def game_new_turn(self):
		self.send_msg("game_new_turn.")

	def game_turn_card_drawn(self, player_name, card_desc):
		self.send_msg("game_turn_card_drawn: " + player_name + ", " + card_desc + ".")

	def game_turn_won(self, winner_name):
		self.send_msg("game_turn_won: " + winner_name + ".")

	def game_turn_battle(self, battle_members_names):
		players_list_str = ""
		for player_name in battle_members_names:
			players_list_str += player_name + ", "
		self.send_msg("game_turn_battle: [" + players_list_str + "].")

	def game_turn_card_pick(self, card_desc):
		self.send_msg("game_turn_card_pick: " + self.name + ", " + card_desc + ".")

	def game_won(self, winner_name):
		self.send_msg("game_won: " + winner_name + ".")

	def game_par(self, winners_names):
		players_list_str = ""
		for player_name in winners_names:
			players_list_str += player_name + ", "
		self.send_msg("game_par: [" + players_list_str + "].")

	# Réception de messages. #

	def ivy__find_rooms(self, agent):
		if not self.game_started:
			self.room()

	def ivy__room(self, agent, room_name):
		pass  # Rien à gérer dans le cas d'un serveur, il gère sa salle sans se soucier des salles "voisines".

	def ivy__connect_room(self, agent, gamehost_name):
		if self.name == gamehost_name and not self.game_started and len(self.players) <3 and agent not in self.players:
			self.send_msg("accept_player: " + agent.agent_name + ".")
			self.players.append(agent)
			self.players_list()
			self.on_new_player(agent.agent_name)
		if len(self.players) >= 3:
			self.send_msg("room_is_full.")

	def ivy__room_is_full(self, agent):
		pass  # Rien à gérer dans le cas d'un serveur, c'est lui qui indique si une salle est pleine ou non !

	def ivy__accept_player(self, agent, player_name):
		pass  # Rien à gérer dans le cas d'un serveur, c'est lui qui décide si on accepte un joueur !

	def ivy__players_list(self, agent, players_names, _):
		pass  # Rien à gérer dans le cas d'un serveur, c'est lui qui envoie la liste de joueurs !

	def ivy__game_begin(self, agent):
		pass  # Rien à gérer dans le cas d'un serveur, c'est lui qui décide quand le jeu commence !

	def ivy__game_new_turn(self, agent):
		pass  # Rien à gérer dans le cas d'un serveur, c'est lui qui indique quand le nouveau tour commence !

	def ivy__game_turn_draw_card(self, agent, gamehost_name):
		if self.name == gamehost_name:
			if agent in self.players:
				self.on_player_draw_card(agent.agent_name)

	def ivy__game_turn_card_drawn(self, agent, client_name, card_desc):
		pass  # Rien à gérer dans le cas d'un serveur, c'est lui qui envoie la carte qui a été tirée par un client !

	def ivy__game_turn_won(self, agent, winner_name):
		pass  # Rien à gérer dans le cas d'un serveur, c'est lui qui indique quand un tour est gagné !

	def ivy__game_turn_battle(self, agent, battle_members_names, _):
		pass  # Rien à gérer dans le cas d'un serveur, c'est lui qui indique quand une bataille a lieu !

	def ivy__game_turn_card_pick(self, agent, gamehost_name, card_desc):
		if self.name == gamehost_name:
			if agent in self.players:
				self.on_player_picked_card(agent.agent_name, card_desc)

	def ivy__game_won(self, agent, winner_name):
		pass  # Rien à gérer dans le cas d'un serveur, c'est lui qui décide quand la partie est gagnée !

	def ivy__game_par(self, agent, winners_names, _):
		pass  # Rien à gérer dans le cas d'un serveur, c'est lui qui décide quand la partie est un match nul !
