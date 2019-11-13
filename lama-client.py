import xmlrpc.client
from game.utils import prompt

if __name__ == "__main__":
    s = xmlrpc.client.ServerProxy('http://localhost:1144')

    # game flow continues
    u_in = prompt(f"Create(c) game or Join(j) game")
    if u_in in ["c", "C"]:
        g = s.open()
        print(f"Your newly created game id is {g}")
    elif u_in in ["j", "J"]:
        g = prompt(f"Enter game id")
        if not s.validate(g):
            print("Fool")
        else:
            print("Cool")
