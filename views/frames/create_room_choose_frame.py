import random
from tkinter import *


class CreateRoomChooseFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        def on_create_room():
            if len(self.entry.get()) > 0:
                self.master.room_name = self.entry.get()
                self.master.raise_frame('create_room_wait')

        Label(self, text="Choisissez un nom de salon :", font=("Helvetica", 18)).pack(side="top", pady=20)

        self.entry = Entry(self)
        self.entry.pack(pady=15)

        Checkbutton(self, text="Partie rapide", variable=self.master.shortRule).pack()
        Checkbutton(self, text="Sans cartes retournées en bataille", variable=self.master.noCardUpsideDown)\
            .pack()

        Button(self, text="Créer le salon", command=on_create_room).pack(pady=(15, 3))
        Button(self, text="Retour au menu", command=lambda: master.raise_frame('start')).pack(pady=3)

    def init(self):
        self.entry.delete(0, END)
        self.entry.insert(0, "Salon#" + str(random.randint(1000, 9999)))
