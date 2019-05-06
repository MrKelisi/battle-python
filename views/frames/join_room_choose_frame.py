import time
from tkinter import *
from tkinter import ttk

from model.nethandler.battle_net_client import BattleNetClient


class JoinRoomChooseFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        def on_room_selected(evt):
            table_item = self.tableview.item(self.tableview.selection()[0])
            self.master.room_name = table_item["text"]
            # Le dernier élément de la liste des valeurs est le nom de l'hébergeur de la partie.
            self.master.handler.connect_room(table_item["values"][len(table_item["values"]) - 1])

        self.rooms = dict()

        Label(self, text="Choisissez un salon", font=("Helvetica", 18)).pack(side="top", pady=20)

        Label(self, text="Double cliquez sur un salon pour entrer dans la partie.", font=("Helvetica", 12)).pack(side="top")

        self.tableview = ttk.Treeview(self, columns=("rule_type", "card_upside_down"))

        self.tableview.heading("#0", text="Nom")
        self.tableview.column("#0", width=200)
        self.tableview.heading("rule_type", text="Type de partie")
        self.tableview.column("rule_type", width=150)
        self.tableview.heading("card_upside_down", text="Carte retournée dans la bataille")
        self.tableview.column("card_upside_down", width=300)

        self.tableview.pack(pady=15)
        self.tableview.bind("<Double-1>", on_room_selected)

        Button(self, text="Rafraîchir", command=lambda: master.handler.find_rooms()).pack(pady=3)

        Button(self, text="Retour au menu", command=lambda: master.raise_frame('start')).pack(pady=3)

        self.error = Label(self, fg='red')
        self.error.pack(pady=3)

    def __show_table_view_content(self):
        self.tableview.delete(*self.tableview.get_children())
        for room_gamehost_name in self.rooms.keys():
            room_data = self.rooms[room_gamehost_name]
            self.tableview.insert("", END, text=room_data[0],  # name
                                  values=("Courte" if room_data[1] else "Longue",  # rule_type
                                          "Non" if room_data[2] else "Oui",  # card_upside_down
                                          # Le dernier élément de la liste des valeurs est le nom de l'hébergeur de la partie.
                                          room_gamehost_name))

    def init(self):
        def on_new_room(gamehost_name, room_name, short_rule, no_card_upside_down):
            self.rooms[gamehost_name] = (room_name, short_rule, no_card_upside_down)
            self.__show_table_view_content()

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
