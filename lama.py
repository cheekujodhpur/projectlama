#! /usr/bin/env python

import sys
from game import Deck, Players

def run(deck, players):
    # set up things
    print( deck )
    print( players )

if __name__ == "__main__":

    # default
    n_players = 2
    if len(sys.argv) > 1 and sys.argv[1].isdigit() and (6 >= int(sys.argv[1]) >= 2):
        n_players = int(sys.argv[1])
    with Deck() as deck:
        with Players(n_players) as players:
            run(deck, players) 
