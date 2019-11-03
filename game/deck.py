import random
import time


class Deck:
    def __init__(self):
        # 56 cards
        cards = [i for i in range(56)]
        random.seed(time.clock_gettime(0))
        random.shuffle(cards)
        self.main_pile = cards
        self.discard_pile = []

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def __str__(self):
        return("Deck status print command")
