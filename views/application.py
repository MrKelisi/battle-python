from tkinter import *
from views.frames.player_frame import PlayerFrame
from views.frames.start_frame import StartFrame
from views.frames.create_room_choose_frame import CreateRoomChooseFrame
from views.frames.create_room_wait_frame import CreateRoomWaitFrame
from views.frames.join_room_choose_frame import JoinRoomChooseFrame
from views.frames.join_room_wait_frame import JoinRoomWaitFrame
from views.frames.game_frame import GameFrame


class Application(Tk):
    WIDTH = 800
    HEIGHT = 500

    def __init__(self):
        Tk.__init__(self)
        self.title("Bataille")
        self.geometry("{}x{}".format(self.WIDTH, self.HEIGHT))

        self.frames = dict()
        self.frames['player'] = PlayerFrame(self)
        self.frames['start'] = StartFrame(self)
        self.frames['create_room_choose'] = CreateRoomChooseFrame(self)
        self.frames['create_room_wait'] = CreateRoomWaitFrame(self)
        self.frames['join_room_choose'] = JoinRoomChooseFrame(self)
        self.frames['join_room_wait'] = JoinRoomWaitFrame(self)
        self.frames['game'] = GameFrame(self)

        for name, frame in self.frames.items():
            frame.place(x=0, y=0, width=self.WIDTH, height=self.HEIGHT)

        self.raise_frame('player')

        self.handler = None
        self.room_name = ""
        self.player_name = ""

    def stop(self):
        if self.handler is not None:
            self.handler.stop()

    def raise_frame(self, name):
        self.frames[name].init()
        self.frames[name].tkraise()


def on_closing():
    app.stop()
    app.destroy()


if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
