# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math

def get_grid_from_file(file_path="day10_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def get_asteroids(grid):
    for i, line in enumerate(grid):
        for j, val in enumerate(line):
            if val == "#":
                yield i, j


def integer_path(a, b):
    (xa, ya), (xb, yb) = a, b
    dx, dy = xa - xb, ya - yb
    if (dx, dy) == (0, 0):
        return
    elif dx == 0:
        steps = abs(dy)
    elif dy == 0:
        steps = abs(dx)
    else:
        steps = math.gcd(dx, dy)
    assert steps
    udx, udy = dx // steps, dy // steps
    assert dx % steps == 0
    assert dy % steps == 0
    for s in range(1, steps):
        x, y = xa - s * udx, ya - s * udy
        assert (x, y) != a
        assert (x, y) != b
        yield x, y


def visible(a, b, asteroids):
    return not any(p in asteroids for p in integer_path(a, b))


def get_best_asteroid_count(grid):
    asteroids = set(get_asteroids(grid))
    return max(sum(a != b and visible(a, b, asteroids) for b in asteroids)
                for a in asteroids)

def run_tests():
    grid = [
        ".#..#",
        ".....",
        "#####",
        "....#",
        "...##",
    ]
    assert get_best_asteroid_count(grid) == 8
    grid = [
        ".#..##.###...#######",
        "##.############..##.",
        ".#.######.########.#",
        ".###.#######.####.#.",
        "#####.##.#.##.###.##",
        "..#####..#.#########",
        "####################",
        "#.####....###.#.#.##",
        "##.#################",
        "#####.##.###..####..",
        "..######..##.#######",
        "####.##.####...##..#",
        ".#####..#.######.###",
        "##...#.##########...",
        "#.##########.#######",
        ".####.#.###.###.#.##",
        "....##.##.###..#####",
        ".#.#.###########.###",
        "#.#.#.#####.####.###",
        "###.##.####.##.#..##",
    ]
    assert get_best_asteroid_count(grid) == 210


def get_solutions():
    grid = get_grid_from_file()
    print(get_best_asteroid_count(grid))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
