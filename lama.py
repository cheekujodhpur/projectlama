#! /usr/bin/env python
import sys
from game import Deck, Players


def run(deck, players):

    # distribute the hand
    players.draw(deck)

    input_str = "q: quit\nllama> "
    while True:
        ukey = input(input_str)

        for player in players.players:
            print(player.hand)

        # exit
        if ukey is "q" or ukey is "Q":
            sys.exit(0)


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
