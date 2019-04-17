from model.battle import *
from model.nethandler.battle_net_client import BattleNetClient


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
	global client, battleClient
	print("Le jeu a commencé.")
	battleClient = ClientBattle(client)
	battleClient.on_new_turn = game_new_turn
	battleClient.on_battle = game_turn_battle
	battleClient.on_turn_finished = game_turn_finished
	battleClient.on_turn_par = game_turn_par
	battleClient.on_game_won = game_won
	battleClient.on_game_par = game_par


def game_new_turn():
	global battleClient
	if battleClient.is_game_ended:
		print("Jeu terminé pour moi, points des autres : " + str(battleClient.others_points()))
	else:
		print("Mes points : " + str(battleClient.my_points()))
		print("Points des autres : " + str(battleClient.others_points()))
		battleClient.draw_card()


def game_turn_battle(in_battle, other_members_names):
	global battleClient
	if in_battle:
		print("Bataille : je suis dedans !")
		battleClient.draw_card()
		battleClient.draw_card()
	else:
		print("Bataille : je ne suis pas dedans.")


def game_turn_finished(winner_name):
	global battleClient
	if winner_name is None:
		print("J'ai gagné ce tour !")
		for card in battleClient.my_cards_to_pick():
			battleClient.pick_card(card)
	else:
		print(winner_name + " a gagné ce tour.")


def game_turn_par():
	global battleClient
	print("Égalité ! Tout le monde récupère les cartes jouées.")
	for card in battleClient.my_cards_to_pick():
		battleClient.pick_card(card)


def game_won(winner_name):
	print("Le gagnant est " + winner_name + " ! Bravo !")


def game_par(winners_names):
	print("Égalité, il y a plusieurs gagnants : " + winners_names)


connected = False
battleClient = None
client = BattleNetClient()
client.on_new_room = room_found
client.on_players_list_updated = players_list
client.on_game_begin = game_begin
client.run()

time.sleep(1)

client.find_rooms()
