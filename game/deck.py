import random
import time
from .utils import plus_one


class Deck:
    def __init__(self):
        # 56 cards
        cards = [(i % 7) + 1 for i in range(56)]
        random.seed(time.clock_gettime(0))
        random.shuffle(cards)
        self.main_pile = cards
        self.discard_pile = []

    def start(self):
        self.discard_pile.append(self.main_pile.pop())

    def discard(self, n):
        self.discard_pile.append(n)

    def top_card(self):
        return self.discard_pile[-1], len(self.discard_pile)

    def playable(self, cards):
        top_card, _ = self.top_card()
        if isinstance(cards, list) and all(isinstance(x, int) for x in cards):
            return ((top_card in cards) or (plus_one(top_card) in cards))
        elif isinstance(cards, int):
            return cards in [top_card, plus_one(top_card)]
        else:
            # raise TypeError("Only list or int")
            return False

    def __str__(self):
        out = f"The top card is {self.discard_pile[-1]}"
        return out
