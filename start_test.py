import sys, random, string
from game import NetworkGame, State

if __name__ == "__main__":
	no_of_games = int(sys.argv[1])
	no_of_players = int(sys.argv[2])
	if no_of_players > 6:
		print("Error: Can't have more than 6 players per game")
		sys.exit(1)
	for i in range(no_of_games):
		game_id = ''.join(
            random.choices(
                string.ascii_uppercase +
                string.digits,
                k=5))
		game = NetworkGame(game_id)
		game.input_wait_queue.append("start")
		for j in range(no_of_players):
			game.add_AIplayer()
		game.init()
		_ = game.step(None)
		curr_state = game.state
		while curr_state is not State.GAME_END:
			_ = game.step(None)
			if curr_state is State.ROUND_CONT:
				if game.turn.auto:
					_ = game.step(game.moveAI(game.turn))
			curr_state = game.state

	sys.exit(0)