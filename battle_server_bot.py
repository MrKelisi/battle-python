from model.battle import *
from model.nethandler.battle_net_server import BattleNetServer

PLAYERS_NUMBER = 4


def cmd_tests():
	print(all_french_cards())

	decks = create_decks(4)
	for deck in decks:
		print("deck of", deck.number_of_cards(), "cards")
		print(deck)

	print()
	c1 = decks[0].draw()
	c2 = decks[1].draw()
	c3 = decks[2].draw()
	c4 = decks[2].draw()

	print(c1, "VS", c2, "VS", c3, "VS", c4)
	print(c1.get_rank().value, "VS", c2.get_rank().value, "VS", c3.get_rank().value, "VS", c4.get_rank().value)
	print("Winner(s):", compare_cards([c1, c2, c3, c4]))


def on_new_player(player_name):
	global nbreDeTours, server, battleServer
	print("Nouveau joueur : " + player_name)
	if len(server.players) == PLAYERS_NUMBER-1:
		battleServer = ServerBattle(server, False)
		battleServer.on_new_turn = game_new_turn
		battleServer.on_battle = game_turn_battle
		battleServer.on_turn_finished = game_turn_finished
		battleServer.on_turn_par = game_turn_par
		battleServer.on_game_won = game_won
		battleServer.on_game_par = game_par
		battleServer.draw_card()


def game_new_turn():
	global battleServer
	if battleServer.is_game_ended:
		print("Jeu terminé pour moi, points des autres : " + str(battleServer.others_points()))
	else:
		print("Mes points : " + str(battleServer.my_points()))
		print("Points des autres : " + str(battleServer.others_points()))
		battleServer.draw_card()


def game_turn_battle(in_battle, other_members_names):
	global battleServer
	if in_battle:
		print("Bataille : je suis dedans !")
		battleServer.draw_card()
		battleServer.draw_card()
	else:
		print("Bataille : je ne suis pas dedans.")


def game_turn_finished(winner_name):
	global battleServer
	if winner_name is None:
		print("J'ai gagné ce tour !")
		for card in battleServer.my_cards_to_pick():
			battleServer.pick_card(card)
	else:
		print(winner_name + " a gagné ce tour.")


def game_turn_par():
	global battleServer
	print("Égalité ! Tout le monde récupère les cartes jouées.")
	for card in battleServer.my_cards_to_pick():
		battleServer.pick_card(card)


def game_won(winner_name):
	print("Le gagnant est " + winner_name + " ! Bravo !")


def game_par(winners_names):
	print("Égalité, il y a plusieurs gagnants : " + winners_names)


battleServer = None
server = BattleNetServer("SERVER_BOT")
server.on_new_player = on_new_player
server.run()
