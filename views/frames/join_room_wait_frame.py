import time
from tkinter import *

from model.battle import ClientBattle


class JoinRoomWaitFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.label = Label(self, font=("Helvetica", 18))
        self.label.pack(side="top", pady=20)

        self.players = Listbox(self)
        self.players.pack(pady=15)

        Label(self, text="En attente d'autres joueurs...").pack(pady=3)

    def init(self):
        def on_players_list_updated(players_names):
            self.players.delete(0, END)
            self.players.insert(0, self.master.handler.name + ' (vous)')
            for name in players_names:
                self.players.insert(END, name)

        def on_game_begin():
            print('== Game begins!')
            self.master.battle = ClientBattle(self.master.handler)
            time.sleep(1)
            self.master.raise_frame('game')

        self.master.handler.on_players_list_updated = on_players_list_updated
        self.master.handler.on_game_begin = on_game_begin

        self.label['text'] = self.master.room_name
