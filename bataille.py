import time

from model.battle import *
from model.gamehandler.battle_game_server import BattleGameServer


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
	global nbreDeTours
	print("Nouveau joueur : " + player_name)
	if len(server.players) == 2:
		server.game_begin()
		print("La partie a commencé.")
		time.sleep(0.5)
		nbreDeTours += 1
		server.game_new_turn()
		print("Premier tour.")


nbreDeTours = 0
server = BattleGameServer("TEST")
server.on_new_player = on_new_player
server.run()
