import random
import itertools

class Card:
    '''
    A Card is a data class that stores a rank and a suit. It also knows whether it is a trump or not.
    '''
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.is_trump = False

    def rank_name(self):
        '''
        Return the English name of the card's rank (named cards are internally stored as numbers above 10).
        '''
        match self.rank:
            case 11:
                return "Jack"
            case 12:
                return "Queen"
            case 13:
                return "King"
            case 14:
                return "Ace"
            case _:
                return str(self.rank)

    def suit_name(self):
        '''
        Return the English  name of the card's suit (internally, the suits are stored as numbers).
        '''
        match self.suit:
            case 0:
                return "Spades"
            case 1: 
                return "Hearts"
            case 2: 
                return "Clubs"
            case 3:
                return "Diamonds"

    def __str__(self):
        if self.is_trump: # In this case, highlight the card a bit more
            result = f"***{self.rank_name()} of {self.suit_name()}***"
            return result.upper()
        else: 
            return f"{self.rank_name()} of {self.suit_name()}"
class Deck:
    '''
    A Deck is a class that stores a list of 36 cards, from 6s to aces, of each suit.
    Decks can be shuffled, which randomly rearranges the order of the cards.
    '''
    def __init__(self):
        self.cards = []
        self.trump_card = None
        for s in range(0, 4): # suits range from 0 to 3, and their names are stored internally in the card
            for i in range(6, 15): # ranks range from 6 to 14, where jack = 11, queen = 12, king = 13, ace = 14
                self.cards.append(Card(i, s)) #add cards to the deck in order

    def shuffle(self):
        '''Shuffle the cards stored in this deck.'''
        random.shuffle(self.cards)

    def draw(self):
        '''Remove the top (i.e. the last) card from the Deck, and return it.'''
        return self.cards.pop()
    
    def choose_trump(self):
        '''Take the first card and put it on the bottom, "face up". This should only be called once per game.'''
        self.trump_card = self.draw()
        self.cards.insert(0, self.trump_card)
        for c in self.cards:
            if c.suit == self.trump_card.suit:
                c.is_trump = True


class Player:
    '''A Player is a class representing one of the players of the game.'''
    def __init__(self, name):
        self.hand = []
        self.name = name
     
    def num_cards(self):
        '''Return True if the player's hand is empty, and False otherwise.'''
        return len(self.hand)
    
    def sort_hand(self):
        '''Sort the player's hand by suit, and by ascending order of value within each suit.'''

        # Sort by rank, except for trumps - put them at the end of the hand. 
        self.hand.sort(key=lambda card: card.rank) #Sort the hand in ascending order by rank

        trumps = []
        for i in range(len(self.hand)):
            if self.hand[i].is_trump: 
                trumps.append(self.hand.pop(i))
                i -= 1 # To avoid skipping a card
        
        for c in trumps: #Place all trumps at the end
            self.hand.append(c)


        """ 
        # Sort by suits, and then sort by rank within each suit. 
        spades, hearts, clubs, diamonds = suitlist = [[] for _ in range(4)]
        for c in self.hand:
            suitlist[c.suit].append(c) # Split the hand into suits

        for s in suitlist:
            s.sort(key=lambda card: card.rank) #Sort each suit in ascending order

        self.hand = list(itertools.chain.from_iterable(suitlist)) # Join suits back into one hand.  """
        




    def __str__(self):
        '''Overridden to output the player's hand, separated by new lines.'''
        return "\n".join(self.hand)

class HumanPlayer(Player):
    '''A HumanPlayer is a Player that can take user input for moves.'''
    def __init__(self, name):
        super(self, name)



class Game:
    '''
    A Game is a class representing an individual game. Games are the main class of this project. Each game has its own Deck, Players, and so on.
    The Game class is responsible for running the game, including taking user input. 
    '''
    def __init__(self, p1name, p2name):
        self.player1 = HumanPlayer(p1name)
        match p2name:
            case _:
                self.player2 = HumanPlayer(p2name)
                self.both_human = True
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.choose_trump()
        self.trump = self.deck.trump_card.suit
        self.end = None

    def start_game(self): #TODO

        while not self.end: # Game loop
            




if __name__ == "__main__":
    
    input('press any key to finish')
    
