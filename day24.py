# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections

size = 5


def get_bugs_from_lines(lines):
    for i, line in enumerate(lines):
        for j, val in enumerate(line):
            if val == "#":
                yield i, j


def get_bugs_from_file(file_path="day24_input.txt"):
    with open(file_path) as f:
        return set(get_bugs_from_lines(f))


def show_bugs(bugs):
    i_vals = [i for i, j in bugs]
    j_vals = [j for i, j in bugs]
    i_range = list(range(min(i_vals), max(i_vals) + 1))
    j_range = list(range(min(j_vals), max(j_vals) + 1))
    for i in i_range:
        print("".join("#" if (i, j) in bugs else "." for j in j_range))


def neighbours(pos):
    i, j = pos
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        i2, j2 = i + di, j + dj
        if 0 <= i2 < size and 0 <= j2 < size:
            yield i + di, j + dj


def next_gen(bugs):
    neigh_count = collections.Counter(n for b in bugs for n in neighbours(b))
    next_bugs = set()
    for b, count in neigh_count.items():
        if count == 1 and b in bugs:
            next_bugs.add(b)
        elif count in (1, 2) and b not in bugs:
            next_bugs.add(b)
    return next_bugs


def first_repeated_layout(bugs):
    seen = set()
    bugs = tuple(bugs)
    while bugs not in seen:
        seen.add(bugs)
        bugs = tuple(next_gen(bugs))
    return sum(2 ** (i * size + j) for i, j in bugs)


def run_tests():
    bugs = [
        "....#",
        "#..#.",
        "#..##",
        "..#..",
        "#....",
    ]
    bugs = set(get_bugs_from_lines(bugs))
    assert first_repeated_layout(bugs) == 2129920


def get_solutions():
    bugs = get_bugs_from_file()
    print(first_repeated_layout(bugs))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
