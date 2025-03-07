from mahjong.card import Cards


class Player:

    def __init__(self, player_id):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.player_id = player_id
        self.hand = Cards()
        self.pile = []

    def get_player_id(self):
        ''' Return the id of the player
        '''

        return self.player_id

    def print_hand(self):
        ''' Print the cards in hand in string.
        '''
        print(self.hand)

    def print_pile(self):
        ''' Print the cards in pile of the player in string.
        '''
        for p in self.pile:
            print(p)

    def play_card(self, dealer, card):
        ''' Play one card
        Args:
            dealer (object): Dealer
            Card (object): The card to be play.
        '''
        self.hand.remove(card)
        dealer.table.append(card)

    def gong(self, dealer, cards):
        ''' Perform Gong
        Args:
            dealer (object): Dealer
            Cards (object): The cards to be Gong.
        '''
        for card in cards:
            self.hand.remove(card)
        self.pile.append(cards)

    def pong(self, dealer, cards):
        ''' Perform Pong
        Args:
            dealer (object): Dealer
            Cards (object): The cards to be Pong.
        '''
        for card in cards:
            self.hand.remove(card)
        self.pile.append(cards)
