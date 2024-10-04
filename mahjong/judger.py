# -*- coding: utf-8 -*-
from mahjong.dealer import Dealer
from mahjong.player import Player
from mahjong.utils import is_winning


class Judger:
    ''' Determine what cards a player can play
    '''

    @staticmethod
    def judge_pong_gong(dealer: Dealer, players: [Player], last_player):
        ''' Judge which player has pong/gong
        Args:
            dealer (object): The dealer object.
            players (list): List of all players
            last_player (int): The player id of last player

        '''
        last_card = dealer.table[-1]
        for player in players:
            if last_player == player.player_id:
                continue
            num = player.hand.get_count_of_card(last_card)
            if num == 3:
                return 'pong', player, [last_card] * 3
            elif num == 4:
                return 'gong', player, [last_card] * 4
        return False, None, None

    def judge_game(self, game):
        ''' Judge which player has win the game
        Args:
            dealer (object): The dealer object.
            players (list): List of all players
            last_player (int): The player id of last player
        '''
        players_val = []
        win_player = -1
        for player in game.players:
            win, val = self.judge_hu(player)
            players_val.append(val)
            if win:
                win_player = player.player_id
        if win_player != -1 or game.dealer.deck.count == 0:
            # todo 通炮
            return True, win_player, players_val
        else:
            #player_id = players_val.index(max(players_val))
            return False, win_player, players_val

    def judge_hu(self, player):
        flag = is_winning(player.hand)
        if flag:
            return flag, 1  # 先不计算番数
        else:
            return flag, 0
