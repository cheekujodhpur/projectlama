#! /usr/bin/env python
import sys
from game import Game


if __name__ == "__main__":

    with Game() as game:
        game.init()
        game.run()
