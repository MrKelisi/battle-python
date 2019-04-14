import time
from model.gamehandler.battle_game_handler import BattleGameHandler


def default_callback(*args):
	pass


class BattleGameClient(BattleGameHandler):
	def __init__(self, name="client#" + str(round(time.time()*1000))):
		self.players_names = []

		self.on_new_room = default_callback  # gamehost_name, room_name
		self.on_room_is_full = default_callback  # gamehost_name
		self.on_another_game_begin = default_callback  # gamehost_name
		self.on_room_connection_accepted = default_callback  #
		self.on_room_connection_failed = default_callback  #

		self.on_game_begin = default_callback  #
		self.on_game_new_turn = default_callback  #

		self.on_players_list_updated = default_callback  # players_names
		self.on_my_card_drawn = default_callback  # card_desc
		self.on_player_card_drawn = default_callback  # client_name, card_desc
		self.on_turn_battle_with = default_callback  # in_battle, others_battle_members
		self.on_turn_finished = default_callback  # winner_name

		self.on_player_picked_card = default_callback  # client_name, card_desc

		self.on_game_won = default_callback  #
		self.on_game_lost = default_callback  # winner_name
		self.on_game_par = default_callback  # winners_names

		self.__connecting_to_room = None
		self.__connected_to_room = None

		BattleGameHandler.__init__(self, name)

	# Envoi de messages. #

	def find_rooms(self):
		self.send_msg("find_rooms.")

	def connect_room(self, gamehost_name):
		self.__connecting_to_room = gamehost_name
		self.send_msg("connect_room: " + gamehost_name + ".")

	def game_turn_draw_card(self):
		self.send_msg("game_turn_draw_card: " + self.__connected_to_room + ".")

	def game_turn_card_pick(self, card_desc):
		self.send_msg("game_turn_card_pick: " + self.__connected_to_room + ", " + card_desc + ".")

	# Réception de messages. #

	def ivy__find_rooms(self, agent):
		pass  # Rien à gérer dans le cas d'un client, c'est lui qui demande quelles sont les salles voisines.

	def ivy__room(self, agent, room_name):
		self.on_new_room(agent.agent_name, room_name)

	def ivy__connect_room(self, agent, gamehost_name):
		pass  # Rien à gérer dans le cas d'un client, c'est lui qui envoie les demandes de connexion à une salle.

	def ivy__room_is_full(self, agent):
		if self.__connecting_to_room == agent.agent_name:
			self.on_room_connection_failed()
			self.__connecting_to_room = None
		self.on_room_is_full(agent.agent_name)

	def ivy__accept_player(self, agent, player_name):
		if self.name == player_name and self.__connecting_to_room == agent.agent_name:
			self.__connecting_to_room = None
			self.__connected_to_room = agent.agent_name
			self.on_room_connection_accepted()

	def ivy__players_list(self, agent, players_names, _):
		if self.__connected_to_room == agent.agent_name:
			self.players_names.clear()
			players_names = players_names.split(", ")[:-1]
			for player_name in players_names:
				if self.name != player_name:
					self.players_names.append(player_name)
			self.on_players_list_updated(self.players_names)

	def ivy__game_begin(self, agent):
		if self.__connected_to_room == agent.agent_name:
			self.on_game_begin()
		else:
			self.on_another_game_begin(agent.agent_name)

	def ivy__game_new_turn(self, agent):
		if self.__connected_to_room == agent.agent_name:
			self.on_game_new_turn()

	def ivy__game_turn_draw_card(self, agent, gamehost_name):
		pass  # Rien à gérer dans le cas d'un client, c'est lui qui envoie le moment où il tire une carte.

	def ivy__game_turn_card_drawn(self, agent, client_name, card_desc):
		if self.__connected_to_room == agent.agent_name:
			if self.name == client_name:
				self.on_my_card_drawn(card_desc)
			else:
				self.on_player_card_drawn(client_name, card_desc)

	def ivy__game_turn_won(self, agent, winner_name):
		if self.__connected_to_room == agent.agent_name:
			self.on_turn_finished(winner_name)

	def ivy__game_turn_battle(self, agent, battle_members_names, _):
		if self.__connected_to_room == agent.agent_name:
			others_member_names = []
			in_battle = False
			battle_members_names = battle_members_names.split(", ")[:-1]
			for battle_member_name in battle_members_names:
				if self.name == battle_member_name:
					in_battle = True
				else:
					others_member_names.append(battle_member_name)
			self.on_turn_battle_with(in_battle, others_member_names)

	def ivy__game_turn_card_pick(self, agent, gamehost_name, card_desc):
		if self.__connected_to_room == gamehost_name:
			if agent.agent_name in self.players_names:
				self.on_player_picked_card(agent.agent_name, card_desc)

	def ivy__game_won(self, agent, winner_name):
		if self.__connected_to_room == agent.agent_name:
			if self.name == winner_name:
				self.on_game_won()
			else:
				self.on_game_lost(winner_name)

	def ivy__game_par(self, agent, winners_names, _):
		if self.__connected_to_room == agent.agent_name:
			self.on_game_par(winners_names.split(", ")[:-1])
