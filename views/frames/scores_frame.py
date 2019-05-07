from tkinter import *


class ScoresFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.result = StringVar(value="Vous avez perdu.")
        self.message = Label(self, textvariable=self.result, font=("Helvetica", 30), fg='lightblue')
        self.message.pack(side="top", pady=(60, 30))

        self.winner_name_label_var = StringVar(value="")
        self.winner_name_label = Label(self, textvariable=self.winner_name_label_var, font=("Helvetica", 16))
        self.winner_name_label.pack(side="top", pady=(0, 30))

        Button(self, text="Quitter", command=master.stop).pack()

    def init(self):
        if len(self.master.winners) == 1:
            if self.master.winners[0] == self.master.player_name:
                self.result.set("Vous avez gagné !")
                self.message.config(fg='gold')
            else:
                self.winner_name_label_var.set(self.master.winners[0] + " a gagné !")
        else:
            if self.master.player_name in self.master.winners:
                self.result.set("Égalité !")
                self.message.config(fg='orange')
            
            winners_label_content = "Les gagnants sont : "
            for winner_name in self.master.winners:
                winners_label_content += winner_name + ", "
            self.winner_name_label_var.set(winners_label_content[:-2])

