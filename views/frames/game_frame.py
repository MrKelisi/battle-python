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
        self.can_pick = False
        self.in_battle = False
        self.on_battle = False
        self.on_par = False
        self.game_ended = False
        self.battle_stage = [0, 0, 0, 0]
        self.players = []
        self.nb_cards_drawed = 0

        self._coords_x = [150, 390, 520, 650]
        self._coords_y = [75, 100, 285]

        self._sheet = Canvas(self, bg="darkblue", border=3)
        self._sheet.place(relx=0.025, rely=0.05, anchor=NW, bordermode=INSIDE, relwidth=0.95, relheight=0.65)

        # ===== DECK PIC =====

        self._deck = Label(self, bg="darkblue")
        self._deck.image = ImageFactory.instance.get_back()
        self._deck.config(image=self._deck.image)
        self._deck.place(relx=0.25, rely=1, anchor=CENTER)

        # ===== PLAYERS NAMES =====

        self._labels_players = []
        for i in range(4):
            self._labels_players.append(Label(self, fg="white", bg="darkblue"))
            self._labels_players[i].place(x=self._coords_x[i], y=self._coords_y[0], anchor=NW)

        # ===== CARDS =====

        self._labels_cards = []
        for i in range(12):
            self._labels_cards.append(Label(self, bg="darkblue", borderwidth=0))
            self._labels_cards[i].place(x=self._coords_x[i % 4], y=self._coords_y[1] + int(i/4) * 20, anchor=NW)
            self._labels_cards[i].bind('<ButtonRelease-1>', self.pick_card)
            self._labels_cards[i].bind('<B1-Motion>', self.drag_card)
            self._labels_cards[i].card = None
            self._labels_cards[i].lower()

        me = self._labels_cards[0]
        me.image = ImageFactory.instance.get_border()
        me.config(image=me.image)

        # ===== MESSAGES =====

        self._labels_msg = []
        for i in range(4):
            self._labels_msg.append(Label(self, fg="gold", bg="darkblue"))
            self._labels_msg[i].place(x=self._coords_x[i], y=self._coords_y[2], anchor=NW)

        # ===== SCORES =====

        self._labels_scores = []
        for i in range(4):
            self._labels_scores.append(Label(self, fg="gold", bg="darkblue"))
            self._labels_scores[i].place(y=i*25, relx=0.975, rely=0.75, anchor=NE)

        # ===== TOP CARD =====

        self._top_card = Label(self, bg="darkblue", borderwidth=0)
        self._top_card.image = ImageFactory.instance.get_back()
        self._top_card.config(image=self._top_card.image)
        self._top_card.place(relx=0.25, rely=1, anchor=CENTER)
        self._top_card.bind('<ButtonRelease-1>', self.release_card)
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
                index = self.players.index(player_name)
            else:
                print('I drawed ' + str(card))
                index = 0

            if self.on_battle:
                self.battle_stage[index] += 1
                index += self.battle_stage[index] * 4

            if index / 4 == 1:
                image = ImageFactory.instance.get_back()
            else:
                image = ImageFactory.instance.get(card)

            self.update_card_img(index, image)
            self._labels_cards[index].card = card

        def on_battle(in_battle, other_members_names):
            print('== Battle!')
            self.on_battle = True
            if in_battle:
                self._labels_msg[0]['text'] = "BATTLE!"
                self.in_battle = True
            for i in range(1, self.nb_players):
                if self.players[i] in other_members_names:
                    self._labels_msg[i]['text'] = "BATTLE!"

        def on_turn_finished(winner_name):
            if winner_name:
                print('== ' + winner_name + ' wins this turn!')
                index = self.players.index(winner_name)
            else:
                print('== I win this turn!')
                index = 0
                self.can_pick = True

            self.in_battle = False
            self.on_battle = False
            self.battle_stage = [0, 0, 0, 0]

            for label in self._labels_msg:
                label['text'] = ''
            self._labels_msg[index]['text'] = "WIN!"

        def on_turn_par():
            print("== Turn par!")
            self.on_par = True
            self.in_battle = False
            self.on_battle = False
            self._labels_msg[0]['text'] = "PAR"

        def on_player_picked_card(card):
            for i in range(12):
                label_card = self._labels_cards[i]
                if label_card.card and label_card.card == card:
                    label_card.image = None
                    label_card.lower()
                    break

        def on_game_ended():
            print("== No more card")
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

        # ===== INITIALISATION DES LABELS =====

        self.nb_players = len(self.players)

        for i in range(self.nb_players):
            self._labels_players[i]['text'] = self.players[i]
            if i == 0:
                self._labels_players[i]['text'] += ' (me)'

    # ===== FONCTIONS UTILES =====

    def refresh_scores(self):
        my_points = self.master.battle.my_points()
        others_points = self.master.battle.others_points()

        self._labels_scores[0]['text'] = "{} : {} pts".format(self.players[0], my_points)
        for i in range(1, self.nb_players):
            self._labels_scores[i]['text'] = "{} : {} pts".format(self.players[i], others_points[self.players[i]])

    def update_card_img(self, index, new_img):
        label_card = self._labels_cards[index]
        label_card.image = new_img
        label_card.config(image=new_img)
        label_card.lift()

    def reset_top_card_position(self):
        if not self.game_ended:
            self._top_card.place(relx=0.25, rely=1, x=0, y=0)

    def drag_card(self, evt):
        if self.can_draw or self.in_battle:
            x, y = self.winfo_pointerx() - self.master.winfo_rootx(), self.winfo_pointery() - self.master.winfo_rooty()
            evt.widget.place(x=x, y=y, relx=0, rely=0, anchor=CENTER)
            evt.widget.lift()

    def release_card(self, evt):
        # TODO: seulement si la carte est dans la zone de dépôt ?
        if self.can_draw:
            self.can_draw = False
            self.reset_top_card_position()
            self.update_card_img(0, ImageFactory.instance.get_back())

            self.master.battle.draw_card()

        if self.in_battle:
            self.reset_top_card_position()

            self.master.battle.draw_card()

    def pick_card(self, evt):
        label_card = evt.widget

        if self.can_pick:
            label_card.image = None
            self.master.battle.pick_card(label_card.card)

        if self.on_par:
            if (self._labels_cards.index(label_card) % 4) == 0:
                label_card.image = None
                self.master.battle.pick_card(label_card.card)

    def new_turn(self):
        self.can_draw = True
        self.can_pick = False
        self.in_battle = False
        self.on_par = False

        for i in range(self.nb_players):
            self._labels_msg[i]['text'] = ''

        me = self._labels_cards[0]
        me.image = ImageFactory.instance.get_border()
        me.config(image=me.image)
        me.lift()
