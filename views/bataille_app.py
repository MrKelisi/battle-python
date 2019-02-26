from tkinter import *

from model.battle import Battle
from views.image_factory import ImageFactory


class BatailleApp(Tk):
	WIDTH = 800
	HEIGHT = 500

	def __init__(self):
		Tk.__init__(self)
		self.title("Bataille")
		self.geometry("{}x{}".format(self.WIDTH, self.HEIGHT))
		self._frame = None
		self._battle = None
		self.replace_frame(StartPage)

	def replace_frame(self, frame_class):
		new_frame = frame_class(self)
		if self._frame is not None:
			self._frame.destroy()
		self._frame = new_frame
		self._frame.pack(fill="both", expand=True)


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

		Label(self, text="Créer un salon").pack(side="top")
		Listbox(self).pack()
		Button(self, text="Jouer", command=launch_game).pack()
		Button(self, text="Retour au menu", command=lambda: master.replace_frame(StartPage)).pack()


class JoinRoomPage(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)

		Label(self, text="Rejoindre un salon").pack(side="top")
		e1 = Entry(self)
		e1.insert(0, "127.0.0.0:2010")
		e1.pack()

		Listbox(self).pack()
		Button(self, text="Retour au menu", command=lambda: master.replace_frame(StartPage)).pack()


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

		self._paquet = Label(self, image=back_img, bg="darkblue")
		self._paquet.image = back_img
		self._paquet.place(x=BatailleApp.WIDTH/2, y=BatailleApp.HEIGHT, anchor=CENTER)

		self._paquet.bind('<ButtonRelease-1>', self.release_paquet)
		self._paquet.bind('<B1-Motion>', self.drag_paquet)

		self.__label_player_self = Label(self, text="Vous ({} cartes)".format(self._battle.nb_cards(0)), fg="white", bg="darkblue")
		self.__label_player_self.place(x=5, y=BatailleApp.HEIGHT - 5, anchor=SW)

		self.__label_player_2 = Label(self, text="Joueur 2 ({} cartes)".format(self._battle.nb_cards(1)), fg="white", bg="darkblue")
		self.__label_player_2.place(x=5, y=5, anchor=NW)

		self.__label_player_3 = Label(self, text="Joueur 3 ({} cartes)".format(self._battle.nb_cards(1)), fg="white", bg="darkblue")
		self.__label_player_3.place(x=BatailleApp.WIDTH/2, y=5, anchor=N)

		self.__label_player_4 = Label(self, text="Joueur 4 ({} cartes)".format(self._battle.nb_cards(1)), fg="white", bg="darkblue")
		self.__label_player_4.place(x=BatailleApp.WIDTH - 5, y=5, anchor=NE)

	def release_paquet(self, evt):

		if True:  # si carte dans la zone de dépot
			draw = self._battle.draw()
			print("{}".format(draw))

			draw_img = ImageFactory.instance.get_c(draw[0])
			x, y = self._paquet.winfo_x() - 13, self._paquet.winfo_y() - 30
			id = self.__drop_zone.create_image((x, y), image=draw_img, anchor=NW)
			self.__drop_zone.imagestk[id] = draw_img

			self._paquet.place(x=BatailleApp.WIDTH/2, y=BatailleApp.HEIGHT)

			self.__label_player_self.config(text="Vous ({} cartes)".format(self._battle.nb_cards(0)))

	def drag_paquet(self, evt):
		x, y = self.winfo_pointerx() - self.master.winfo_rootx(), self.winfo_pointery() - self.master.winfo_rooty()
		self._paquet.place(x=x, y=y, anchor=CENTER)


if __name__ == "__main__":
	app = BatailleApp()
	app.mainloop()
