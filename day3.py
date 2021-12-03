# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_wires_from_file(file_path="day3_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


directions = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}

def get_wire_path(wire):
    x, y = 0, 0
    for instruction in wire.split(","):
        (dx, dy), value = directions[instruction[0]], int(instruction[1:])
        for i in range(value):
            x += dx
            y += dy
            yield x, y


def get_cross_distance(wires):
    crossings = set.intersection(*(set(get_wire_path(w)) for w in wires))
    distances = [abs(x) + abs(y) for x, y in crossings]
    return min(distances)


def run_tests():
    wires = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
    assert get_cross_distance(wires) == 6
    wires = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
    assert get_cross_distance(wires) == 159


def get_solutions():
    wires = get_wires_from_file()
    print(get_cross_distance(wires))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
