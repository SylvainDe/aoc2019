# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math


def get_orders_from_file(file_path="day22_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def new_deck(nb):
    return list(range(nb))


def deal_into_new_stack(deck):
    return list(reversed(deck))


def cut_n_cards(deck, n):
    left, right = deck[:n], deck[n:]
    return right + left


def deal_with_increment(deck, n):
    l = len(deck)
    assert math.gcd(l, n) == 1
    deck2 = [0] * l
    for i in range(l):
        deck2[(n * i) % l] = deck[i]
    return deck2


def apply_order(order, deck):
    if order == "deal into new stack":
        return deal_into_new_stack(deck)
    orders = [("cut ", cut_n_cards), ("deal with increment ", deal_with_increment)]
    for prefix, func in orders:
        if order.startswith(prefix):
            param = int(order[len(prefix) :])
            return func(deck, param)
    assert False


def apply_orders(nb, orders):
    deck = new_deck(nb)
    for order in orders:
        deck = apply_order(order, deck)
    return deck


def run_tests():
    deck = new_deck(10)
    assert deck == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert deal_into_new_stack(deck) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert cut_n_cards(deck, 3) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert cut_n_cards(deck, -4) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    assert deal_with_increment(deck, 3) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
    assert deck == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    orders = [
        "deal with increment 7",
        "deal into new stack",
        "deal into new stack",
    ]
    assert apply_orders(10, orders) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
    orders = [
        "cut 6",
        "deal with increment 7",
        "deal into new stack",
    ]
    assert apply_orders(10, orders) == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
    orders = [
        "deal with increment 7",
        "deal with increment 9",
        "cut -2",
    ]
    assert apply_orders(10, orders) == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
    orders = [
        "deal into new stack",
        "cut -2",
        "deal with increment 7",
        "cut 8",
        "cut -4",
        "deal with increment 7",
        "cut 3",
        "deal with increment 9",
        "deal with increment 3",
        "cut -1",
    ]
    assert apply_orders(10, orders) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]


def get_solutions():
    orders = get_orders_from_file()
    print(apply_orders(10007, orders).index(2019))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
