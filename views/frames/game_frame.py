from tkinter import *

from model.nethandler.battle_net_client import BattleNetClient
from model.nethandler.battle_net_server import BattleNetServer
from views.image_factory import ImageFactory
from model.battle import Battle
from model.card import *


class GameFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='darkblue')

        self._battle = None
        self.nb_players = 2
        self.can_draw = True
        self.can_pick = False
        self.players = []
        self.nb_cards_drawed = 0

        self._coords_x = [150, 390, 520, 650]
        self._coords_y = [75, 100, 250]

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
        for i in range(4):
            self._labels_cards.append(Label(self, bg="darkblue", borderwidth=0))
            self._labels_cards[i].place(x=self._coords_x[i], y=self._coords_y[1], anchor=NW)

        me = self._labels_cards[0]
        me.image = ImageFactory.instance.get_border()
        me.config(image=me.image)
        me.bind('<1>', self.pick_cards)

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

        # ===== INITIALISATION D'UN PLATEAU DE SERVEUR =====

        if isinstance(self.master.handler, BattleNetServer):

            self.players.append(self.master.handler.name)
            for agent in self.master.handler.players:
                self.players.append(agent.agent_name)

            self.nb_players = len(self.players)
            self._battle = Battle(self.nb_players)
            self.refresh_scores()
            self._battle.draw()

            # == REDEFINITION DES CALLBACKS ==

            def on_player_draw_card(client_name):
                index = self.players.index(client_name)
                card = self._battle.current_draw()[index]
                image = ImageFactory.instance.get(card)
                self.update_card_img(index, image)
                self.master.handler.game_turn_card_drawn(client_name, str(card))
                self.card_drawn()
                print(client_name + ' drawed ' + str(card))

            def on_player_picked_card(client_name, card_desc):
                self.new_turn()
                self.refresh_scores()
                self._battle.draw()

            self.master.handler.on_player_draw_card = on_player_draw_card
            self.master.handler.on_player_picked_card = on_player_picked_card

        # ===== INITIALISATION D'UN PLATEAU DE CLIENT =====

        elif isinstance(self.master.handler, BattleNetClient):

            self.players.append(self.master.handler.name)
            self.players.extend(self.master.handler.players_names)

            self.nb_players = len(self.players)

            # == REDEFINITION DES CALLBACKS ==

            def on_game_new_turn():
                print('== New turn!')
                self.can_draw = True

            def on_my_card_drawn(card_desc):
                print('I drawed ' + card_desc)
                card = self.generate_card_from_desc(card_desc)
                image = ImageFactory.instance.get(card)
                self.update_card_img(0, image)

            def on_player_card_drawn(client_name, card_desc):
                print(client_name + ' drawed ' + card_desc)
                index = self.players.index(client_name)
                card = self.generate_card_from_desc(card_desc)
                image = ImageFactory.instance.get(card)
                self.update_card_img(index, image)

            def on_player_picked_card(client_name, card_desc):
                self.new_turn()

            def on_turn_finished(winner):
                print('== ' + winner + ' wins this turn!')
                index = self.players.index(winner)
                self._labels_msg[index]['text'] = "WINNER !"
                self.can_pick = (index == 0)

            self.master.handler.on_game_new_turn = on_game_new_turn
            self.master.handler.on_my_card_drawn = on_my_card_drawn
            self.master.handler.on_player_card_drawn = on_player_card_drawn
            self.master.handler.on_player_picked_card = on_player_picked_card
            self.master.handler.on_turn_finished = on_turn_finished

        self.init_labels()

    # ===== FONCTIONS UTILES =====

    @staticmethod
    def generate_card_from_desc(card_desc):
        p = re.compile("([A-Z]*)\(([A-Z]*)\)")  # TODO: refaire parce que c'est dégueux (utiliser plutôt repr)
        res = p.search(card_desc)
        return Card(CardSuite[res.group(1)], CardRank[res.group(2)])

    def init_labels(self):
        for i in range(self.nb_players):
            self._labels_players[i]['text'] = self.players[i]

    def refresh_scores(self):
        for i in range(self.nb_players):
            points = self._battle.nb_points(i)
            cards = self._battle.nb_cards_won(i)
            self._labels_scores[i]['text'] = "{} : {} pt / {} cartes".format(self.players[i], points, cards)

    def update_card_img(self, index, new_img):
        label_card = self._labels_cards[index]
        label_card.image = new_img
        label_card.config(image=new_img)

    def reset_top_card_position(self):
        self._top_card.place(relx=0.25, rely=1, x=0, y=0)

    def drag_card(self, evt):
        if self.can_draw:
            x, y = self.winfo_pointerx() - self.master.winfo_rootx(), self.winfo_pointery() - self.master.winfo_rooty()
            evt.widget.place(x=x, y=y, relx=0, rely=0, anchor=CENTER)

    def card_drawn(self):
        self.nb_cards_drawed += 1

        if self.nb_cards_drawed == self.nb_players:
            self.nb_cards_drawed = 0

            winner = self._battle.turn_winner()
            print('== ' + self.players[winner] + ' wins this turn!')

            self.master.handler.game_turn_won(self.players[winner])
            self.can_pick = (winner == 0)
            self._labels_msg[winner]['text'] = "WINNER !"

    def release_card(self, evt):
        # TODO: seulement si la carte est proche de la zone de dépôt ?
        if self.can_draw:
            self.can_draw = False
            self.reset_top_card_position()
            self.update_card_img(0, ImageFactory.instance.get_back())

            if isinstance(self.master.handler, BattleGameClient):
                self.master.handler.game_turn_draw_card()
            elif isinstance(self.master.handler, BattleGameServer):
                card = self._battle.current_draw()[0]
                image = ImageFactory.instance.get(card)
                self.update_card_img(0, image)
                self.master.handler.game_turn_card_drawn(self.players[0], str(card))
                self.card_drawn()
                print('I drawed ' + str(card))

    def pick_cards(self, evt):
        if self.can_pick:
            if isinstance(self.master.handler, BattleGameClient):
                self.master.handler.game_turn_card_pick("something")
            elif isinstance(self.master.handler, BattleGameServer):
                self.master.handler.game_turn_card_pick("something")
                self.refresh_scores()
                self._battle.draw()

            self.new_turn()

    def new_turn(self):
        self.can_pick = False
        self.can_draw = True

        for label in self._labels_cards:
            label.image = None
        for i in range(0, self.nb_players):
            self._labels_players[i].image = None
            self._labels_msg[i]['text'] = ''

        me = self._labels_cards[0]
        me.image = ImageFactory.instance.get_border()
        me.config(image=me.image)
