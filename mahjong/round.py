import logging
from mahjong.dealer import Dealer
from mahjong.judger import Judger
from mahjong.card import Cards

logger = logging.getLogger(__name__)


class Round:

    def __init__(self, judger: Judger, dealer: Dealer, num_players):
        ''' Initialize the round class

        Args:
            judger (object): the object of MahjongJudger
            dealer (object): the object of MahjongDealer
            num_players (int): the number of players in game
        '''
        self.np_random = None
        self.judger = judger
        self.dealer = dealer
        self.target = None
        self.current_player = 0
        self.last_player = None
        self.num_players = num_players
        self.direction = 1
        self.played_cards = []
        self.is_over = False
        self.player_before_act = 0
        self.prev_status = None
        self.valid_act = False
        self.last_cards = []

    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            player (object): object of UnoPlayer
            action (str): string of legal action
        '''
        #hand_len = [len(p.hand) for p in players]
        #pile_len = [sum([len([c for c in p]) for p in pp.pile]) for pp in players]
        #total_len = [i + j for i, j in zip(hand_len, pile_len)]
        logger.info("self.current_player:%s, action:%s" % (self.current_player, action))
        if action == 'stand':
            self.last_player = self.current_player
            self.current_player = (self.player_before_act + 1) % self.num_players
            self.dealer.deal_cards(players[self.current_player], 1)
            self.valid_act = False
        elif action == 'gong':
            players[self.current_player].gong(self.dealer, self.last_cards)
            self.last_player = self.current_player
            self.valid_act = False

        elif action == 'pong':
            players[self.current_player].pong(self.dealer, self.last_cards)
            self.last_player = self.current_player
            self.valid_act = False

        elif action == 'chow':
            players[self.current_player].chow(self.dealer, self.last_cards)
            self.last_player = self.current_player
            self.valid_act = False
        elif action == 'over':
            pass
        else: # Play game: Proceed to next player
            players[self.current_player].play_card(self.dealer, action)
            self.player_before_act = self.current_player
            self.last_player = self.current_player
            (valid_act, player, cards) = self.judger.judge_pong_gong(self.dealer, players, self.last_player)
            if valid_act:
                self.valid_act = valid_act
                self.last_cards = cards
                self.last_player = self.current_player
                self.current_player = player.player_id
            else:
                self.last_player = self.current_player
                self.current_player = (self.current_player + 1) % self.num_players
                self.dealer.deal_cards(players[self.current_player], 1)
                # if self.dealer.deck.count > 0:
                #     self.last_player = self.current_player
                #     self.current_player = (self.current_player + 1) % self.num_players
                #     self.dealer.deal_cards(players[self.current_player], 1)
                # else:
                #     self.last_player = self.current_player
                #     self.current_player = -1

    def get_state(self, players, player_id):
        '''

        Args:
            players (list): The list of MahjongPlayer
            player_id (int): The id of the player
        Return:
            state (dict): The information of the state
        '''
        state = dict()
        if self.current_player == -1:
            state['valid_act'] = ['play']
            state['table'] = self.dealer.table
            state['player'] = self.current_player
            state['current_hand'] = Cards()
            state['players_pile'] = {}
            state['action_cards'] = []
            return state

        if self.valid_act: # PONG/GONG
            state['valid_act'] = [self.valid_act, 'stand']
            state['table'] = self.dealer.table
            state['player'] = self.current_player
            state['current_hand'] = players[self.current_player].hand
            state['players_pile'] = {p.player_id: p.pile for p in players}
            state['action_cards'] = self.last_cards # For doing action (pong, chow, gong)
        else: # Regular Play
            state['valid_act'] = ['play']
            state['table'] = self.dealer.table
            state['player'] = self.current_player
            state['current_hand'] = players[player_id].hand
            state['players_pile'] = {p.player_id: p.pile for p in players}
            state['action_cards'] = players[player_id].hand.cards # For doing action (pong, chow, gong)
        return state

