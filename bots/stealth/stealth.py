#!/usr/bin/env python
"""
This is a bot that applies personal stealth strategy of playing the game Schnapsen.
The strategy consists of making opponent "play" trumps as soon as possible, if they have any, making them want to take cards.
If you don't have many, then keep the trumps for the phase two, because then the winning of points is more likely.
"""

from api import State, util, Deck
import random
# from . import load
# from .kb import KB, Boolean, Integer


def get_card_value(tup):
    card = Deck.get_rank(tup[0])
    if card == 'A':
        value = 11
    elif card == '10':  # 10s
        value = 10
    elif card == 'K':   # Kings
        value = 4
    elif card == 'Q':   # Queens
        value = 3
    else:               # Jacks
        value = 2
    return value


def sort_cards(tup):
    tup.sort(key=lambda x: x[0])
    return tup


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # Get all legal moves
        moves = state.moves()
        print("Moves beginning:", moves)

        # Different "good" moves starting lists
        possible_moves = []
        moves_trump = []
        high_cards = []
        low_cards = []
        trumps_counter = 0
        good_moves_counter = 0
        safe_moves_counter = 0

        # GET ALL TRUMPS moves available
        # IF more than 3 trump cards in hand, try to win the trick by playing the trump (AGGRESSIVE TRUMP PLAY)
        # If low number of moves_trump, we keep the cards for phase 2 (PASSIVE PLAY)
        for index, move in enumerate(moves):
            if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                moves_trump.append(move)
                possible_moves.append(move)
                trumps_counter += 1

        num_of_moves = len(possible_moves)
        for i in range(num_of_moves):
            if get_card_value(possible_moves[i]) == 11:
                high_cards.append(possible_moves[i])
                good_moves_counter += 1
                print("High cards: ", high_cards)
            elif get_card_value(possible_moves[i]) == 10:
                high_cards.append(possible_moves[i])
                good_moves_counter += 1
            else:
                low_cards.append(possible_moves[i])
                safe_moves_counter += 1
                print("Low cards: ", low_cards)

        if trumps_counter > 2:
            sort_cards(moves_trump)
            chosen_move = moves_trump[trumps_counter - 1]
            return chosen_move
        elif good_moves_counter and safe_moves_counter == 1:
            sort_cards(low_cards)
            chosen_move = low_cards[safe_moves_counter - 1]
            return chosen_move

        print("Trump moves: ", trumps_counter)
        print("Good moves: ", good_moves_counter)
        print("Safe moves: ", safe_moves_counter)
        print("=====")
        print("High cards: ", high_cards)
        print("Low cards: ", low_cards)

        # IF THE OPPONENT PLAYED A CARD
        if state.get_opponents_played_card() is not None:
            # Different "good" moves starting lists
            possible_moves = []
            moves_same_suit = []
            moves_trump = []
            high_cards = []
            low_cards = []
            trumps_counter = 0
            good_moves_counter = 0
            safe_moves_counter = 0

            # Get all TRUMPS
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                    moves_trump.append(move)
                    possible_moves.append(move)
                    trumps_counter += 1

            # Get all moves of the same suit as the opponent's played card, trying to win the trick and some points
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) == Deck.get_suit(state.get_opponents_played_card()):
                    moves_same_suit.append(move)
                    if get_card_value(move) < get_card_value(state.get_opponents_played_card()):
                        low_cards.append(move)
                        safe_moves_counter += 1
                    else:
                        high_cards.append(move)
                        good_moves_counter += 1

            # Get other low valid cards
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) != Deck.get_suit(state.get_opponents_played_card()):
                    moves_same_suit.append(move)
                    possible_moves.append(move)
                    safe_moves_counter += 1

            if trumps_counter > 2:
                sort_cards(moves_trump)
                chosen_move = moves_trump[trumps_counter - 1]
                return chosen_move
            elif good_moves_counter == 1 and Deck.get_rank(state.get_opponents_played_card()) > Deck.get_rank(moves_same_suit[0]):
                chosen_move = moves_same_suit[0]
                return chosen_move
            else:
                if good_moves_counter > safe_moves_counter:
                    chosen_move = moves_same_suit[0]
                    return chosen_move
                else:
                    chosen_move = possible_moves

            print("Possible moves:", possible_moves)
            print("Trumps: ", moves_trump)
            print("Same suit", moves_same_suit)
