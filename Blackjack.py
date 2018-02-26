
import random
import time

# Card variables
suits = ('H','D','S','C')
ranks = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')
values = {'A':11, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}


class Player(object):
    """
    A Blackjack player
    """
    def __init__(self,name,hand = [],balance = 500, bet = 0, status = ''):
        self.balance = balance
        self.name = name
        self.hand = hand
        self.bet = bet
        self.status = status
    
    def add_funds(self,add_amount):
        """
        :param add_amount: Amount of money to be added to the player's balance
        """
        self.balance += add_amount
    
    def sub_funds(self,sub_amount):
        self.balance += sub_amount
        
    def create_hand(self):
        """
        Creates a 'hand' object to store the player's cards
        :return: Hand object
        """
        self.hand = Hand()


class Card(object):
    """
    A playing card
    """
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.suit + self.rank
    
    def grab_suit(self):
        """
        :return: The suit of the card
        """
        return self.suit
    
    def grab_rank(self):
        """
        :return: The value of the card
        """
        return self.rank


class Deck(object):
    """
    A standard deck of 52 playing cards
    """
    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                card = Card(suit,rank)
                self.cards.append(card)
        
    def __str__(self):
        card_list = []
        for card in self.cards:
            card_list.append(str(card))
        return '\n'.join(card_list)
    
    def shuffle(self):
        """
        Shuffle the deck
        """
        random.shuffle(self.cards)
    
    def draw(self):
        """
        Draw a card from the deck
        :return: The drawn card
        """
        drawn_card = self.cards.pop()
        return drawn_card


class Hand(object):
    """
    An object for storing dealt cards
    """
    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace_count = 0
    
    def __str__(self):
        card_list = []
        for card in self.cards:
            card_list.append(str(card))
        return '\n'.join(card_list)
    
    def add_card(self, new_card):
        """
        Adds a new card to the hand and updates the value of the hand
        :param new_card: A new card, drawn from the deck
        """
        self.cards.append(new_card)
        if new_card.rank == 'A':
            self.ace_count += 1
        self.value += values[new_card.rank]
    
    def hand_value(self):
        """
        :return: The value of the hand, taking into account the variable value of Aces
        """
        if self.value < 22:
            return self.value
        elif self.ace_count == 0:
            return self.value
        elif self.ace_count == 1:
            return self.value - 10
        elif (self.ace_count == 2 and self.value - 10 < 22):
            return self.value - 10
        elif (self.ace_count == 2 and self.value - 20 < 22):
            return self.value - 20
        elif (self.ace_count == 3 and self.value - 20 < 22):
            return self.value - 20
        elif (self.ace_count == 3 and self.value - 30 < 22):
            return self.value - 30
        elif (self.ace_count == 4 and self.value - 30 < 22):
            return self.value - 30
        elif (self.ace_count == 4 and self.value - 40 < 22):
            return self.value - 40
        else:
            return self.value - self.ace_count * 10


def create_players():
    """
    Ask the user how many people will be playing the game and their names, and create one player object for each of
    them, plus a dealer.
    """
    global dealer
    global pl_store
    dealer = Player('Dealer', 10000)
    dealer.create_hand()
    while True:
        try:
            player_count = range(0, int(input('How many people want to play? ')))
        except:
            print('Please input a number (integer)')
        else:
            break
    pl_store = {}
    for num in player_count:
        pl_store[num] = Player(input('Player {pl_num}, what is your name? '.format(pl_num=num+1)))
    for p in pl_store:
        pl_store[p].create_hand()


def player_reset():
    """
    Reset player's status and hand, for playing additional hands
    """
    for p in pl_store:
        pl_store[p].create_hand()
        pl_store[p].status = ''
    dealer.create_hand()
    dealer.status = ''


def create_deck():
    """
    Create a shuffled deck object
    """
    global deck
    deck = Deck()
    deck.shuffle()


def place_bets():
    """
    Place Bets function - for taking player bets and ensuring they have sufficient funds
    """
    for p in pl_store:
        while True:
            try:
                pl_store[p].bet = int(input('{name}, your balance is {balance}. How much would you like to bet? '.format(name=pl_store[p].name, balance=pl_store[p].balance)))
                if pl_store[p].bet > pl_store[p].balance:
                    while True:
                        try:
                            pl_store[p].add_funds(int(input('You are out of funds. How much would you like to add to your balance? ')))
                        except:
                            print('Please input a number (integer)')
                        else:
                            break
            except:
                print('Please input a number (integer)')
            else:
                break
        pl_store[p].balance -= pl_store[p].bet
        print('Your remaining balance is {balance}'.format(balance=pl_store[p].balance))
    time.sleep(3)


def deal():
    """
    For the initial deal at the start of a hand
    """
    global deck
    card_count = 0
    while card_count < 2:
        for p in pl_store:
            pl_store[p].hand.add_card(deck.draw())
        dealer.hand.add_card(deck.draw())
        card_count += 1


def player_moves():
    """
    Player takes their move
    """
    for p in pl_store:
        print("\n{name}'s turn\n".format(name=pl_store[p].name))
        while pl_store[p].hand.hand_value() < 22:
            print('Face up dealer card: {card} \nValue: {value}'.format(card=dealer.hand.cards[0], value=values[dealer.hand.cards[0].rank]))
            print('Your cards:\n{cards}\nHand value:{value}'.format(cards=pl_store[p].hand, value=pl_store[p].hand.hand_value()))
            if pl_store[p].hand.hand_value() == 21:
                print('You have 21 so you must stand.')
                break
            else:    
                move = input('\nWould you like to hit or stand? ')
                if move.upper().startswith('H'):
                    pl_store[p].hand.add_card(deck.draw())
                    if pl_store[p].hand.hand_value() > 21:
                        print('\nNew card: {card}'.format(card=pl_store[p].hand.cards[-1]))
                        print('Hand value:{value}'.format(value=pl_store[p].hand.hand_value()))
                        print("You're bust!")
                        pl_store[p].status = 'Bust'
                    elif pl_store[p].hand.hand_value() == 21:
                        print('\nNew card: {card}'.format(card=pl_store[p].hand.cards[-1]))
                        print('Hand value:{value}'.format(value=pl_store[p].hand.hand_value()))
                        print('You have 21 so you must stand.')
                        break
                elif move.upper().startswith('S'):
                    break
                else:
                    continue
        time.sleep(5)


def show_dealer_hand():
    """
    Display the hand of the dealer
    """
    print('\nDealers full hand:\n{hand}'.format(hand = dealer.hand))
    print("Dealer's hand value: {value}".format(value = dealer.hand.hand_value()))


def dealer_moves():
    """
    Dealer takes their turn
    """
    while dealer.hand.hand_value() < 22:
        show_dealer_hand()
        time.sleep(3)
        if dealer.hand.hand_value() == 21:
            print('Dealer stands')
        elif dealer.hand.hand_value() < 17:
            print('Dealer hits')
            dealer.hand.add_card(deck.draw())
            if dealer.hand.hand_value() > 21:
                show_dealer_hand()
                print('The dealer is bust!')
                dealer.status = 'Bust'
            elif dealer.hand.hand_value() == 21:
                show_dealer_hand()
                print('Dealer stands')
                break
            else:
                continue
        else:
            print('Dealer stands')
            break
    time.sleep(5)


def process_results():
    """
    Process results to decide the outcomes following player and dealer moves
    """
    for p in pl_store:
        if pl_store[p].status == 'Bust':
            print('{name} is bust'.format(name=pl_store[p].name))
        else:
            print('{name} scored {score}'.format(name=pl_store[p].name, score=pl_store[p].hand.hand_value()))
    if dealer.status == 'Bust':
        print('The dealer is bust')
    else:
        print('The dealer scored {score}'.format(score=dealer.hand.hand_value()))
    for p in pl_store:
        if pl_store[p].status == 'Bust':
            pl_store[p].bet = 0
            print('{name} lost. New balance is {balance}'.format(name=pl_store[p].name, balance=pl_store[p].balance))
        elif (dealer.status == 'Bust' or pl_store[p].hand.hand_value() > dealer.hand.hand_value()):
            pl_store[p].balance += pl_store[p].bet*2
            pl_store[p].bet = 0
            print('{name} won! New balance is {balance}'.format(name=pl_store[p].name, balance=pl_store[p].balance))
        elif pl_store[p].hand.hand_value() < dealer.hand.hand_value():
            pl_store[p].bet = 0
            print('{name} lost. New balance is {balance}'.format(name=pl_store[p].name, balance=pl_store[p].balance))
        elif pl_store[p].hand.hand_value() == dealer.hand.hand_value():
            pl_store[p].balance += pl_store[p].bet
            pl_store[p].bet = 0
            print('{name} tied with the dealer. New balance is {balance}'.format(name=pl_store[p].name, balance=pl_store[p].balance))
        else:
            print('unexpected outcome for {name}'.format(name=pl_store[p].name))
        time.sleep(3)

# Game body
if __name__ == '__main__':
    play_again = True
    create_players()
    while play_again:
        create_deck()
        place_bets()
        deal()
        player_moves()
        dealer_moves()
        process_results()
        if input('Do you want to play again? ').upper().startswith('Y'):
            player_reset()
        else:
            play_again = False
            print('Thanks for playing - see you next time!')