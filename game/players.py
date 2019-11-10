from .utils import nread, prompt


class Player:
    def __init__(self, sno, auto=False):
        self.id = sno
        self.auto = auto
        self.hand = []
        self.active = True
        self.score = 0

    def init(self):
        self.hand = []
        self.active = True

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def draw(self, deck):
        self.hand.append(deck.main_pile.pop())

    def calc_score(self):
        if not len(self.hand):
            if not self.score:
                self.score = 0
            # TODO: Ideally the following should be a choice
            elif self.score < 10:
                self.score = self.score - 1
            else:
                self.score = self.score - 10
        else:
            hand = list(set(map(nread,self.hand)))
            increment = sum(map(lambda x: x if x < 7 else 10, hand))
            self.score = self.score + increment
        return self.score

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
        print(f"Player{self.id} has hand\n{hand}\n")
        # check if unplayable and draw if so
        if not deck.playable(hand):
            if not len(deck.main_pile):
                return False  # round ends
            u_out = f"Player{self.id} cannot play. Draw(d) or Fold(f)"
            choice = prompt(u_out)
            if choice is "f" or choice is "F":
                self.deactivate()
                return True
            elif choice is "d" or choice is "D":
                print("They draw...")
                self.draw(deck)
                return True
            else:
                print("Error: Invalid input")
                return self.play(deck)

        # Now we are asking for choice
        u_out = f"Player{self.id} playing...\n\
You have to play on {nread(top_card)} or fold(f)"
        choice = prompt(u_out)

        # play the choice
        if not choice.isdigit():
            if choice is "f" or choice is "F":
                self.deactivate()
                return True
            else:
                print("Error: Input should be a digit or f to fold")
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
