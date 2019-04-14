from tkinter import *


class StartFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        Label(self, text="Bataille !", font=("Helvetica", 24)).pack(side="top", pady=20)
        Button(self, text="Créer un salon", command=lambda: master.raise_frame('create_room_choose')).pack(pady=3)
        Button(self, text="Rejoindre un salon", command=lambda: master.raise_frame('join_room_choose')).pack(pady=3)

    def init(self):
        pass
