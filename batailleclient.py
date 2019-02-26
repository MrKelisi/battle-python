import time

from model.battle import *
from model.gamehandler.battle_game_client import BattleGameClient


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


def room_found(gamehost_name, room_name):
	global connected
	print("Salle : " + room_name + " sur " + gamehost_name + ".")
	if not connected:
		client.connect_room(gamehost_name)
		connected = True


def players_list(players_names):
	print("Joueurs dans la partie : " + str(players_names))

def game_begin():
	print("Le jeu a commencé.")

def game_new_turn():
	global nbreDeTours
	nbreDeTours += 1
	print("Le tour a " + str(nbreDeTours) + " commencé.")


connected = False
nbreDeTours = 0
client = BattleGameClient()
client.on_new_room = room_found
client.on_players_list_updated = players_list
client.on_game_begin = game_begin
client.on_game_new_turn = game_new_turn
client.run()

time.sleep(1)

client.find_rooms()
