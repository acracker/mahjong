# -*- coding: utf-8 -*-

import random
import logging
from mahjong.utils import init_deck
from mahjong.card import Cards
from mahjong.player import Player

logger = logging.getLogger(__name__)


class Dealer:
    ''' Initialize a mahjong dealer class
    '''
    def __init__(self):
        self.deck = init_deck()
        self.table = []

    def deal_cards(self, player: Player, num: int):
        ''' Deal some cards from deck to one player

        Args:
            player (object): The object of DoudizhuPlayer
            num (int): The number of cards to be dealed
        '''
        for _ in range(num):
            card = self.deck.pop()
            player.hand.append(card)
            # logger.debug("deal card. player:%s, card:%s" % (player.get_player_id(), card))

