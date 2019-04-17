from battle_bot import BattleBot
from model.battle import *
from model.nethandler.battle_net_client import BattleNetClient


def room_found(gamehost_name, room_name):
	"""
	Lancé lorsqu'une salle a été trouvée. Si on n'est pas déjà connecté à une salle, on tente de s'y connecter.
	:param gamehost_name: Nom de l'hôte de la salle de jeu.
	:type gamehost_name: str
	:param room_name: Nom de la salle.
	:type room_name: str
	"""
	global connected
	print("Salle : " + room_name + " sur " + gamehost_name + ".")
	if not connected:  # On n'est pas connecté, on tente donc de s'y connecter.
		client.connect_room(gamehost_name)
		connected = True


def players_list(players_names):
	"""
	Lancé lorsque la liste des joueurs dans la partie est reçue (habituellement, lorsqu'un nouveau joueur rejoint la partie).
	:param players_names: Noms des joueurs dans la partie.
	:type players_names: str
	"""
	print("Joueurs dans la partie : " + str(players_names))


def game_begin():
	"""
	Lancé lorsque la partie commence.
	On crée l'objet de jeu et on lui affecte les callbacks.
	"""
	global client, clientBattle
	print("Le jeu a commencé.")

	# Création de l'objet de jeu et de la classe de gestion de la partie des robots.
	clientBattle = BattleBot(ClientBattle(client))


connected = False
clientBattle = None
client = BattleNetClient()
client.on_new_room = room_found
client.on_players_list_updated = players_list
client.on_game_begin = game_begin
client.run()

time.sleep(1)

client.find_rooms()
