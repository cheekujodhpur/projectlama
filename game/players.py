from .utils import prompter
import numpy

class node:
    def __init__(self, index_list):
        self.index_list = index_list
        #First Value corresponds to Play/Draw
        #As of now, Play refers to playing ANY card in the deck
        #Second Value corresponds to Fold
        self.Q_VALUES = numpy.random.rand(2)

class Player:
    def __init__(self, Q = False, auto=False):
        self.auto = auto
        self.hand = []
        self.active = True
        self.isbot = False
        self.isQbot = Q
        self.score = 0
        if Q:
            #New parameters added from here
            self.isQbot = False
            self.Q_HASH_TABLE = numpy.empty( 8889, dtype=object )
            self.ALPHA = 0.2
            self.COMPL_REWARD = 10.0
            #self.PLAY_REWARD defined later
            self.DRAW_PENALTY = (-0.5)
            #self.FOLD_PENALTY defined later

    def init(self):
        self.hand = []
        self.activate()

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def bot(self):
        self.isbot = True

    def draw(self, deck):
        self.hand.append(deck.main_pile.pop())

    def calc_score(self):
        if not len(self.hand):
            if not self.score:
                self.score = 0
            # TODO: Ideally the following should be a choice
            elif self.score < 10:
                self.score = self.score - 1
            else:
                self.score = self.score - 10
        else:
            uniq_hand = list(set(self.hand))
            increment = sum(map(lambda x: x if x < 7 else 10, uniq_hand))
            self.score = self.score + increment
        return self.score

    def delete(self, n):
        i = 0
        while i < len(self.hand):
            if self.hand[i] == n:
                return self.hand.pop(i)
            i = i + 1

    ####### All Changes start from here #########

    def encode(self, deck):
    #Encodes the discard pile only as of now
    #Units is tc; the rest are number of cards for 1,2,..
        index = 0
        tc = deck.discard_pile[-1]
        index = index + tc
        for x in deck.discard_pile:
            index = index + int(pow(10, x))
        index = index - int(pow(10, tc))
        return index  

    def playable(self, deck):
        for card in self.hand:
            if card ==  deck.discard_pile[-1] or card == plus_one(deck.discard_pile[-1]):
                return True

        return False

    def bot_score(self, hand):
        score = 0
        uniq_hand = list(set(hand))
        increment = sum(map(lambda x: x if x < 7 else 10, uniq_hand))
        score = score + increment
        return score

    def Q_Bot_AI(self, deck):
        index_act = self.encode(deck)
        index_arr = int(index_act/10000)
        index_list = int(index_act%10000)

        if self.Q_HASH_TABLE[index_arr] is None:
            new = node(index_list)
            self.Q_HASH_TABLE[index_arr] = [new]

        else:
            for node in Q_HASH_TABLE[index_arr]:
                if node.index_list == index_list:
                    ###This Part contains the action and the updating of Q_VALUES###
                    if node.Q_VALUES[0] < node.Q_VALUES[1]:
                        if not self.playable(deck):
                            node.Q_VALUES[0] = (1-self.ALPHA)*(node.Q_VALUES[0]) + (self.ALPHA)*(self.DRAW_PENALTY)
                            return "Draw"
                        else:
                            for card in self.hand:
                                if card ==  deck.discard_pile[-1] or card == plus_one(deck.discard_pile[-1]):
                                    self.PLAY_REWARD = card * (0.1)
                                    node.Q_VALUES[0] = (1-self.ALPHA)*(node.Q_VALUES[0]) + (self.ALPHA)*(self.PLAY_REWARD)
                                    return card

                    else:
                        temp_score = self.bot_score(self.hand)
                        self.FOLD_PENALTY = (-1*temp_score)/10
                        node.Q_VALUES[1] = (1-self.ALPHA)*(node.Q_VALUES[1]) + (self.ALPHA)*(self.FOLD_PENALTY)
                        return "Fold"

            #If the index hasn't been called yet
            new = node(index_list)
            self.Q_HASH_TABLE[index_arr].append(new)
            return self.Q_Bot_AI(deck)



class NetworkPlayer(Player):
    def __init__(self, alias, token, Q = False):
        self.alias = alias
        self.token = token
        super().__init__(Q)

