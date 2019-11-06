import random
import time
from .utils import nread


class Deck:
    def __init__(self):
        # 56 cards
        cards = [i for i in range(56)]
        random.seed(time.clock_gettime(0))
        random.shuffle(cards)
        self.main_pile = cards
        self.discard_pile = []

    def start(self):
        self.discard_pile.append(self.main_pile.pop())

    def discard(self, n):
        self.discard_pile.append(n)

    def top_card(self):
        return self.discard_pile[-1]

    def playable(self, cards):
        top_card = self.top_card()
        if isinstance(cards, list):
            return (nread(top_card) in cards or nread(top_card + 1) in cards)
        elif isinstance(cards, int):
            return cards in [nread(top_card), nread(top_card + 1)]
        else:
            raise TypeError("Only list or int")

    def __str__(self):
        out = f"The top card is {nread(self.discard_pile[-1])}"
        return out
