from .utils import nread


class Player:
    def __init__(self, sno, auto=False):
        self.id = sno
        self.auto = auto
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.main_pile.pop())

    def delete(self, n):
        i = 0
        while i < len(self.hand):
            if nread(self.hand[i]) == n:
                return self.hand.pop(i)
            i = i + 1

    def play(self, deck):
        visible = list(map(nread, self.hand))
        top_card = nread(deck.discard_pile[-1])
        if top_card not in visible and nread(top_card) not in visible:
            self.draw(deck)
            return
        print(f"Player{self.id} playing...")
        print("You have the following options:")
        print(visible)
        print(f"to be played on {top_card}")
        choice = input("llama> ")
        if not choice.isdigit():
            print("Error: Input should be a digit")
            self.play(deck)
            return
        if int(choice) not in visible or \
                int(choice) not in [top_card, nread(top_card)]:
            print("Error: Invalid input")
            self.play(deck)
            return
        deck.discard(self.delete(int(choice)))


class Players:
    def __init__(self, n_players):
        self.n = n_players
        self.players = [Player(i + 1) for i in range(self.n)]

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

    def play(self, deck):
        for player in self.players:
            player.play(deck)
