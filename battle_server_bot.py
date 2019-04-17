from battle_bot import BattleBot
from model.battle import *
from model.nethandler.battle_net_server import BattleNetServer

PLAYERS_NUMBER = 4  # Nombre de joueurs à partir duquel on doit lancer la partie.


def on_new_player(player_name):
	"""
	Lancé lorsqu'un nouveau joueur rejoint la partie.
	:param player_name: Le nom du joueur ayant rejoint.
	"""
	global server, serverBattle
	print("Nouveau joueur : " + player_name)
	if len(server.players) == PLAYERS_NUMBER-1:  # Le nombre de joueurs est suffisant pour lancer la partie.
		# Création de l'objet de jeu et de la classe de gestion de la partie des robots.
		serverBattle = BattleBot(ServerBattle(server, False))
		# On tire une carte dans cette fonction car les callbacks n'ont été définis qu'après le lancement du premier tour.
		serverBattle.battle.draw_card()


serverBattle = None  # Classe du jeu de la bataille.
server = BattleNetServer("SERVER_BOT")  # NetHandler.
# Affectation des callbacks.
server.on_new_player = on_new_player
server.run()
