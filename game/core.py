from .deck import Deck
from .players import Player
from .utils import prompt


class Round:
    def __init__(self):
        self.history = []
        self.deck = Deck()
        self.deck.start()

    def run(self, players):
        # init draw
        for i in range(6):
            for player in players:
                player.draw(self.deck)

        while True:
            print(self.deck)
            for player in players:
                player.play(self.deck)


class Game:
    def __init__(self):
        self.history = []

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def init(self):
        u_in = prompt("How many players?")
        n_players = 2  # default
        if u_in.isdigit() and 6 >= int(u_in) >= 2:
            n_players = int(u_in)

        self.players = [Player(i + 1) for i in range(n_players)]

    def run(self):
        while True:
            self.round = Round()
            self.round.run(self.players)
