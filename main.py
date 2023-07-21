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

    @staticmethod
    def rank_to_name(rank):
        '''
        Return the English name of a card's rank, given the rank id (named cards are internally stored as numbers above 10).
        '''
        match rank:
            case 11:
                return "Jack"
            case 12:
                return "Queen"
            case 13:
                return "King"
            case 14:
                return "Ace"
            case _:
                return str(rank)
            
    @staticmethod
    def lt_several(first, second):
        '''
        Precondition: first and second have the same length.
        Given two lists of cards of equal length, compare them pairwise by index. Returns True if in every pair, the first card is less than the second card.
        Returns False otherwise. 
        '''
        for i in range(len(first)):
            if not (first[i] < second[i]):
                return False
        return True

    def rank_name(self):
        '''
        Return the English name of the card's rank (named cards are internally stored as numbers above 10).
        '''
        return Card.rank_to_name(self.rank)

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

    def __lt__(self, other):
        # A card is less than another if it has lower rank and they are the same suit, or if the other card is a trump and they have different suits. 
        if self.suit == other.suit:
            if self.rank < other.rank: 
                return True
        elif other.is_trump: 
            return True
        return False

    def __repr__(self):
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

    def num_cards(self):
        return len(self.cards)
    
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
    
    def get_rank_classes(self):
        '''
        Returns a dict with keys being ranks of cards in hand, and values being a set of all cards in the hand with rank being the key. 
        '''
        result = {}
        for card in self.hand:
            if card.rank in result:
                result[card.rank].add(card)
            else:
                result[card.rank] = set()
                result[card.rank].add(card)
        return result

    def valid_attacks(self, _playable_ranks):
        '''Given the current playable ranks, return a set of valid sets of attacking cards that the Player can play next in the current round, assuming it is the player's turn.'''
        candidates = self.get_rank_classes()
        result = set()
        for c in candidates:
            if c in _playable_ranks or not _playable_ranks:
                for i in range(len(candidates[c])):
                    result = result.union(set(frozenset(x) for x in itertools.combinations(candidates[c], i + 1)))
        return result
    
    def valid_defenses(self, _incoming):
        '''Given the current incoming attacking cards, return a set of valid defences (i.e. order does not matter).'''
        beaters = [] # A list of tuples consisting of each incoming card, and a list of cards in the hand that beat them. 
        for i in range(len(_incoming)):
            beaters.append((_incoming[i], []))
            for c in self.hand:
                if c > _incoming[i]:
                    beaters[i][1].append(c)
        # For each incoming card, we have a list of all cards that beat it. Now, we construct a defense by playing one card at a time.
        # We will find valid defenses by means of a tree search. 
        
        def make_defense_tree(curr_beaters, curr_solution):
            '''Recursively generate a tree of all possible defenses. Return a list of all values of leaves in the tree, from the given current node.
            Takes a nonempty list of beating cards as generated above, as well as a Set representing the partial solution constructed at the current node.
            The algorithm is as follows: Take the first incoming card. Try to cover it with every possible option, removing this option from the other incoming cards' lists. Recurse, removing the first incoming card each time.
            Note that it is sufficient to consider the first card first, as in all valid defenses, this card must be covered at some point. '''
            if not curr_beaters:
                return frozenset([frozenset(curr_solution)]) # We use sets to reduce the space taken by, multiple defenses in different orders (common occurrence with, say, multiple trumps)
            result = set()
            for card in curr_beaters[0][1]:
                if card not in curr_solution:
                    result = result.union(make_defense_tree(curr_beaters[1:], curr_solution.union(set([card]))))
            return frozenset(result) # If there are no solutions, we return an empty set. 
        result = make_defense_tree(beaters, set())
        foo = frozenset()
        if foo in result:
            result.remove(foo)

        return result
    
    def valid_reflections(self): #TODO
        return None

    def sort_hand(self):
        '''Sort the player's hand by suit, and by ascending order of value within each suit.'''

        # Sort by rank, except for trumps - put them at the end of the hand. 
        self.hand.sort(key=lambda card: card.rank) #Sort the hand in ascending order by rank

        trumps = []
        i = 0 
        # This is a little awkward. I don't want to use a usual for loop with range, because I want to decrement the index when necessary. It's either this, or a while loop.
        # The length of the hand can never change in the middle of the sort, so this is good enough (and I believe, slightly faster).
        for _ in itertools.repeat(None, self.num_cards()):
            if self.hand[i].is_trump: 
                trumps.append(self.hand.pop(i))
            else:
                i += 1
        
        self.hand.extend(trumps) #Place all trumps at the end
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
        super().__init__(name)

    def generate_attack(self, playable_ranks):
        '''Generates an attack (in the case of the human player, "generation" is made via user input).
        Takes a parameter of the current card pool (i.e. which cards have been played this round). If this parameter is an empty list, any card may be played.
        Returns a tuple consisting the card to be played, and its position in the hand after sorting. 
        A return value of None indicates that the attacker does not wish to continue the attack.
        '''
        nl = "\n" # Escape sequences are not allowed in f-strings.
        self.sort_hand() # This can be done here, since the only purpose of sorting your hand is for readability.
        print(f"\n{self.name}, you have {self.num_cards()} cards. ")
        if not playable_ranks:
            print ("\nNo cards have been played yet, so you may attack with any card.")
        else:
            print (f"\nIn this round so far, cards with rank {', '.join(Card.rank_to_name(rank) for rank in playable_ranks)} have been played.")
        print(f"\nYour cards are:\n{nl.join(f'{i + 1}. {self.hand[i]}' for i in range(self.num_cards()))}")
        invalid_input = True
        v_a = self.valid_attacks(playable_ranks)
        while invalid_input:
            s = input("\nWhat would you like to attack with? Enter a number displayed above, or 'pass' if you are done attacking:\n")
            if not (s == 'pass' or (s.isdigit() and int(s) <= self.num_cards() and int(s) != 0)): # An absolutely invalid input was made
                print("Invalid input.")
            elif s == 'pass': # 'pass' was inputed
                if not playable_ranks: # playable_ranks is empty, so this is the first attack of the round.
                    print("You cannot pass on your first attack of the round!")
                else:
                    invalid_input = False
                    result = None
            else: # We have a valid numerical input
                index = int(s) - 1
                if self.hand[index] in v_a:
                    invalid_input = False
                    result = (self.hand[index], index)
                else: # If we got here, playable_ranks is not empty, so this will never look bad
                    print(f"You cannot play that card! The available plays are: {', '.join(f'{Card.rank_to_name(rank)}' for rank in playable_ranks)}")
        return result

    def generate_defense(self, incoming, ref_allowed):
        '''Generates a defense (in the case of the human player, "generation" is made via user input).
        Takes a parameter of the incoming cards (i.e. which cards must be defended against.), and whether a reflection is allowed (i.e. if this is the prospective first defense of the round).
        Returns a tuple consisting of a list of cards to be played from the player's hand, 
        and a list with the indices of the cards being played in the hand after sorting.
        A return value of None indicates that the defender has surrendered. 
        '''
        nl = "\n" # Escape sequences are not allowed in f-strings.
        self.sort_hand()
        print(f"\n{self.name}, you have {self.num_cards()} cards. ")
        print(f"\nYou are being attacked by the following cards: {', '.join(str(card) for card in incoming)}")
        print(f"\nYour cards are:\n{nl.join(f'{i + 1}. {self.hand[i]}' for i in range(self.num_cards()))}")
        invalid_input = True
        v_d = self.valid_defenses(incoming)
        while invalid_input:
            s = input("\nWhat would you like to defend with? Enter a sequence of as many numbers as attacking cards, representing the cards you want to use in the order you want to use them, separated by \
spaces (for example, '1 2 4'), or 'surrender' if you give up:\n")
            indices = s.split(" ")
            if not (s == 'surrender' or (all(x.isdigit() and int(x) <= self.num_cards() and int(x) != 0 for x in indices)) and len(indices) == len(incoming)): # An absolutely invalid input was made
                print("Invalid input.")
            elif s == 'surrender': # 'surrender' was inputted
                invalid_input = False
                result = None
            else: # We have a valid numerical input
                indices = [(int(x) - 1) for x in indices]
                defense_attempt = frozenset([self.hand[i] for i in indices])
                if defense_attempt in v_d:
                    return defense_attempt
                else: 
                    #TODO: It would be good to be more verbose about *why* the defense failed (which card failed to be defended against, for example)
                    print(f"\nYou entered an invalid defense!\nYou are being attacked by the following cards: {', '.join(str(card) for card in incoming)}.\nIf you cannot defend yourself, you must surrender.")
        return result
class Game:
    '''
    A Game is a class representing an individual game. Games are the main class of this project. Each game has its own Deck, Players, and so on.
    The Game class is responsible for running the game, including taking user input. 
    '''

    class RoundResult:
        '''A RoundResult is a data class consisting of three elements:
        1. The result of the round (i.e. which player "won", that is, which player plays next). This is a Player object.
        2. The cards to be added to the attacker's hand after the round. If this is a number, the attacker draws this many cards. If it is a list of cards, each card is added.
        3. The cards to be added to the defender's hand after the round. If this is a number, the defender draws this many cards. If it is a list of cards, each card is added. 
        Note: Elements 2 and 3 can only be lists in the case of one player surrendering.
        '''

        def __init__(self, _winner, c1, c2):
            self.winner = _winner
            self.attacker_draw = c1
            self.defender_draw = c2

    class Round:
        '''A Round is a class representing a single round of the game. The round keeps track of each player's hand, the cards on the field, and the valid moves each player can make.
        When a round is initialized, the first player passed into it is the attacker for the round, and is the one who is prompted for attack. 
        The Round class keeps track of which player was the original attacker, since this player must draw first regardless of whether a reflection was played.'''
        
        def __init__(self, p1, p2, d):
            self.attacker = p1
            self.defender = p2
            self.deck = d
            self.attacking_cards = []
            self.card_pool = []
            self.result = None
        
        def execute_move(self, player, _cards):
            '''Execute a move, passed in as a parameter in the form of the player moving, and the cards they are using.
            This method assumes that the specified move is valid - this should be verified before calling this method.'''
            cards = set(_cards)
            player.hand = list(set(player.hand) - cards)
            self.card_pool.extend(cards)
            

        def round_info(self, defender_turn):
            '''
            Returns information about current status of the round in String form. (This is a helper method for output only.)
            The status includes:
            - The name of the player whose move it is, and their current position (attacker or defender). 
            - The number of cards each player has.
            - If it is the defender's turn, the current attacking card(s) in play.
            - If it is the attacker's turn, and a card has already been played, the current pool of playable cards for additional attacks.
            '''

            if defender_turn:
                p = self.defender
                s = "defending"
                sentence = f"You need to defend against {', '.join(card for card in self.attacking_cards)}."
            else:
                p = self.attacker
                s = "attacking"
                sentence = f"The cards that have been played so far are {', '.join(card for card in self.card_pool)}."

            result = f"{p.name}, it's your turn. You are currently {s}. {sentence}"
            return result


        def start_round(self):
            # It's the attacker's turn first.
            winner = None
            while not winner:
                print(self.round_info(), False)
                attack = self.attacker.generate_attack()
                if not attack: # In the first loop, generate_attack does not allow this case
                    winner = self.defender
                    break
                else:
                    self.execute_move(self.attacker, attack)
                print(self.round_info(), True)
                defense = self.defender.generate_defense()
                if not defense:
                    winner = self.attacker
                    break
                else:
                    self.execute_move(self.defender, defense)
            return self.winner # The return value is the player object of the winning player.


    def __init__(self, p1name, p2name):
        self.player1 = HumanPlayer(p1name)
        match p2name:
            case _:
                self.player2 = HumanPlayer(p2name)
                self.both_human = True # The point of this flag is to know whether we should clear the whole screen when each player plays (to prevent each player from seeing the other's hand).
        self.deck = Deck()
        self.deck.shuffle()
        self.deck.choose_trump()
        self.trump = self.deck.trump_card.suit
        self.winning_player = None

    #def start_game(self): 

       # while not self.winning_player: # Game loop

if __name__ == "__main__":
    d = Deck()
    d.shuffle()
    d.choose_trump()

    c1 = d.draw()
    c2 = d.draw()

    print(f"Trumps are {d.trump_card}")
    p = HumanPlayer("Player")
    for i in range(6):
        p.hand.append(d.draw())

    print(p.get_rank_classes())

    print(p.valid_attacks([]))