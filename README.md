# projectlama
Leg Alle Minpunten Af

[L.A.M.A.](https://boardgamegeek.com/boardgame/266083/llama) is a board game we love to play. This repository is our attempt to write an AI and a GUI to play this.

```python
pip install -r requirements_dev.txt
# For testing and gameplay
python lama.py
# For future
python lama-server.py # in one terminal
python lama-client.py # in another and more
```

## TODO
- You are not using the Q table to decide the move right? You should use the max(q(state, \*actions)) to decide the action given a state. 
- You should also implement exploration. i.e., with some small probability it picks a random action instead of the max over q values.
- Can you set your IDE/code editor to use 4 spaces instead of tab? 
- Make sure you follow PEP8 conventions, get pylint or flake8 to check this for you

