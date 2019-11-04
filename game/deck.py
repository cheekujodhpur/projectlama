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

    def __str__(self):
        out = f"The top card is {nread(self.discard_pile[-1])}"
        return out
