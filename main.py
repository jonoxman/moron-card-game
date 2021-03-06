import random

class card:
    '''
    A card is a data class that stores a rank and a suit.
    '''
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

class deck:
    '''
    A deck is a class that stores a list of 36 cards, from 6s to aces, of each suit.
    Decks can be shuffled, which randomly rearranges the order of the cards.
    '''
    def __init__(self):
        self.cards = []
        suits = ["spades", "hearts", "clubs", "diamonds"]
        for s in suits:
            for i in range(6, 15): #ranks range from 6 to 14, where jack = 11, queen = 12, king = 13, ace = 14
                self.cards.append(card(i, s)) #add cards to the deck in order

    def shuffle(self):
        """Shuffle the cards stored in this deck."""
        random.shuffle(self.cards)
    
if __name__ == "__main__":
    d = deck()
    for c in d.cards:
        print(c.suit)
        print(c.rank)
    
    d.shuffle()
    for c in d.cards:
        print(c.suit)
        print(c.rank)
    
    input('press any key to finish')
    
