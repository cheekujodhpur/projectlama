class Player:
    def __init__(self, auto=False):
        self.auto = auto
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.main_pile.pop())

class Players:
    def __init__(self, n_players):
        self.n = n_players
        self.players = [Player() for i in range(self.n)]

    def __enter__(self):
        print(f"Initialised with {self.n} players...")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def __str__(self):
        return f"{self.n} players are playing L.A.M.A."

    def draw(self, deck):
        for i in range(6):
            for player in self.players:
                player.draw(deck)
