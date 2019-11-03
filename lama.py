#! /usr/bin/env python
import sys
from game import Deck, Players


def run(deck, players):

    # distribute the hand
    players.draw(deck)
    deck.start()

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

    # default
    n_players = 2
    if len(sys.argv) > 1 and \
            sys.argv[1].isdigit() and \
            (6 >= int(sys.argv[1]) >= 2):
        n_players = int(sys.argv[1])
    with Deck() as deck:
        with Players(n_players) as players:
            run(deck, players)
