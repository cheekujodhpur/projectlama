from .utils import plus_one
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
        if self.isQbot:
            #New parameters added from here
            self.ROUND_REW = 0
            self.ROUND_PEN = 0

            self.Q_HASH_TABLE = numpy.empty( 8889, dtype=object )
            self.ALPHA = 0.2
            self.DISCOUNT_FACTOR = 0.8
            #The state can never be 0, so it's okay to initialise as such
            self.PREV_STATE = 0
            self.CURR_STATE = 0

            self.PREV_REWARD = 0
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

    def bot(self, Q):
        self.isbot = True
        self.isQbot = Q

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

    def R_Rew(self):
        return self.ROUND_REW

    def R_Pen(self):
        return self.ROUND_PEN

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

    def Q_node(self, index_act):
        index_arr = int(index_act/10000)
        index_list = int(index_act%10000)

        for nodes in self.Q_HASH_TABLE[index_arr]:
            if nodes.index_list == index_list:
                return nodes
        return False


    def Q_Bot_AI(self, deck):
        if self.active == False:
            return None
        else:
            index_act = self.encode(deck)
            index_arr = int(index_act/10000)
            index_list = int(index_act%10000)

            if self.PREV_STATE == 0:
                self.PREV_STATE = index_act
            self.CURR_STATE = index_act

            if self.Q_HASH_TABLE[index_arr] is None:
                new = node(index_list)
                self.Q_HASH_TABLE[index_arr] = [new]
                nodes = new

            elif self.Q_node(index_act) is False:
                new = node(index_list)
                self.Q_HASH_TABLE[index_arr].append(new)
                nodes = new

            else:
                nodes = self.Q_node(index_act)
            
            ###This Part contains the action and the updating of Q_VALUES###
            if nodes.Q_VALUES[0] > nodes.Q_VALUES[1]:
                if not self.playable(deck):
                    if self.PREV_STATE != self.CURR_STATE:
                        self.Q_node(self.PREV_STATE).Q_VALUES[self.PREV_ACT] = (1-self.ALPHA)*(self.Q_node(self.PREV_STATE).Q_VALUES[self.PREV_ACT]) + (self.ALPHA)*((self.PREV_REWARD) + self.DISCOUNT_FACTOR*(nodes.Q_VALUES[0]))
                    self.PREV_REWARD = self.DRAW_PENALTY
                    self.ROUND_PEN+=self.DRAW_PENALTY
                    self.PREV_STATE = self.CURR_STATE
                    self.PREV_ACT = 0
                    return "Draw"
                else:
                    for card in self.hand:
                        if card ==  deck.discard_pile[-1] or card == plus_one(deck.discard_pile[-1]):
                            self.PLAY_REWARD = card * (0.1) 
                            self.ROUND_REW+=self.PLAY_REWARD
                            if self.PREV_STATE != self.CURR_STATE:
                                self.Q_node(self.PREV_STATE).Q_VALUES[self.PREV_ACT] = (1-self.ALPHA)*(self.Q_node(self.PREV_STATE).Q_VALUES[self.PREV_ACT]) + (self.ALPHA)*((self.PREV_REWARD) + self.DISCOUNT_FACTOR*(nodes.Q_VALUES[0]))
                                if len(self.hand) == 1:
                                    self.Q_node(self.PREV_STATE).Q_VALUES[self.PREV_ACT] = (1-self.ALPHA)*(self.Q_node(self.PREV_STATE).Q_VALUES[self.PREV_ACT]) + (self.ALPHA)*((self.PREV_REWARD) + self.DISCOUNT_FACTOR*(nodes.Q_VALUES[0]))
                                    self.ROUND_REW+=self.COMPL_REWARD
                            self.PREV_REWARD = self.PLAY_REWARD
                            self.PREV_STATE = self.CURR_STATE
                            self.PREV_ACT = 0
                            return card
            else:
                temp_score = self.bot_score(self.hand)
                if temp_score > 13:
                    self.FOLD_PENALTY = -5
                else:
                    self.FOLD_PENALTY = (-1*temp_score)/10
                if self.PREV_STATE != self.CURR_STATE:
                    #Update Previous State
                    self.Q_node(self.PREV_STATE).Q_VALUES[self.PREV_ACT] = (1-self.ALPHA)*(self.Q_node(self.PREV_STATE).Q_VALUES[self.PREV_ACT]) + (self.ALPHA)*((self.PREV_REWARD) + self.DISCOUNT_FACTOR*(nodes.Q_VALUES[1]))
                #Update Current State
                nodes.Q_VALUES[1] = (1-self.ALPHA)*(nodes.Q_VALUES[1]) + (self.ALPHA)*((self.FOLD_PENALTY) + self.DISCOUNT_FACTOR*(nodes.Q_VALUES[1]))
                self.PREV_REWARD = self.FOLD_PENALTY
                self.ROUND_PEN+=self.FOLD_PENALTY
                self.PREV_STATE = self.CURR_STATE
                self.PREV_ACT = 1
                return "Fold"


class NetworkPlayer(Player):
    def __init__(self, alias, token, Q = False):
        self.alias = alias
        self.token = token
        super().__init__(Q)

