from .constants import State, Prompt, GameErrors
from .deck import Deck
from .players import Player, NetworkPlayer
from .utils import prompter
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


class NetworkGame(Game):
    def __init__(self, game_id):
        self.game_id = game_id
        self.players = []
        self.package_send = {}
        self.package_send2 = {}
        super().__init__()

    def add_player(self, alias):
        if len(self.players) < 6:
            player_token = ''.join(
                random.choices(
                    string.ascii_uppercase +
                    string.digits,
                    k=5))
            self.players.append(NetworkPlayer(alias, player_token))
            return {"token": player_token}
        else:
            raise xmlrpc.Fault(GameErrors.GAME_FULL, f"Game {self.game_id} is full")

    def find_player(self, player_token):
        # validate guarantees you will find one
        for player in self.players:
            if player.token == player_token:
                return player
        return None

    def evaluate(self, state, info):
        if state is State.GAME_BEGIN:
            if info is None:
                return Prompt.NUM_PLAYERS, State.GAME_BEGIN
            else:
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
            self.package_send2 = {}

            # first draw
            for player in self.players:
                player.init()
            for i in range(6):
                for player in self.players:
                    player.draw(self.deck)

            return None, State.ROUND_CONT

        elif state is State.ROUND_CONT:
            # print(self.deck)
            if info is not None and info.isdigit():
                info = int(info)

            if not sum(map(lambda x: x.active, self.players)):
                return None, State.ROUND_END

            player = self.players[self.turn-1]
            deck = self.deck
            if player.active:
                if not deck.playable(player.hand):
                    active_players = sum(map(lambda x: x.active, self.players))
                    if not len(deck.main_pile) or active_players is 1:
                        player.deactivate()
                        return None, State.ROUND_END
                    else:
                        if info == "Fold":
                            player.deactivate()
                        elif info == "Draw":
                            player.draw(self.deck)
                        else:
                            return Prompt.FD, State.ROUND_CONT
                else:
                    if info is None:
                        return Prompt.PF, State.ROUND_CONT
                    else:
                        if info == "Fold":
                            player.deactivate()
                        elif deck.playable(info) and info in player.hand:
                            deck.discard(player.delete(info))

                            # round ender if finishes hand
                            if not len(player.hand):
                                return None, State.ROUND_END
                        else:
                            return Prompt.PF, State.ROUND_CONT

            self.advance_turn()
            return None, State.ROUND_CONT

        elif state is State.ROUND_END:
            over = self.calc_score()
            print_str = ""
            for player in self.players:
                print_str = f"{print_str}Player{player.id} has score {self.score[player.id]}...\n"
            if over:
                winner = sorted(self.players,
                                key=lambda x: self.score[x.id])[0]
                print_str = f"{print_str}Player{winner.id} wins.\n"
                for player in self.players:
                    self.package_send2[player.id] = print_str
                print(print_str)
                return None, State.GAME_END
            else:
                for player in self.players:
                    self.package_send2[player.id] = print_str
                print(print_str)
                return None, State.ROUND_BEGIN

    def get_info(self, prompt):
        if prompt is None:
            self.package_send = {}
            return None
        elif prompt is Prompt.NUM_PLAYERS:
            return len(self.players)
        elif prompt is Prompt.FD:
            self.package_send[self.turn] = str(prompt)
            return None
        elif prompt is Prompt.PF:
            self.package_send[self.turn] = str(prompt)
            return None

    def step(self, info):
        print(info)
        if self.state is not State.GAME_END:
            prompt, new_state = self.evaluate(self.state, info)
            print(f"{self.game_id} stepping from {str(self.state)} to {str(new_state)}")
            self.state = new_state
            return self.get_info(prompt)

class GameMaster(xmlrpc.XMLRPC):
    def __init__(self):
        self.games = {}
        xmlrpc.XMLRPC.__init__(self)

    @staticmethod
    def __apply_CORS_headers(request):
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        request.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Access-Control-Allow-Origin')

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
    def xmlrpc_join(self, request, game_id, alias):
        GameMaster.__apply_CORS_headers(request)
        return self.games[game_id].add_player(alias)

    @xmlrpc.withRequest
    def xmlrpc_query_state(self, request, game_id, player_token):
        GameMaster.__apply_CORS_headers(request)
        if not self.xmlrpc_validate(request, game_id, player_token=player_token):
            raise xmlrpc.Fault(GameErrors.INVALID_TOKEN, f"Invalid token, game pair presented")
        game = self.games[game_id]
        player = game.find_player(player_token)
        curr_state = game.state
        result = {}

        # Game not begun, lobby state to be sent
        if curr_state is None:
            result["game_state"] = "none"
            result["action"] = "wait"
            result["players"] = list(map(lambda x: x.alias, game.players))
            return result

        #TODO: hack, refactor
        try:
            top_card = game.deck.top_card()
        except:
            top_card = str(None)
        player_hand = game.players[player-1].hand
        player_package = game.package_send.get(player)
        if curr_state is None:
            return f"Game has not begun yet. {len(self.games[game_id].players)} players have joined as of now."
        else:
            if not game.package_send and not game.package_send2:
                _ = game.step(None)

            return_dict = {"curr_state": str(curr_state),
                           "player_action": str(player_package),
                           "top_card": top_card,
                           "player_hand": player_hand}

            score_package = game.package_send2.get(player)
            if score_package:
                game.package_send2.pop(player, None)
                return_dict["score_package"]=score_package
            return return_dict

    @xmlrpc.withRequest
    def xmlrpc_push_input(self, request, game_id, player_token, inp):
        GameMaster.__apply_CORS_headers(request)
        if not self.xmlrpc_validate(request, game_id, player_token=player_token):
            raise xmlrpc.Fault(GameErrors.INVALID_TOKEN, f"Invalid token, game pair presented")
        game = self.games[game_id]
        curr_state = game.state
        player = game.find_player(player_token)
        if game.turn == player:
            _ = game.step(inp)
        return True

    @xmlrpc.withRequest
    def xmlrpc_start_game(self, request, game_id, player_token):
        GameMaster.__apply_CORS_headers(request)
        if not self.xmlrpc_validate(request, game_id, player_token=player_token):
            raise xmlrpc.Fault(GameErrors.INVALID_TOKEN, f"Invalid token, game pair presented")
        game = self.games[game_id]
        game.init()
        players = game.step(None)
        # go to round init
        _ = game.step(players)
        return True

