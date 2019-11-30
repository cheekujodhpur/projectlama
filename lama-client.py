from game.utils import prompter
import time
import xmlrpc.client

if __name__ == "__main__":
    s = xmlrpc.client.ServerProxy('http://localhost:1144')

    in_game = False
    token = None
    prev_game_state = None
    while True:
        time.sleep(0.1)
        if not in_game:
            # let us join a game
            choice = prompter(f"What to do?", ["Create", "Join"], validate=True)
            if choice is 1:
                game_id = s.open()
                print(f"Your newly created game id is {game_id}")
                token = s.join(game_id)
                print(f"You have joined with player token {token}")
                in_game = True
            elif choice is 2:
                game_id = prompter(f"Enter game id.",[])
                if not s.validate(game_id):
                    print("Invalid game id\n")
                    continue
                else:
                    try:
                        token = s.join(game_id)
                        print(f"You have joined with player token {token}")
                        in_game = True
                    except xmlrpc.client.Fault as e:
                        print(f"Error {e.faultCode}: {e.faultString}\n")

        else:
            game_state = s.query_state(game_id,token)
            if game_state == prev_game_state:
                continue
            prev_game_state = game_state
            print(game_state)

