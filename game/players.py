from .utils import nread, prompt


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
        u_out = f"Player{self.id} playing...\n\
You have the following options:\n\
{visible}\n\
to be played on {top_card}"
        choice = prompt(u_out)
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
