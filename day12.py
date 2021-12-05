# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools
import operator

def get_pos_from_str(s):
    for c in "<>xyz= ":
        s = s.replace(c, "")
    return [int(v) for v in s.split(",")]

def get_pos_from_file(file_path="day12_input.txt"):
    with open(file_path) as f:
        return [get_pos_from_str(l.strip()) for l in f]


def vect_bin_op(op):
    return lambda v1, v2: [op(c1, c2) for c1, c2 in zip(v1, v2)]


def vect_op(op):
    return lambda v: [op(c) for c in v]


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


add = vect_bin_op(operator.add)
sub = vect_bin_op(operator.sub)
signv = vect_op(sign)
absv = vect_op(abs)


def simulation(positions, nb_steps):
    velocities = [[0] * len(positions[0]) for _ in range(len(positions))]
    for _ in range(nb_steps):
        # Apply gravity
        for i, (p, v) in enumerate(zip(positions, velocities)):
            for j, p2 in enumerate(positions):
                if i != j:
                    v = add(v, signv(sub(p2, p)))
            velocities[i] = v
        # Apply velocity
        for i, (p, v) in enumerate(zip(positions, velocities)):
            positions[i] = add(p, v)
    return sum(sum(absv(p)) * sum(absv(v)) for p, v in zip(positions, velocities))


def run_tests():
    pos = [
        "<x=-1, y=0, z=2>",
        "<x=2, y=-10, z=-7>",
        "<x=4, y=-8, z=8>",
        "<x=3, y=5, z=-1>",
    ]
    pos = [get_pos_from_str(p) for p in pos]
    assert simulation(pos, 10) == 179
    pos2 = [
        "<x=-8, y=-10, z=0>",
        "<x=5, y=5, z=10>",
        "<x=2, y=-7, z=3>",
        "<x=9, y=-8, z=-3>",
    ]
    pos2 = [get_pos_from_str(p) for p in pos2]
    assert simulation(pos2, 100) == 1940



def get_solutions():
    pos = get_pos_from_file()
    print(simulation(pos, 1000))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
