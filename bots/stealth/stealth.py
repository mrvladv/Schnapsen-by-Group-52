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

# CONSTANTS
OPTIMAL_NUMBER = 1
HIGH_NUMBER = 1


def get_card_value(tup):
    card = Deck.get_rank(tup)[0]
    if card == 'A':
        value = 11
    elif card == '10':  # 10s
        value = 10
    elif card == 'K':   # Kings
        value = 4
    elif card == 'Q':   # Queens
        value = 3
    elif card is None:
        value = 2
    else:               # Jacks
        value = 2
    return value


def get_opponent_value(number):
    card = Deck.get_rank(number)
    if card == 'A':
        value = 11
    elif card == '10':  # 10s
        value = 10
    elif card == 'K':   # Kings
        value = 4
    elif card == 'Q':   # Queens
        value = 3
    elif card is None:
        value = 2
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

        # Get at which phase we are playing
        current_phase = state.get_phase()

        # Different "good" moves starting lists
        possible_moves = []
        moves_same_suit = []
        moves_trump = []
        high_cards = []
        low_cards = []
        possible_trumps_ex = []
        trumps_counter = 0
        good_moves_counter = 0
        safe_moves_counter = 0

        # GET ALL TRUMPS moves available
        # IF more than OPTIMAL NUMBER of trump cards in hand, try to win the trick by playing the trump (AGGRESSIVE TRUMP PLAY)
        # If low number of moves_trump, we keep the cards for phase 2 (PASSIVE PLAY)
        for index, move in enumerate(moves):
            if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                moves_trump.append(move)
                possible_moves.append(move)
                trumps_counter += 1
            else:
                low_cards.append(move)
                possible_moves.append(move)
                safe_moves_counter += 1

        num_of_moves = len(possible_moves)
        print("Possible moves:", possible_moves)
        for i in range(num_of_moves):
            if get_opponent_value(possible_moves[i][0]) == 11:
                high_cards.append(possible_moves[i])
                good_moves_counter += 1
            elif get_opponent_value(possible_moves[i][0]) == 10:
                high_cards.append(possible_moves[i])
                good_moves_counter += 1
            elif get_opponent_value(possible_moves[i][0]) is None:
                possible_trumps_ex.append(possible_moves[i])

        print("Trump moves:", moves_trump)
        print("Possible moves:", possible_moves)
        print("High cards: ", high_cards)
        print("Low cards: ", low_cards)
        print("=====")
        print("Trump counter:", trumps_counter)
        print("Good moves counter:", good_moves_counter)
        print("Safe moves counter:", safe_moves_counter)

        if trumps_counter > OPTIMAL_NUMBER and current_phase == 1:
            sort_cards(moves_trump)
            chosen_move = moves_trump[trumps_counter - 1]
            return chosen_move
        elif good_moves_counter and safe_moves_counter > 1:
            sort_cards(low_cards)
            chosen_move = low_cards[safe_moves_counter - 1]
            return chosen_move

        if trumps_counter > 0 and current_phase == 2:
            sort_cards(moves_trump)
            chosen_move = moves_trump[trumps_counter - 1]
            return chosen_move
        elif current_phase == 2 and high_cards > 0:
            sort_cards(high_cards)
            chosen_move = high_cards[0]
            return chosen_move
        elif current_phase == 2 and low_cards > 0:
            sort_cards(low_cards)
            chosen_move = low_cards[0]
            return chosen_move

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
                    if get_card_value(move[0]) < get_card_value(state.get_opponents_played_card()):
                        low_cards.append(move)
                        safe_moves_counter += 1
                    else:
                        high_cards.append(move)
                        good_moves_counter += 1

            # Get other low valid cards
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) != Deck.get_suit(state.get_opponents_played_card()):
                    low_cards.append(move)
                    safe_moves_counter += 1

            if trumps_counter > OPTIMAL_NUMBER:
                sort_cards(moves_trump)
                chosen_move = moves_trump[trumps_counter - 1]
                return chosen_move
            elif good_moves_counter == 1 and get_opponent_value(state.get_opponents_played_card()) < get_card_value(moves_same_suit[0]):
                chosen_move = moves_same_suit[0]
                return chosen_move
            elif len(low_cards) > HIGH_NUMBER:
                chosen_move = random.choice(low_cards)
                return chosen_move
            else:
                if good_moves_counter > 1:
                    sort_cards(high_cards)
                    chosen_move = high_cards[0]
                    return chosen_move
                else:
                    sort_cards(low_cards)
                    chosen_move = low_cards[safe_moves_counter - 1]
                    return chosen_move
