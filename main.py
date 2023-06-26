import random

class Card:
    '''
    A Card is a data class that stores a rank and a suit.
    '''
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def rank_name(self):
        '''
        Return the English name of the card's rank (named cards are internally stored as numbers above 10).
        '''
        if self.rank <= 10:
            return str(self.rank)
        elif self.rank == 11:
            return "Jack"
        elif self.rank == 12:
            return "Queen"
        elif self.rank == 13:
            return "King"
        else:
            return "Ace"

    def suit_name(self):
        '''
        Return the English  name of the card's suit (internally, the suits are stored as numbers).
        '''
        if self.suit == 0: 
            return "Spades"
        elif self.suit == 1:
            return "Hearts"
        elif self.suit == 2:
            return "Clubs"
        else:
            return "Diamonds"

    def __str__(self):
        return self.rank_name() + " of " + self.suit_name()


class Deck:
    '''
    A Deck is a class that stores a list of 36 cards, from 6s to aces, of each suit.
    Decks can be shuffled, which randomly rearranges the order of the cards.
    '''
    def __init__(self):
        self.cards = []
        for s in range(0, 4): # suits range from 0 to 3, and their names are stored internally in the card
            for i in range(6, 15): # ranks range from 6 to 14, where jack = 11, queen = 12, king = 13, ace = 14
                self.cards.append(Card(i, s)) #add cards to the deck in order

    def shuffle(self):
        '''Shuffle the cards stored in this deck.'''
        random.shuffle(self.cards)

class Player:
    '''A Player is a class representing one of the players of the game.'''
    def __init__(self, name):
        self.cards = []
        self.name = name
    
    def empty(self):
        '''Return True if the Hand is empty, and False otherwise.'''
        return len(self.cards) == 0


class HumanPlayer(Player):
    '''A HumanPlayer is a Player that can take user input for moves.'''
    def __init__(self, name):
        super(self, name)

if __name__ == "__main__":
    d = Deck()
    for c in d.cards:
        print(c.suit)
        print(c.rank)
    
    d.shuffle()
    for c in d.cards:
        print(c.suit)
        print(c.rank)
    
    input('press any key to finish')
    
