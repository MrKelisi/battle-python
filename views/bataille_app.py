import time

from tkinter import *

from model.battle import Battle
from views.image_factory import ImageFactory
from model.gamehandler.battle_game_server import BattleGameServer
from model.gamehandler.battle_game_client import BattleGameClient


class BatailleApp(Tk):
	WIDTH = 800
	HEIGHT = 500

	def __init__(self):
		Tk.__init__(self)
		self.title("Bataille")
		self.geometry("{}x{}".format(self.WIDTH, self.HEIGHT))
		self._frame = None
		self._battle = None
		self._server = None
		self._client = None
		self._connected = False
		self.replace_frame(StartPage)

	def replace_frame(self, frame_class):
		new_frame = frame_class(self)
		if self._frame is not None:
			self._frame.destroy()
		self._frame = new_frame
		self._frame.pack(fill="both", expand=True)

	def close(self):
		if self._server:
			self._server.stop()
		if self._client:
			self._client.stop()


class StartPage(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)

		Label(self, text="Bataille !").pack(side="top")
		Button(self, text="Créer un salon", command=lambda: master.replace_frame(CreateRoomPage)).pack()
		Button(self, text="Rejoindre un salon", command=lambda: master.replace_frame(JoinRoomPage)).pack()


class CreateRoomPage(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)

		def launch_game():
			master._battle = Battle(2)  # Number of people in the room
			master.replace_frame(GamePage)

		def on_new_player(player_name):
			self.__list_players.insert('end', player_name)

		Label(self, text="Créer un salon").pack(side="top")
		self.__list_players = Listbox(self)
		self.__list_players.pack()
		Button(self, text="Jouer", command=launch_game).pack()
		Button(self, text="Retour au menu", command=lambda: master.replace_frame(StartPage)).pack()

		master._server = BattleGameServer("Room")
		master._server.on_new_player = on_new_player
		master._server.run()


class JoinRoomPage(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)

		def room_found(gamehost_name, room_name):
			print("Salle : " + room_name + " sur " + gamehost_name + ".")
			if not master._connected:
				master._client.connect_room(gamehost_name)
				master._connected = True

		def players_list_updated(players_names):
			self.__list_players.delete(0, 'end')
			for name in players_names:
				self.__list_players.insert('end', name)

		Label(self, text="Rejoindre un salon").pack(side="top")
		e1 = Entry(self)
		e1.insert(0, "127.0.0.0:2010")
		e1.pack()

		self.__list_players = Listbox(self)
		self.__list_players.pack()
		Button(self, text="Retour au menu", command=lambda: master.replace_frame(StartPage)).pack()

		master._client = BattleGameClient()
		master._client.on_new_room = room_found
		master._client.on_players_list_updated = players_list_updated
		master._client.run()
		master._client.find_rooms()


class GamePage(Frame):
	def __init__(self, master):
		Frame.__init__(self, master, bg="darkblue")

		if master._battle is not None:
			self._battle = master._battle

		self.__drop_zone = Canvas(self, width=BatailleApp.WIDTH - 30, height=BatailleApp.HEIGHT*2/3, bg="darkblue", relief="solid")
		self.__drop_zone.place(x=13, y=30, anchor=NW)
		self.__drop_zone.imagestk = dict()

		back_img = ImageFactory.instance.get_back()
		self.__image_deck = Label(self, image=back_img, bg="darkblue")
		self.__image_deck.image = back_img
		self.__image_deck.place(x=BatailleApp.WIDTH/2, y=BatailleApp.HEIGHT, anchor=CENTER)

		self.__top_card = Label(self, image=back_img, bg="darkblue")
		self.__top_card.image = back_img
		self.__top_card.place(x=BatailleApp.WIDTH/2, y=BatailleApp.HEIGHT, anchor=CENTER)
		self.__top_card.bind('<ButtonRelease-1>', self.release_top_card)
		self.__top_card.bind('<B1-Motion>', self.drag_top_card)

		self.__label_player_self = Label(self, text="Vous ({} cartes)".format(self._battle.nb_cards(0)), fg="white", bg="darkblue")
		self.__label_player_self.place(x=5, y=BatailleApp.HEIGHT - 5, anchor=SW)

		self.__label_player_2 = Label(self, text="Joueur 2 ({} cartes)".format(self._battle.nb_cards(1)), fg="white", bg="darkblue")
		self.__label_player_2.place(x=5, y=5, anchor=NW)

		self.__label_player_3 = Label(self, text="Joueur 3 ({} cartes)".format(self._battle.nb_cards(1)), fg="white", bg="darkblue")
		self.__label_player_3.place(x=BatailleApp.WIDTH/2, y=5, anchor=N)

		self.__label_player_4 = Label(self, text="Joueur 4 ({} cartes)".format(self._battle.nb_cards(1)), fg="white", bg="darkblue")
		self.__label_player_4.place(x=BatailleApp.WIDTH - 5, y=5, anchor=NE)

	def release_top_card(self, evt):

		if True:  # TODO: si carte dans la zone de dépot
			draw = self._battle.draw()
			print("{}".format(draw))

			draw_img = ImageFactory.instance.get_c(draw[0])
			x, y = self.__top_card.winfo_x() - 13, self.__top_card.winfo_y() - 30
			id = self.__drop_zone.create_image((x, y), image=draw_img, anchor=NW)
			self.__drop_zone.imagestk[id] = draw_img

			self.__top_card.place(x=BatailleApp.WIDTH/2, y=BatailleApp.HEIGHT)

			self.__label_player_self.config(text="Vous ({} cartes)".format(self._battle.nb_cards(0)))

	def drag_top_card(self, evt):
		x, y = self.winfo_pointerx() - self.master.winfo_rootx(), self.winfo_pointery() - self.master.winfo_rooty()
		self.__top_card.place(x=x, y=y, anchor=CENTER)


def on_closing():
	app.close()
	app.destroy()


if __name__ == "__main__":
	app = BatailleApp()
	app.protocol("WM_DELETE_WINDOW", on_closing)
	app.mainloop()
