# дурак - Card Game

дурак (translation: Moron) is a traditional Russian card game. 
The game is usually played between two or more players. 
However, in this implementation of the game, a single player faces a single AI player. 
The AI player has several different difficulty settings and playstyles.

## Game Rules

### Setup

The game is played with a deck of 36 playing cards. This deck is constructed by removing every 
card of rank 2-5 prior to the start of the game, as well as jokers. The 
deck is also shuffled before each round of the game.

The game begins with each player being dealt a hand of 6 cards. One card is 
placed face up on the bottom of the deck (it will be the last card to be drawn).
This card is visible to the players. The suit of that card is the trump suit for 
the current round of the game.

### Gameplay

The game is played in turns. Players take turns "attacking" their opponent.

#### Turns

The attacking player may play one card to the defending player. The defending
player has three options:

##### Defence 

The defending player may play any card from their hand onto the attacking card. 
The defending card must be of the same suit as the attacking card, and be of 
higher rank. Trump cards can be played on any suit, and outrank all other suits, 
although they keep their own rank hierarchy.

The attacking player may, following a defence, play another attacking card. Such 
a card must be of the same rank as one of the cards already in play - for 
example, if an attacking 6 was covered by a defending 7, the attacker may 
continue by playing another 6 or another 7. 

The turn continues until the attacker chooses not to continue the attack, the 
defender runs out of cards in their hand, or the defender surrenders (see below).

After the turn has finished, all the cards are discarded, and each player, 
starting with the attacker, draws back up to 6 cards in hand, if necessary.
After that, the defending player is the next to attack.

##### Reflection

Only if the defending player has not yet chosen to defend, they may play a card of 
the same rank as the attacking card. If they do, the players' roles are 
switched, (as if the previous defend is now attacking the former attacker with both the 
original attacking card and the new card of the same rank at the same time). The former attacker may take any of the three defender options, including reflecting all cards of the same rank back by playing another card of the same rank.

IMPORTANT: Once a defender has started defending against an attack, they may NOT
choose to reflect cards for the rest of the round. 

Once the turn is resolved, the original attacker draws up to 6 cards first, 
and then the opponent does. The player who was the last defender attacks next,
regardless of if they were the original attacker or not. 

##### Surrender

If a player chooses to, or if they are unable to reflect or defend against the
attack, they may instead choose to surrender. The player who surrenders must 
pick up all of the cards in play, including both the previous attacking cards and the cards the defending player used to cover them. 

### Resolving a Turn

A turn is resolved when the attacker chooses not to continue the attack, when the defender runs out of cards, or when the defender surrenders. When a turn is resolved, players draw from the deck up to 6 cards in their hand (until the deck runs out). The player who was the original attacker draws first.

#### Winning the Game

The object of the game is to run out of cards in your hand when the deck is
fully depleted. The player who empties their hand first wins the game. If both
players run out of cards in the same round, the game is a draw. 
