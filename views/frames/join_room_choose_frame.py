import time
from tkinter import *

from model.nethandler.battle_net_client import BattleNetClient


class JoinRoomChooseFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        def on_room_selected(evt):
            index = int(self.listbox.curselection()[0])
            self.master.room_name = self.listbox.get(index)
            master.handler.connect_room(self.rooms[self.master.room_name])

        self.rooms = dict()

        Label(self, text="Choisissez un salon :", font=("Helvetica", 18)).pack(side="top", pady=20)

        self.listbox = Listbox(self)
        self.listbox.pack(pady=15)
        self.listbox.bind('<ButtonRelease-1>', on_room_selected)

        Button(self, text="Rafraîchir", command=lambda: master.handler.find_rooms()).pack(pady=3)

        Button(self, text="Retour au menu", command=lambda: master.raise_frame('start')).pack(pady=3)

        self.error = Label(self, fg='red')
        self.error.pack(pady=3)

    def init(self):
        def on_new_room(gamehost_name, room_name):
            self.rooms[room_name] = gamehost_name
            self.listbox.delete(0, END)
            self.listbox.insert(END, *self.rooms.keys())

        def on_room_connection_accepted():
            self.master.raise_frame('join_room_wait')

        def on_room_connection_failed():
            self.error['text'] = "Salon plein !"

        if self.master.handler is not None:
            self.master.handler.stop()
            time.sleep(0.1)

        self.master.handler = BattleNetClient(self.master.player_name)
        self.master.handler.on_new_room = on_new_room
        self.master.handler.on_room_connection_accepted = on_room_connection_accepted
        self.master.handler.on_room_connection_failed = on_room_connection_failed
        self.master.handler.run()

        time.sleep(0.1)
        self.master.handler.find_rooms()
