"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State, util, Deck
import random

# CONSTANTS
TRUMP_OPTIMAL_NUMBER = 2  # How many cards
HIGH_NUMBER = 2  # How many cards


def get_card_value(testing_card):
    if type(testing_card) is tuple:
        card = testing_card[0]
        if card is None:
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
    elif type(testing_card) is int:
        card = testing_card
        if card is None:  # Tuple (None, int) is possible jack trump exchange, meaning the card is Jack
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
        # type: (State) -> tuple[int, int]
        """

        """

        # All legal moves
        moves = state.moves()
        chosen_move = moves[0]

        # Get current phase
        current_phase = state.get_phase()

        # If playing FIRST
        if state.get_opponents_played_card() is None:
            moves_trump = []
            high_cards = []
            low_cards = []
            possible_trumps_ex = []
            possible_marriage = []
            trump_marriage = []

            for index, move in enumerate(moves):

                if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                    moves_trump.append(move)
                    if type(move[0]) is int and type(move[1]) is int:
                        trump_marriage.append(move)
                elif move[0] is None:
                    possible_trumps_ex.append(move)
                elif type(move[0]) is int and type(move[1]) is int:
                    possible_marriage.append(move)
                elif get_card_value(move[0]) == 11 or get_card_value(move[0]) == 10:
                    high_cards.append(move)
                else:
                    low_cards.append(move)

            if len(trump_marriage) > 0:
                chosen_move = trump_marriage[0]
                return chosen_move

            if len(possible_trumps_ex) > 0:
                chosen_move = possible_trumps_ex[0]
                return chosen_move

            if len(moves_trump) > TRUMP_OPTIMAL_NUMBER:
                sort_cards(moves_trump)
                chosen_move = moves_trump[0]
                return chosen_move

            if len(high_cards) > 0:
                chosen_move = high_cards[0]
                return chosen_move

            if len(low_cards) > 0:
                chosen_move = low_cards[0]
                return chosen_move

        if state.get_opponents_played_card() is not None:
            opponent_card_suit = Deck.get_suit(state.get_opponents_played_card())
            opponent_card_value = get_card_value(state.get_opponents_played_card())
            moves = state.moves()
            # Sorting lists
            moves_same_suit = []
            moves_trump = []
            high_cards = []
            low_cards = []
            high_same_suit = []
            low_same_suit = []

            for index, move in enumerate(moves):

                if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                    moves_trump.append(move)

            if len(moves_trump) > 0:
                chosen_move = moves_trump[0]
                return chosen_move

            for index, move in enumerate(moves):

                if move[0] is not None and Deck.get_suit(move[0]) == opponent_card_suit:
                    moves_same_suit.append(move)
                    if get_card_value(move[0]) > opponent_card_value:
                        high_same_suit.append(move)

            if len(high_same_suit) > 0:
                chosen_move = high_same_suit[0]
                return chosen_move

            # Get other moves of the different suit
            for index, move in enumerate(moves):
                if move[0] is not None and Deck.get_suit(move[0]) != opponent_card_suit:
                    if get_card_value(move[0]) >= opponent_card_value:
                        high_cards.append(move)
                    else:
                        low_cards.append(move)

            print("====================+ PLAYER 2 TURN +====================")
            print("Phase: ", state.get_phase())
            print("OPPONENT SUIT:", opponent_card_suit)
            print("OPPONENT VALUE: ", opponent_card_value)
            print("TRUMP moves:", moves_trump)
            print("H-I-G-H cards: ", high_cards)
            print("l_o_w cards: ", low_cards)
            print("High SAME SUIT:", high_same_suit)
            print("Low SAME SUIT:", low_same_suit)
            print("Moves SAME SUIT:", moves_same_suit)
            print("=====")
            print("TRUMP count:", len(moves_trump))
            print("High card count:", len(high_cards))
            print("Low card count:", len(low_cards))
            print("====================+ PRINT END +====================")

            if len(low_cards) > 0:
                chosen_move = low_cards[0]
                return chosen_move

        return chosen_move
