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
TRUMP_OPTIMAL_NUMBER = 2            # How many cards
HIGH_NUMBER = 2             # How many cards


def get_card_value(testing_card):
    if type(testing_card) is tuple:
        card = testing_card[0]
        if card is None:
            value = 2
        elif card % 5 == 0:
            value = 11
        elif card % 5 == 1:  # 10s
            value = 10
        elif card % 5 == 2:   # Kings
            value = 4
        elif card % 5 == 3:   # Queens
            value = 3
        else:               # Jacks
            value = 2
        return value
    elif type(testing_card) is int:
        card = testing_card
        if card is None:      # Tuple (None, int) is possible jack trump exchange, meaning the card is Jack
            value = 2
        elif card % 5 == 0:
            value = 11
        elif card % 5 == 1:  # 10s
            value = 10
        elif card % 5 == 2:  # Kings
            value = 4
        elif card % 5 == 3:  # Queens
            value = 3
        else:  # Jacks
            value = 2
        return value
    else:
        value = 2
        return value


def sort_cards(tup):
    for i in range(len(tup)):
        if tup[i][0] is None:
            tup = tup
            break
        else:
            tup.sort(key=lambda x: x[0])
    return tup


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # Get all legal moves
        moves = state.moves()
        print("ALL LEGAL MOVES:", moves)

        # Get at which phase we are playing
        current_phase = state.get_phase()

        # Different "good" moves starting lists
        moves_trump = []
        high_cards = []
        low_cards = []
        possible_trumps_ex = []
        possible_marriage = []

        # IF BOT/PLAYER plays first
        if state.get_opponents_played_card() is None:
            # SORTING
            # GET ALL TRUMPS moves available
            # IF more than OPTIMAL NUMBER of trump cards in hand, try to win the trick by playing the trump (AGGRESSIVE TRUMP PLAY)
            # If low number of moves_trump, we keep the cards for phase 2 (PASSIVE PLAY)
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                    moves_trump.append(move)
                elif move[0] is None:
                    possible_trumps_ex.append(move)
                elif move[0] is int and move[1] is int:
                    possible_marriage.append(move)
                elif get_card_value(move[0]) == 11 or get_card_value(move[0]) == 10:
                    high_cards.append(move)
                else:
                    low_cards.append(move)

            # print("====================+ PLAYER 1 TURN +====================")
            # print("Phase: ", state.get_phase())
            # print("TRUMP moves:", moves_trump)
            # print("H-I-G-H cards: ", high_cards)
            # print("l_o_w cards: ", low_cards)
            # print("Possible trump exchange: ", possible_trumps_ex)
            # print("=====")
            # print("TRUMP count:", len(moves_trump))
            # print("High card count:", len(high_cards))
            # print("Low card count:", len(low_cards))
            # print("Possible marriage:", possible_marriage)
            # print("====================+ PRINT END +====================")

            if current_phase == 1:
                if len(moves_trump) >= TRUMP_OPTIMAL_NUMBER:
                    sort_cards(moves_trump)
                    chosen_move = moves_trump[0]
                    return chosen_move
                elif len(moves_trump) == 0 and len(high_cards) > len(low_cards):
                    sort_cards(high_cards)
                    chosen_move = high_cards[0]
                    return chosen_move
                elif len(high_cards) < len(low_cards):
                    sort_cards(low_cards)
                    chosen_move = low_cards[0]
                    return chosen_move
                elif len(high_cards) == len(low_cards):
                    sort_cards(high_cards)
                    chosen_move = high_cards[0]
                    return chosen_move

            if current_phase == 2:                      # ALWAYS TRY TO PLAY TRUMPS IN THE PHASE 2
                if len(moves_trump) > 0:
                    sort_cards(moves_trump)
                    chosen_move = moves_trump[0]
                    return chosen_move
                elif len(moves_trump) == 0 and len(high_cards) > len(low_cards):
                    sort_cards(high_cards)
                    chosen_move = high_cards[0]
                    return chosen_move
                elif len(high_cards) < len(low_cards):
                    sort_cards(low_cards)
                    chosen_move = low_cards[0]
                    return chosen_move
                elif len(high_cards) == len(low_cards):
                    sort_cards(high_cards)
                    chosen_move = high_cards[0]
                    return chosen_move
        # IF THE OPPONENT PLAYED A CARD
        elif state.get_opponents_played_card() is not None:
            opponent_card_suit = Deck.get_suit(state.get_opponents_played_card())
            opponent_card_value = get_card_value(state.get_opponents_played_card())
            # Different "good" moves starting lists, used later for sorting
            moves_same_suit = []
            moves_trump = []
            high_cards = []
            low_cards = []
            high_same_suit = []
            low_same_suit = []
            possible_trumps_ex = []

            # SORTING
            # Get all TRUMPS
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                    moves_trump.append(move)
                # Get all moves of the same suit as the opponent's played card
                elif move[0] is not None and Deck.get_suit(move[0]) != state.get_trump_suit():
                    if move[0] is not None and Deck.get_suit(move[0]) == opponent_card_suit:
                        moves_same_suit.append(move)
                        if get_card_value(move[0]) < opponent_card_value:
                            low_same_suit.append(move)
                            # low_cards.append(move)
                        elif get_card_value(move[0]) > opponent_card_value:
                            high_same_suit.append(move)
                            # high_cards.append(move)
                elif move[0] is None:
                    possible_trumps_ex.append(move)

            # Get other moves of the different suit
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) != opponent_card_suit:
                    if get_card_value(move[0]) >= opponent_card_value:
                        high_cards.append(move)
                    else:
                        low_cards.append(move)
                elif move[0] is None:
                    possible_trumps_ex.append(move)

            # print("====================+ PLAYER 2 TURN +====================")
            # print("Phase: ", state.get_phase())
            # print("OPPONENT SUIT:", opponent_card_suit)
            # print("OPPONENT VALUE: ", opponent_card_value)
            # print("TRUMP moves:", moves_trump)
            # print("H-I-G-H cards: ", high_cards)
            # print("l_o_w cards: ", low_cards)
            # print("High SAME SUIT:", high_same_suit)
            # print("Low SAME SUIT:", low_same_suit)
            # print("Possible trump exchange: ", possible_trumps_ex)
            # print("Moves SAME SUIT:", moves_same_suit)
            # print("=====")
            # print("TRUMP count:", len(moves_trump))
            # print("High card count:", len(high_cards))
            # print("Low card count:", len(low_cards))
            # print("====================+ PRINT END +====================")

            if current_phase == 1:
                if len(moves_trump) >= TRUMP_OPTIMAL_NUMBER:
                    sort_cards(moves_trump)
                    chosen_move = moves_trump[len(moves_trump) - 1]               # Play weakest trump
                    return chosen_move
                elif len(high_same_suit) > 0:
                    sort_cards(high_same_suit)
                    if opponent_card_value < get_card_value(high_same_suit[0]):
                        chosen_move = high_same_suit[0]
                        return chosen_move
                elif len(high_cards) > len(low_cards):
                    sort_cards(high_cards)
                    if opponent_card_value >= get_card_value(high_cards[0]):
                        chosen_move = high_cards[-1]            # Play lowest high card
                        return chosen_move
                    else:
                        chosen_move = high_cards[0]            # Play first higest
                        return chosen_move
                elif len(high_cards) == len(low_cards):
                    if opponent_card_value >= get_card_value(high_cards[0]):
                        sort_cards(low_cards)
                        chosen_move = low_cards[0]
                        return chosen_move
                    else:
                        sort_cards(high_cards)
                        chosen_move = high_cards[-1]        # Play lowest high card
                        return chosen_move
                else:
                    sort_cards(low_cards)
                    chosen_move = low_cards[0]
                    return chosen_move

            if current_phase == 2:
                for index, move in enumerate(moves):
                    if move[0] is not None and Deck.get_suit(move[0]) == opponent_card_suit:
                        moves_same_suit.append(move)
                        if get_card_value(move[0]) < opponent_card_value:
                            low_same_suit.append(move)
                        else:
                            high_same_suit.append(move)

                if len(high_same_suit) > 0:            # ALWAYS TRY first to play highest of the same suit
                    if opponent_card_value < get_card_value(high_same_suit[0]):
                        chosen_move = high_same_suit[0]
                        return chosen_move
                    else:
                        chosen_move = moves_same_suit[0]
                        return chosen_move
                elif len(low_same_suit) > 0:
                    if len(low_same_suit) != 0:
                        sort_cards(low_same_suit)
                        chosen_move = low_same_suit[0]
                        return chosen_move
                    elif len(low_cards) != 0:
                        chosen_move = moves[0]
                        return chosen_move
                elif len(high_same_suit) != 0 and len(low_same_suit) == len(high_same_suit):
                    sort_cards(low_same_suit)
                    chosen_move = moves[0]
                    return chosen_move

                if len(moves_trump) > 0:              # ALWAYS TRY TO PLAY TRUMPS IN THE PHASE 2, after the same suit
                    sort_cards(moves_trump)
                    chosen_move = moves_trump[0]
                    return chosen_move
                elif len(high_cards) > len(low_cards):
                    sort_cards(high_cards)
                    chosen_move = high_cards[0]
                    return chosen_move
                elif len(high_cards) < len(low_cards):
                    sort_cards(low_cards)
                    chosen_move = low_cards[0]
                    return chosen_move
                elif len(high_cards) == len(low_cards):
                    if len(low_same_suit) != 0:
                        sort_cards(low_same_suit)
                        chosen_move = low_same_suit[0]
                        return chosen_move
                    elif len(low_cards) != 0:
                        sort_cards(low_cards)
                        chosen_move = low_cards[0]
                        return chosen_move
                elif len(low_same_suit) != 0:
                        sort_cards(low_same_suit)
                        chosen_move = low_same_suit[0]
                        return chosen_move
                elif len(low_cards) != 0:
                    sort_cards(low_cards)
                    chosen_move = low_cards[0]
                    return chosen_move
                else:
                    chosen_move = move[0]
                    return chosen_move
