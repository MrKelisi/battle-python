import time
from tkinter import *
from model.gamehandler.battle_game_server import BattleGameServer


class CreateRoomWaitFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        def on_play():
            if self.nb_players > 1:
                self.master.handler.game_begin()
                print('== Game begins!')
                self.master.handler.game_new_turn()
                print('== New turn!')
                self.master.raise_frame('game')

        self.nb_players = 1

        self.label = Label(self, font=("Helvetica", 18))
        self.label.pack(side="top", pady=20)

        self.players = Listbox(self)
        self.players.pack(pady=15)

        Button(self, text="Jouer", command=on_play).pack(pady=3)

    def init(self):
        def on_new_player(player_name):
            print(player_name + " joined the room!")
            self.nb_players += 1
            self.players.insert('end', player_name)

        if self.master.handler is not None:
            self.master.handler.stop()
            time.sleep(0.1)

        self.master.handler = BattleGameServer(self.master.room_name, self.master.player_name)
        self.master.handler.on_new_player = on_new_player
        self.master.handler.run()

        time.sleep(0.1)
        self.master.handler.room()

        self.label['text'] = self.master.room_name
        self.players.insert(0, self.master.handler.name + ' (vous)')
