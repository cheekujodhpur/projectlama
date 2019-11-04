#! /usr/bin/env python
import sys
from game import Game


def run(deck, players):

    while True:
        # print deck status
        deck.status()

        input_str = "q: quit\nllama> "
        input_str = f"c: continue\n{input_str}"
        ukey = input(input_str)

        # exit
        if ukey is "q" or ukey is "Q":
            sys.exit(0)
        elif ukey is "c" or ukey is "C":
            players.play(deck)


if __name__ == "__main__":

    with Game() as game:
        game.init()
        game.run()
