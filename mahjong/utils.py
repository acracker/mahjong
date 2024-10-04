import numpy as np
from mahjong.card import Card, Cards, Counter


card_encoding_dict = {}
num = 0
for _type in Card.CARD_INFO['type']:
    for _trait in Card.CARD_INFO['trait']:
        card = Card(_type, _trait)
        card_encoding_dict[card] = num
        num += 1
card_encoding_dict['pong'] = num
card_encoding_dict['gong'] = num + 1
card_encoding_dict['stand'] = num + 2

card_decoding_dict = {card_encoding_dict[key]: key for key in card_encoding_dict.keys()}


def init_deck():
    return init_cards()


def pile2list(pile):
    cards_list = []
    for each in pile:
        cards_list.extend(each)
    return Cards(cards_list)


def encode_cards(cards: Cards):
    if isinstance(cards, list):
        cards = Cards(cards)
    plane = np.zeros((27,4), dtype=int)
    # cards = cards2list(cards)
    for card, _ in cards.view_card_in_seq(copy=False):
        index = card_encoding_dict[card]
        num = cards.get_count_of_card(card)
        plane[index][:num] = 1
    return plane


# ****************************

def is_sequential(card, cards):
    try:
        return cards.counts[card.next_card(1)] > 0 and cards.counts[card.next_card(2)] > 0
    except KeyError:
        return False


def can_form_melds(cards: Cards):
    if sum(cards.counts.values()) == 0:
        return True
    for card, new_cards in cards.view_card_in_seq():
        if new_cards.get_count_of_card(card) >= 3:
            new_cards.remove(card, 3)
            if can_form_melds(new_cards):
                return True
            new_cards.add(card, 3)
        if is_sequential(card, new_cards):
            new_cards.remove(card)
            new_cards.remove(card.next_card(1))
            new_cards.remove(card.next_card(2))
            if can_form_melds(new_cards):
                return True
        return False
    return True


def is_winning(hand_cards: Cards):
    """
    是否和牌
    """
    if sum(hand_cards.counts.values()) % 3 != 2:
        return False
        # raise ValueError("恭喜,相公了! 手牌数量:%s" % len(hand_cards.cards))
    for card, cards in hand_cards.view_card_in_seq():
        try:
            cards.remove(card, 2)
            if can_form_melds(cards):
                return True
        except (KeyError,IndexError):
            pass
    return False


def init_cards():
    result = []
    for card_type in Card.CARD_INFO['type']:
        for trait in Card.CARD_INFO['trait']:
            for i in range(4):
                result.append(Card(card_type, trait))
    return Cards(result)
