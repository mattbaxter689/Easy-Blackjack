import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:

    def __init__(self):
        self.deck = [] #start with an empty list
        for suit in suits:
            for rank in ranks:
                 self.deck.append(Card(suit, rank)) #build the Card objects and add to the list

    def __str__(self):
        deck_comp = '' #start with an empty string
        for card in self.deck:
            deck_comp += '\n ' + card.__str__() #add each Card object to the output
        return 'The deck has: '+ deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self):
        self.cards = [] #start with an empty list again
        self.value = 0 #start with a value of zero
        self.aces = 0 #this attribute keeps track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:

    def __init__(self):
        self.total = 100 #the base amount of chips for players. Could be any other value
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet: "))
        except ValueError:
            print("Sorry, bet must be an integer!")
        else:
            if chips.bet > chips.total:
                print("sorry, your bet can't exceed", chips.total)
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's': ")

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing")
            playing = False

        else:
            print("Sorry, please try again")
            continue
        break

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden> ")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep = '\n ') # '*' is used to print every item in a collection, and the sep arguement separates them on a separate line
    print("Player's hand total: ", player.value)

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer Busts")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()

def push(player, dealer):
    print("Player and Dealer Tie! It's a push.")

#Now add everything together to make the game!
while True:
    #print an opening statement
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #Set up the players chips
    player_chips = Chips() #default value was set to 100

    #Ask player for their bet
    take_bet(player_chips)

    #Show the cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:

        #ask the player if they want to hit
        hit_or_stand(deck, player_hand)

        #show the cards but keep the dealer hidden
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    #if the player's hasn't busted, play the dealers hand until the dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            print("\n")
            print("The dealer hits \n")
            hit(deck, dealer_hand)

            #show all of the cards
            show_all(player_hand, dealer_hand)

            #Run through different win scenarios
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
            
            else:
                push(player_hand, dealer_hand)

    #show the totals of both hands for both player and dealer
    show_all(player_hand, dealer_hand)

    #Inform the player of their chip total
    print("\n Player's winnings stand at", player_chips.total)

    #Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n': ")

    if new_game[0].lower() == 'y':
        playing = True
        continue

    else:
        print("Thanks for playing!")
        break