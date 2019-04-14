import random
from tkinter import *


class PlayerFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        def on_validate():
            if len(self.entry.get()) > 0:
                self.master.player_name = self.entry.get()
                self.master.raise_frame('start')

        Label(self, text="Entrez votre nom :", font=("Helvetica", 18)).pack(side="top", pady=20)

        self.entry = Entry(self)
        self.entry.pack(pady=15)

        Button(self, text="Valider", command=on_validate).pack(pady=3)

    def init(self):
        self.entry.insert(0, "Player#" + str(random.randint(1000, 9999)))
