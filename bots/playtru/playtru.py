#!/usr/bin/env python
"""
This is a bot that applies personal logic of playing the game.
The strategy consists of making opponent and yourself "play" trumps as soon as possible, if you have many.
If you don't have many, then keep the trumps for the phase two, because then the winning of points is more likely.
"""

from api import State, util, Deck
import random
# from . import load
# from .kb import KB, Boolean, Integer


def get_card_value(card):
    rank = card[0]
    if rank == 0 or 5 or 10 or 15:      # ACES
        value = 11
    elif rank == 1 or 6 or 11 or 16:    # 10s
        value = 10
    elif rank == 2 or 7 or 12 or 17:    # Kings
        value = 4
    elif rank == 3 or 8 or 13 or 18:    # Queens
        value = 3
    else:                               # Jacks
        value = 2
    return value


def sort_cards(tuple):
    tuple.sort(key=lambda x: x[0])
    print("IT'S SORTED!")
    print(tuple)
    return


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # Determine are you player 1 or 2
        player = state.whose_turn()
        print("This is the player who plays: ", player)

        # Get all legal moves
        moves = state.moves()
        print("MOVES:", moves)

        # Different "good" moves starting lists
        trumps = []
        high_cards = []
        low_cards = []
        good_moves = []
        safe_moves = []
        if player == 1:
            # GET ALL TRUMPS suit moves available
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                    trumps.append(move)
                    print("Trump moves: ", trumps)
                    print(enumerate(moves))
                # Get all valid aces
                elif get_card_value(move[0]) == 11:
                    high_cards.append(move)
                    print("ACES: ", high_cards)
                # Get all valid 10s
                elif get_card_value(move[0]) == 10:
                    high_cards.append(move)
                    print("10s: ", high_cards)
                # Get low cards
                else:
                    low_cards.append(move)
                    print("Low moves: ", low_cards)

            # IF more than 3 trump cards in hand, try to win the trick by playing the trump (AGGRESSIVE TRUMP PLAY)
            # If low number of trumps, we keep the cards for phase 2 (PASSIVE PLAY)
            if len(trumps) > 2:
                chosen_move = trumps[0]
            elif len(high_cards) > 1:
                chosen_move = high_cards[0]
            else:
                chosen_move = low_cards[0]
            return chosen_move

            # If the opponent has played a card
        else:
            moves_same_suit = []
            trumps = []
            high_cards = []
            low_cards = []
            good_moves = []
            safe_moves = []
            # Get all moves of the same suit as the opponent's played card, trying to win the trick
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) == Deck.get_suit(state.get_opponents_played_card()):
                    moves_same_suit.append(move)
                # Get all trumps
                elif move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                    trumps.append(move)
                # Get all valid aces
                elif get_card_value(move[0]) == 11:
                    high_cards.append(move)
                # Get all valid 10s
                elif get_card_value(move[0]) == 10:
                    high_cards.append(move)
                # Get low cards
                else:
                    low_cards.append(move)

            if len(moves_same_suit) > 0:
                chosen_move = moves_same_suit[0]
                return chosen_move

        print("Trumps: ", trumps)
        print("High cards:", high_cards)
        print("Low cards: ", low_cards)
        print("Safe moves: ", safe_moves)
        print("Good moves: ", good_moves)
