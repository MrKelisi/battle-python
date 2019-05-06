import logging
from abc import abstractmethod

from ivy.ivy import ivylogger, IvyServer


class BattleNetHandler(IvyServer):
	def __init__(self, name):
		ivylogger.setLevel(logging.WARN)
		self.name = name
		IvyServer.__init__(self, self.name)

	def run(self):
		self.start("127:2134")

		# find_rooms.
		self.bind_msg(self.ivy__find_rooms, "find_rooms\\.")
		# room: [room_name], [short_rule], [no_card_upside_down].
		self.bind_msg(self.ivy__room, "room: ([^,.]+), (true|false), (true|false)\\.")
		# connect_room: [gamehost_name].
		self.bind_msg(self.ivy__connect_room, "connect_room: ([^,.]+)\\.")
		# room_is_full.
		self.bind_msg(self.ivy__room_is_full, "room_is_full\\.")
		# accept_player [player_name].
		self.bind_msg(self.ivy__accept_player, "accept_player: ([^,.]+)\\.")
		# players_list [[player_name], [...]].
		self.bind_msg(self.ivy__players_list, "players_list: \\[(([^,.]+, )+)\\]\\.")

		# game_begin [short_rule], [no_card_upside_down].
		self.bind_msg(self.ivy__game_begin, "game_begin (true|false), (true|false)\\.")

		# game_new_turn.
		self.bind_msg(self.ivy__game_new_turn, "game_new_turn\\.")
		# game_turn_draw_card [gamehost_name].
		self.bind_msg(self.ivy__game_turn_draw_card, "game_turn_draw_card: ([^,.]+)\\.")
		# game_turn_card_drawn [player_name], [card_desc].
		self.bind_msg(self.ivy__game_turn_card_drawn, "game_turn_card_drawn: ([^,.]+), ([^,.]+)\\.")
		# game_turn_battle [[player_name], [...]].
		self.bind_msg(self.ivy__game_turn_battle, "game_turn_battle: \\[(([^,.]+, )+)\\].")
		# game_turn_won [player_name].
		self.bind_msg(self.ivy__game_turn_won, "game_turn_won: ([^,.]+)\\.")
		# game_turn_par.
		self.bind_msg(self.ivy__game_turn_par, "game_turn_par\\.")
		# game_turn_card_pick [gamehost_name], [card_desc].
		self.bind_msg(self.ivy__game_turn_card_pick, "game_turn_card_pick: ([^,.]+), ([^,.]+)\\.")

		# game_ended [player_name].
		self.bind_msg(self.ivy__game_ended, "game_ended: ([^,.]+)\\.")
		# game_won [winner_name].
		self.bind_msg(self.ivy__game_won, "game_won: ([^,.]+)\\.")
		# game_par [[winner_name], [...]].
		self.bind_msg(self.ivy__game_par, "game_par: \\[(([^,.]+, )+)\\]\\.")

	def handle_new_client(self, client):
		IvyServer.handle_new_client(self, client)

		found = False
		for c in self.get_clients():
			if client.agent_name == c:
				if found:
					client.send_die_message()  # Un autre client avec le même nom existe déjà.
				else:
					found = True

	@abstractmethod
	def ivy__find_rooms(self, agent):
		pass

	@abstractmethod
	def ivy__room(self, agent, room_name, short_rule, no_card_upside_down):
		pass

	@abstractmethod
	def ivy__connect_room(self, agent, gamehost_name):
		pass

	@abstractmethod
	def ivy__room_is_full(self, agent):
		pass

	@abstractmethod
	def ivy__accept_player(self, agent, player_name):
		pass

	@abstractmethod
	def ivy__players_list(self, agent, players_names, _):
		pass

	@abstractmethod
	def ivy__game_begin(self, agent, short_rule, no_card_upside_down):
		pass

	@abstractmethod
	def ivy__game_new_turn(self, agent):
		pass

	@abstractmethod
	def ivy__game_turn_draw_card(self, agent, gamehost_name):
		pass

	@abstractmethod
	def ivy__game_turn_card_drawn(self, agent, client_name, card_desc):
		pass

	@abstractmethod
	def ivy__game_turn_battle(self, agent, battle_members_names, _):
		pass

	@abstractmethod
	def ivy__game_turn_won(self, agent, winner_name):
		pass

	@abstractmethod
	def ivy__game_turn_par(self, agent):
		pass

	@abstractmethod
	def ivy__game_turn_card_pick(self, agent, gamehost_name, card_desc):
		pass

	@abstractmethod
	def ivy__game_ended(self, agent, player_name):
		pass

	@abstractmethod
	def ivy__game_won(self, agent, winner_name):
		pass

	@abstractmethod
	def ivy__game_par(self, agent, winners_names, _):
		pass
