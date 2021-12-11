# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math
import functools
import collections


def get_orders_from_file(file_path="day22_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


# Basic operations on full deck
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


# Basic operations on single card
def single_deal_into_new_stack(nb_cards, position):
    return nb_cards - position - 1


def single_cut_n_cards(nb_cards, n, position):
    return (position - n) % nb_cards


def single_deal_with_increment(nb_cards, n, position):
    return (n * position) % nb_cards


# Reverse operation on single card
reverse_deal_into_new_stack = single_deal_into_new_stack


def reverse_cut_n_cards(nb_cards, n, position):
    return single_cut_n_cards(nb_cards, -n, position)


def reverse_deal_with_increment(nb_cards, n, position):
    assert math.gcd(nb_cards, n) == 1
    # Card i ends up at position j such that: j = (n*i) % nb_cards
    # Finding i from j corresponds to finding the inverse of n modulo nb_cards
    n_inv = modinv(n, nb_cards)
    return position * n_inv % nb_cards


def xgcd(a, b):
    """Computes the extended gcd."""
    # http://anh.cs.luc.edu/331/notes/xgcd.pdf
    prevx, x = 1, 0
    prevy, y = 0, 1
    while b:
        q = a // b
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, a % b
    return a, prevx, prevy


@functools.lru_cache()
def modinv(a, m):
    """Computes the Modular multiplicative inverse."""
    g, x, y = xgcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    else:
        return x % m


# Orders
Operation = collections.namedtuple("Operation", ["deck", "single", "reverse"])
orders = [
    (
        "deal into new stack",
        Operation(
            deal_into_new_stack, single_deal_into_new_stack, reverse_deal_into_new_stack
        ),
    ),
    ("cut ", Operation(cut_n_cards, single_cut_n_cards, reverse_cut_n_cards)),
    (
        "deal with increment ",
        Operation(
            deal_with_increment, single_deal_with_increment, reverse_deal_with_increment
        ),
    ),
]


def get_order_and_remaining(order):
    for prefix, op in orders:
        if order.startswith(prefix):
            return op, order[len(prefix) :]
    assert False


def apply_order(order, deck):
    op, rem = get_order_and_remaining(order)
    if rem:
        return op.deck(deck, int(rem))
    else:
        return op.deck(deck)


def apply_orders(nb, orders):
    deck = new_deck(nb)
    for order in orders:
        deck = apply_order(order, deck)
    return deck


# Orders on single cards
def apply_single_order(order, nb_cards, position):
    op, rem = get_order_and_remaining(order)
    if rem:
        return op.single(nb_cards, int(rem), position)
    else:
        return op.single(nb_cards, position)


def apply_single_orders(orders, nb_cards, position):
    for order in orders:
        position = apply_single_order(order, nb_cards, position)
    return position


# Reverse orders on single cards
def apply_reverse_order(order, nb_cards, position):
    op, rem = get_order_and_remaining(order)
    if rem:
        return op.reverse(nb_cards, int(rem), position)
    else:
        return op.reverse(nb_cards, position)


def apply_reverse_orders(orders, nb_cards, position):
    for order in reversed(orders):
        position = apply_reverse_order(order, nb_cards, position)
    return position


def test_minimal_operations():
    deck = new_deck(10)
    assert deck == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert deal_into_new_stack(deck) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert cut_n_cards(deck, 3) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert cut_n_cards(deck, -4) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    assert deal_with_increment(deck, 3) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
    assert deck == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_single_card_operations():
    for nb_cards in [10, 20]:
        deck = deal_into_new_stack(new_deck(nb_cards))
        for pos, card in enumerate(deck):
            assert single_deal_into_new_stack(nb_cards, card) == pos
            assert reverse_deal_into_new_stack(nb_cards, pos) == card
        for cut_arg in [3, -4]:
            deck = cut_n_cards(new_deck(nb_cards), cut_arg)
            for pos, card in enumerate(deck):
                assert single_cut_n_cards(nb_cards, cut_arg, card) == pos
                assert reverse_cut_n_cards(nb_cards, cut_arg, pos) == card
        for incr_arg in [3]:
            deck = deal_with_increment(new_deck(nb_cards), incr_arg)
            for pos, card in enumerate(deck):
                assert single_deal_with_increment(nb_cards, incr_arg, card) == pos
                assert reverse_deal_with_increment(nb_cards, incr_arg, pos) == card


def test_single_card_orders(nb_cards, orders):
    result = apply_orders(nb_cards, orders)
    for pos, card in enumerate(result):
        assert apply_single_orders(orders, nb_cards, card) == pos
        assert apply_reverse_orders(orders, nb_cards, pos) == card


def test_orders():
    nb_cards = 10
    orders = [
        "deal with increment 7",
        "deal into new stack",
        "deal into new stack",
    ]
    assert apply_orders(nb_cards, orders) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
    test_single_card_orders(nb_cards, orders)
    orders = [
        "cut 6",
        "deal with increment 7",
        "deal into new stack",
    ]
    assert apply_orders(nb_cards, orders) == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
    test_single_card_orders(nb_cards, orders)
    orders = [
        "deal with increment 7",
        "deal with increment 9",
        "cut -2",
    ]
    assert apply_orders(nb_cards, orders) == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
    test_single_card_orders(nb_cards, orders)
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
    assert apply_orders(nb_cards, orders) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
    test_single_card_orders(nb_cards, orders)


def run_tests():
    test_minimal_operations()
    test_single_card_operations()
    test_orders()


def part1(orders):
    nb_cards = 10007
    card_number = 2019
    return apply_single_orders(orders, nb_cards, card_number)


def part2(orders):
    positions_seen = dict()
    nb_cards = 119315717514047
    final_position = 2020
    # Perform operations in reverse order
    # Hope to see same positions twice and infer a frequence
    for i in range(101741582076661):
        if final_position in positions_seen:
            break
        positions_seen[final_position] = i
        final_position = apply_reverse_orders(orders, nb_cards, final_position)


def get_solutions():
    orders = get_orders_from_file()
    print(part1(orders))
    # print(part2(orders)) - not efficient enough yet >_<


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
