from tkinter import *

from model.nethandler.battle_net_client import BattleNetClient
from model.nethandler.battle_net_server import BattleNetServer
from views.image_factory import ImageFactory


class GameFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='darkblue')
        # self.master.wm_attributes('-transparentcolor', 'lime')

        self.nb_players = 2

        self.can_draw = True
        self.can_pick_mine = False
        self.can_pick_all = False
        self.on_par = False
        self.in_battle = False
        self.game_ended = False

        self.battle_stage = [0, 0, 0, 0]
        self.players = []

        self._coords_x = [150, 390, 520, 650]
        self._coords_y = [75, 100, 285]

        self._sheet = Canvas(self, bg="darkblue", border=3, highlightbackground='lightblue')
        self._sheet.place(relx=0.025, rely=0.05, anchor=NW, bordermode=INSIDE, relwidth=0.95, relheight=0.65)

        # ===== DECK =====

        self._deck = Label(self, bg="darkblue")
        self._deck.image = ImageFactory.instance.get_deck()
        self._deck.config(image=self._deck.image)
        self._deck.place(relx=0.25, rely=1, anchor=S)

        # ===== DEFAUSSE =====

        self._defausse = Label(self, bg="darkblue")
        self._defausse.place(relx=0.65, rely=1, anchor=CENTER)

        # ===== PLAYERS NAMES =====

        self._players_names = []
        for i in range(4):
            self._players_names.append(Label(self, fg="white", bg="darkblue"))
            self._players_names[i].place(x=self._coords_x[i], y=self._coords_y[0], anchor=NW)

        # ===== CARDS =====

        self._cards = []
        for i in range(12):
            self._cards.append(Label(self, bg="darkblue", borderwidth=0))
            self._cards[i].place(x=self._coords_x[i % 4], y=self._coords_y[1] + int(i / 4) * 20, anchor=NW)
            self._cards[i].bind('<ButtonRelease-1>', self.card_picked)
            self._cards[i].bind('<B1-Motion>', self.drag_card)
            self._cards[i].card = None

        # ===== MESSAGES =====

        self._messages = []
        for i in range(4):
            self._messages.append(Label(self, fg="gold", bg="darkblue"))
            self._messages[i].place(x=self._coords_x[i], y=self._coords_y[2], anchor=NW)

        # ===== SCORES =====

        self._scores = []
        for i in range(4):
            self._scores.append(Label(self, fg="gold", bg="darkblue"))
            self._scores[i].place(y=i * 25, relx=0.975, rely=0.75, anchor=NE)

        # ===== TOP CARD =====

        self._top_card = Label(self, bg="darkblue", borderwidth=0)
        self._top_card.image = ImageFactory.instance.get_back()
        self._top_card.config(image=self._top_card.image)
        self._top_card.place(relx=0.25, rely=1, anchor=CENTER)
        self._top_card.bind('<ButtonRelease-1>', self.card_drawed)
        self._top_card.bind('<B1-Motion>', self.drag_card)

    def init(self):

        self.players.clear()

        # ===== RÉCUPÉRATION DES NOMS POUR UN SERVEUR =====

        if isinstance(self.master.handler, BattleNetServer):

            self.players.append(self.master.handler.name)
            for agent in self.master.handler.players:
                self.players.append(agent.agent_name)

        # ===== RÉCUPÉRATION DES NOMS POUR UN CLIENT =====

        elif isinstance(self.master.handler, BattleNetClient):

            self.players.append(self.master.handler.name)
            self.players.extend(self.master.handler.players_names)

        # ===== REDEFINITIONS DES CALLBACKS DE BATTLE =====

        def on_new_turn():
            print('== New turn!')
            self.new_turn()
            self.refresh_scores()

        def on_card_drawn(player_name, card):
            if player_name:
                print(player_name + ' drawed ' + str(card))
                index_player = self.players.index(player_name)
            else:
                print('I drawed ' + str(card))
                index_player = 0

            index = index_player + self.battle_stage[index_player] * 4
            self.battle_stage[index_player] += 1

            if (not self.master.handler.no_card_upside_down) and (int(index / 4) == 1):
                image = ImageFactory.instance.get_back()
            else:
                image = ImageFactory.instance.get(card)

            self.update_card_img(index, image)
            self._cards[index].card = card

        def on_battle(in_battle, other_members_names):
            print('== Battle!')
            if in_battle:
                self.can_draw = True
                self.in_battle = True
                self.replace_top_card()
                self.battle_stage[0] = 1
                self._messages[0]['text'] = "BATAILLE !"
            for i in range(1, self.nb_players):
                if self.players[i] in other_members_names:
                    self.battle_stage[i] = 1
                    self._messages[i]['text'] = "BATAILLE !"

        def on_turn_finished(winner_name):
            if winner_name:
                print('== ' + winner_name + ' wins this turn!')
                index = self.players.index(winner_name)
            else:
                print('== I win this turn!')
                index = 0
                self.can_pick_all = True

            self.can_draw = False
            self.in_battle = False

            self.battle_stage = [0, 0, 0, 0]
            for label in self._messages:
                label['text'] = ''
            self._messages[index]['text'] = "GAGNÉ !"

            self.hide_top_card()

        def on_turn_par():
            print("== Turn par!")

            self.on_par = True
            self.can_pick_mine = True
            self.in_battle = False

            self.battle_stage = [0, 0, 0, 0]
            self._messages[0]['text'] = "ÉGALITÉ"

            self.hide_top_card()

        def on_player_picked_card(card):
            for i in range(12):
                label_card = self._cards[i]
                if label_card.card and label_card.card == card:
                    label_card.image = None
                    label_card.lower()
                    break

        def on_game_ended():
            print("== No more card for me")
            self.game_ended = True
            self._top_card.place_forget()
            self._deck.place_forget()

        def on_game_won(winner_name):
            print('== ' + winner_name + ' WINS THE GAME!')
            self.master.winners.append(winner_name)
            self.master.raise_frame('scores')

        def on_game_par(winners_names):
            winners = ''
            for name in winners_names:
                winners += name + " "
            print('== ' + winners + 'WIN THE GAME!')
            self.master.winners = winners_names
            self.master.raise_frame('scores')

        self.master.battle.on_new_turn = on_new_turn
        self.master.battle.on_card_drawn = on_card_drawn

        self.master.battle.on_battle = on_battle
        self.master.battle.on_turn_finished = on_turn_finished
        self.master.battle.on_turn_par = on_turn_par
        self.master.battle.on_player_picked_card = on_player_picked_card

        self.master.battle.on_game_ended = on_game_ended
        self.master.battle.on_game_won = on_game_won
        self.master.battle.on_game_par = on_game_par

        self.nb_players = len(self.players)

        for i in range(self.nb_players):
            self._players_names[i]['text'] = self.players[i] + (' (moi)' if (i == 0) else '')

        self.new_turn()
        self.refresh_scores()

    # ===== FONCTIONS UTILES =====

    def refresh_scores(self):
        my_points = self.master.battle.my_points()
        others_points = self.master.battle.others_points()

        for i in range(0, self.nb_players):
            self._scores[i]['text'] = "{} : {} pts".format(self.players[i], my_points if (i == 0) else others_points[self.players[i]])

    def update_card_img(self, index, new_img):
        card = self._cards[index]
        card.image = new_img
        card.config(image=new_img)
        card.lift()

    def drag_card(self, evt):
        def dragging(card):
            x, y = self.winfo_pointerx() - self.master.winfo_rootx(), self.winfo_pointery() - self.master.winfo_rooty()
            card.place(x=x, y=y, relx=0, rely=0, anchor=CENTER)
            card.lift()
            return

        if self.can_draw and not self.game_ended:
            if evt.widget == self._top_card:
                dragging(evt.widget)

        if self.can_pick_mine:
            index = self._cards.index(evt.widget)
            if index % 4 == 0:
                dragging(evt.widget)

        if self.can_pick_all:
            if evt.widget in self._cards:
                dragging(evt.widget)

    def card_drawed(self, evt):
        if self.can_draw:
            self.can_draw = self.in_battle
            self.master.battle.draw_card()

            if self.in_battle:
                self.replace_top_card()
            else:
                self.hide_top_card()

    def card_picked(self, evt):
        if self.can_pick_all:
            self.master.battle.pick_card(evt.widget.card)
            self.replace_card_in_sheet(evt.widget)

        if self.can_pick_mine:
            index = self._cards.index(evt.widget)
            if index % 4 == 0:
                self.master.battle.pick_card(evt.widget.card)
                self.replace_card_in_sheet(evt.widget)

    def new_turn(self):
        self.can_draw = True
        self.can_pick_all = False
        self.can_pick_mine = False
        self.in_battle = False

        for i in range(self.nb_players):
            self._messages[i]['text'] = ''

        self.update_card_img(0, ImageFactory.instance.get_border())
        self.replace_top_card()

    def replace_card_in_sheet(self, card):
        if not self.on_par:
            self._defausse.image = ImageFactory.instance.get(card.card)
            self._defausse.config(image=self._defausse.image)

        i = self._cards.index(card)
        x, y = self._coords_x[i % 4], self._coords_y[1] + int(i / 4) * 20
        card.place(x=x, y=y, anchor=NW)
        card.image = None
        card.lower()

    def replace_top_card(self):
        if self.game_ended:
            self.hide_top_card()
        else:
            self._top_card.place(relx=0.25, rely=1, x=0, y=0, anchor=CENTER)

    def hide_top_card(self):
        self._top_card.place(relx=0.25, rely=1, x=0, y=0, anchor=N)