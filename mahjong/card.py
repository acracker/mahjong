# -*- coding: utf-8 -*-
import random
from bisect import bisect_left, insort_left
from collections import Counter, defaultdict


class Card:
    CARD_INFO = {
        'type': ['筒', '条', '万'],
        'trait': {1, 2, 3, 4, 5, 6, 7, 8, 9},
    }

    def __init__(self, *args):
        if len(args) == 2:
            card_type, trait = args
        elif len(args) == 1:
            trait = int(args[0][0])
            card_type = args[0][1]
        else:
            raise ValueError("error args:%s" % str(args))
        self.card_type = card_type
        self.trait = trait
        self.index_num = 0

    def __str__(self):
        return "%s%s" % (self.trait, self.card_type)

    def __repr__(self):
        return self.__str__()

    def next_card(self, offset=1):
        if self.trait + offset in self.CARD_INFO['trait']:
            return self.copy(self.card_type, self.trait + offset)
        else:
            raise KeyError

    @classmethod
    def from_str(cls, value):
        pass

    @classmethod
    def copy(cls, card_type, trait):
        return cls(card_type, trait)

    def __copy__(self):
        return self.copy(self.card_type, self.trait)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.card_type == other.card_type and self.trait == other.trait

    def __lt__(self, other):
        return (self.card_type, self.trait) < (other.card_type, other.trait)

    def __gt__(self, other):
        return (self.card_type, self.trait) > (other.card_type, other.trait)

    def __hash__(self):
        return hash((self.card_type, self.trait))


class Cards(object):

    def __init__(self, cards: list = None):
        cards = cards or []
        self.counts = Counter(cards)

    @property
    def cards(self):
        return sorted(self.counts.elements())

    @property
    def count(self):
        return sum(self.counts.values())

    def __copy__(self):
        return self.copy()

    def remove(self, card, num=1):
        """
        从 cards中删除指定打card， counts也对应减少
        :param card:
        :param num:
        :return:
        """
        if self.counts[card] < num:
            raise KeyError("牌不够了. card: %s" % card)
        self.counts[card] -= num
        return self

    def get_count_of_card(self, card):
        return self.counts.get(card, 0)

    def pop(self, card=None):
        """
                从剩余打牌中,发一张牌出去; 可以是玩家打出去; 或者 从剩余打牌中被摸了一张
        :param card: 可以指定要啥牌，默认就随机
        :return:
        """
        if card is None:
            card = random.choice(self.cards)
            self.counts[card] -= 1
            return card
        else:
            self.remove(card)
            return card

    def view_card_in_seq(self, copy=True):
        """
        按顺序展示一张牌， 返回两个数据， 打出牌和剩余的Cards
        :param copy: 是否复制本身
        :return:
        """
        for card, num in self.counts.items():
            if num == 0:
                continue
            if copy:
                yield card, self.copy()
            else:
                yield card, self

    def add(self, card, num=1, copy=False):
        if copy:
            inst = self.copy()
            inst.add(card, num)
            return inst
        else:
            self.counts[card] += num
            return self

    def append(self, card, num=1, copy=False):
        return self.add(card, num, copy=copy)

    def __repr__(self):
        return " ".join(map(str, self.cards))

    # def __next__(self):
    #     return iter(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def copy(self):
        inst = type(self)([])
        inst.counts = self.counts.copy()
        return inst
