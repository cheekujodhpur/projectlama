from .utils import nread, prompt


class Player:
    def __init__(self, sno, auto=False):
        self.id = sno
        self.auto = auto
        self.active = True
        self.hand = []

    def activate(self):
        self.active = True

    def draw(self, deck):
        self.hand.append(deck.main_pile.pop())

    def delete(self, n):
        i = 0
        while i < len(self.hand):
            if nread(self.hand[i]) == n:
                return self.hand.pop(i)
            i = i + 1

    def play(self, deck):
        # Return if folded
        if not self.active:
            return True

        print(deck)
        top_card = deck.top_card()
        hand = list(map(nread, self.hand))
        # check if unplayable and draw if so
        if not deck.playable(hand):
            if not len(deck.main_pile):
                return False  # round ends
            self.draw(deck)
            print(f"Player{self.id} cannot play. They draw...\n")
            return True

        # Now we are asking for choice
        u_out = f"Player{self.id} playing...\n\
You have the following options:\n\
{hand}\n\
to be played on {nread(top_card)}"
        choice = prompt(u_out)

        # play the choice
        if not choice.isdigit():
            print("Error: Input should be a digit")
            return self.play(deck)
        if not deck.playable(int(choice)):
            print("Error: Invalid input")
            return self.play(deck)
        # We only reach here if we can actually play the choice
        deck.discard(self.delete(int(choice)))

        # decide if it ends the round
        if not len(self.hand):
            return False

        return True
