from .deck import Deck
from .players import Player, NetworkPlayer
from .utils import prompter
from .constants import State, Prompt, GameErrors
from twisted.web import http, server, xmlrpc
import random
import string


class Game:
    def __init__(self):
        self.history = []
        self.state = None
        self.turn = None

    def init(self):
        self.state = State.GAME_BEGIN

    def advance_turn(self):
        self.turn = self.turn % len(self.players) + 1

    def calc_score(self):
        for player in self.players:
            self.score[player.id] = player.calc_score()
        for player in self.players:
            if self.score[player.id] >= 40:
                return True
        return False

    def evaluate(self, state, info):
        if state is State.GAME_BEGIN:
            if info is None:
                return Prompt.NUM_PLAYERS, State.GAME_BEGIN
            else:
                n_players = info
                self.players = [Player(i + 1) for i in range(n_players)]
                self.score = {}
                for player in self.players:
                    self.score[player.id] = 0
                # Decide who has first turn
                self.turn = 1  # The first playerId has first turn
                return None, State.ROUND_BEGIN

        elif state is State.ROUND_BEGIN:
            # deck
            self.deck = Deck()
            self.deck.start()

            # first draw
            for player in self.players:
                player.init()
            for i in range(6):
                for player in self.players:
                    player.draw(self.deck)

            return None, State.ROUND_CONT

        elif state is State.ROUND_CONT:
            print(self.deck)

            if not sum(map(lambda x: x.active, self.players)):
                return None, State.ROUND_END

            player = self.players[self.turn-1]
            deck = self.deck
            if player.active:
                if not deck.playable(player.hand):
                    active_players = sum(map(lambda x: x.active, self.players))
                    if not len(deck.main_pile) or active_players is 1:
                        player.deactivate()
                    elif info is None:
                        return Prompt.FD, State.ROUND_CONT
                    else:
                        if info is "Fold":
                            player.deactivate()
                        elif info is "Draw":
                            player.draw(self.deck)
                else:
                    if info is None:
                        return Prompt.PF, State.ROUND_CONT
                    else:
                        if info is "Fold":
                            player.deactivate()
                        else:
                            deck.discard(player.delete(info))

                            # round ender if finishes hand
                            if not len(player.hand):
                                return None, State.ROUND_END

            self.advance_turn()
            return None, State.ROUND_CONT

        elif state is State.ROUND_END:
            over = self.calc_score()
            for player in self.players:
                print(f"Player{player.id} has score {self.score[player.id]}...\n")
            if over:
                winner = sorted(self.players,
                                key=lambda x: self.score[x.id])[0]
                print(f"Player{winner.id} wins.\n")
                return None, State.GAME_END
            else:
                return None, State.ROUND_BEGIN


    def get_info(self, prompt):
        if prompt is None:
            return None
        elif prompt is Prompt.NUM_PLAYERS:
            u_in = prompter("How many players?", [])
            n_players = 2  # default
            if u_in.isdigit() and 6 >= int(u_in) >= 2:
                n_players = int(u_in)
            return n_players
        elif prompt is Prompt.FD:
            choices = ["Draw", "Fold"]
            player = self.players[self.turn-1]
            choice = prompter(f"Player{player.id} cannot play from hand {player.hand}", choices)
            if not choice.isdigit() or int(choice)-1 not in range(len(choices)):
                print("Invalid input.\n")
                return None

            return choices[int(choice)-1]
        elif prompt is Prompt.PF:
            choices = ["Play", "Fold"]
            player = self.players[self.turn-1]
            deck = self.deck
            choice = prompter(f"Player{player.id} can play from hand {player.hand}.", choices)
            if not choice.isdigit() or int(choice)-1 not in range(len(choices)):
                print("Invalid input.\n")
                return None
            if int(choice) is 2:
                return "Fold"
            else:
                choice = prompter(f"Which card would you like to play?", [])
                if not choice.isdigit() or int(choice) not in player.hand or not deck.playable(int(choice)):
                    print("Invalid input.\n")
                    return None
                else:
                    return int(choice)

    def run(self):
        info = None
        while self.state is not State.GAME_END:
            prompt, new_state = self.evaluate(self.state, info)
            self.state = new_state
            info = self.get_info(prompt)


class NetworkGame(Game):
    def __init__(self, game_id):
        self.game_id = game_id
        self.players = []
        super().__init__()

    def add_player(self):
        if len(self.players) < 6:
            player_token = ''.join(
                random.choices(
                    string.ascii_uppercase +
                    string.digits,
                    k=5))
            self.players.append(NetworkPlayer(len(self.players), player_token))
            return player_token
        else:
            raise xmlrpc.Fault(GameErrors.GAME_FULL, f"Game {self.game_id} is full")

class GameMaster(xmlrpc.XMLRPC):
    def __init__(self):
        self.games = {}
        xmlrpc.XMLRPC.__init__(self)

    @staticmethod
    def __apply_CORS_headers(request):
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        request.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')

    def render_OPTIONS(self, request):
        GameMaster.__apply_CORS_headers(request)
        request.setResponseCode(http.OK)
        request.write('OK'.encode('utf-8'))
        request.finish()
        return server.NOT_DONE_YET

    @xmlrpc.withRequest
    def xmlrpc_open(self, request):
        GameMaster.__apply_CORS_headers(request)
        game_id = ''.join(
            random.choices(
                string.ascii_uppercase +
                string.digits,
                k=5))
        g = NetworkGame(game_id)
        self.games[game_id] = g
        return game_id

    @xmlrpc.withRequest
    def xmlrpc_validate(self, request, game_id, player_token=None):
        GameMaster.__apply_CORS_headers(request)
        if game_id not in self.games:
            return False
        elif player_token is not None:
            search = sum(map(lambda x:x.token == player_token, self.games[game_id].players))
            if not search:
                return False
        return True

    @xmlrpc.withRequest
    def xmlrpc_join(self, request, game_id):
        GameMaster.__apply_CORS_headers(request)
        return self.games[game_id].add_player()

    @xmlrpc.withRequest
    def xmlrpc_query_state(self, request, game_id, player_token):
        GameMaster.__apply_CORS_headers(request)
        if not self.xmlrpc_validate(game_id, player_token=player_token):
            raise xmlrpc.Fault(GameErrors.INVALID_TOKEN, f"Invalid token, game pair presented")
        curr_state = self.games[game_id].state
        if curr_state is None:
            return f"Game has not begun yet. {len(self.games[game_id].players)} players have joined as of now."
