from api import Deck


def sort_cards(tup):
    for i in range(len(tup)):
        if tup[i][0] is None:
            tup = tup
            break
        else:
            tup.sort(key=lambda x: x[0])
    return tup


tuple1 = [(5, 0), (2, 0), (None, 0), (0, None)]
print(sort_cards(tuple1))

