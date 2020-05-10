# projectlama
Leg Alle Minpunten Af

[L.A.M.A.](https://boardgamegeek.com/boardgame/266083/llama) is a board game we love to play. This repository is our attempt to write an AI and a GUI to play this.

```python
pip install -r requirements_dev.txt
# For testing of bots
python test-arena.py
# For future
python lama-server.py # in one terminal
python lama-client.py # in another and more
```

Logging of the gamestates is done as follows:
Keyword- Meaning, Stored data
1) nG - new Game, Game Number
2) nT - new Test, Date&Time
2) nR - new Round, /none/
3) tC - top Card, top card
4) pT - player Turn; Alias of the player who is active, their hand, and their action(f, d or p)
5) rE - round End, scores of all the players
6) gE - game End, winner
7) tE - End of Testing


## TODO
- Store qmatrix as follows:
```python
from collections import defaultdict
q_matrix = defaultdict(int)
q_matrix[(current_state, current_action)] = q_matrix[(current_state, current_action)] + alpha*reward*q_matrix[(next_state, next_action)]
```
- Write the equation you are using in code in comments and in README
- Add instructions how to run in README
- What is the play reward, can you make it a separate function so it can be edited easily?
- Seed your random
- Add a State Decoder as well
- Add requirements to `requirements\_dev.txt`
### Random Thoughts, Lower priority
- does the q agent have to start so dumb that it always just folds?
- Aren't there too many newlines in game logs? is it needed?
- Can we do better naming of all variables? self.BLOCK\_VAR is just bad. There is a standard Python naming convention. Follow that. Get a PEP8 checker like pylint or flake8 to check your code.
