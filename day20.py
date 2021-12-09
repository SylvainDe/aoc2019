# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import string
import collections

def get_grid_from_file(file_path="day20_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def points_iter(grid):
    for x, line in enumerate(grid):
       for y, val in enumerate(line):
           yield (x, y), val


def neighbours(pos):
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        yield x + dx, y + dy

def solve_maze(grid):
    # Extract relevant info from maze
    passages = set()
    letters = dict()
    for pos, val in points_iter(grid):
        if val == ".":
            passages.add(pos)
        elif val in string.ascii_uppercase:
            letters[pos] = val
        elif val not in " #":
            assert False
    # Extract positions for labels
    labels = dict()
    for pos, val in letters.items():
        neigh = list(neighbours(pos))
        passage = [n for n in neigh if n in passages]
        letter = [letters[n] for n in neigh if n in letters]
        if len(letter) == 1 and len(passage) == 1:
            label = "".join(sorted(val + letter[0]))
            pos2 = passage[0]
            labels.setdefault(label, []).append(pos2)
    print(labels)
    entrance = labels.pop("AA")
    exit = labels.pop("ZZ")
    assert len(entrance) == 1
    assert len(exit) == 1
    entrance = entrance[0]
    exit = exit[0]
    # Build graph: first passage then add warp
    graph = {
        pos: set(pos2 for pos2 in neighbours(pos) if pos2 in passages)
        for pos in passages
    }
    for positions in labels.values():
        assert len(positions) == 2
        pos1, pos2 = positions
        graph[pos1].add(pos2)
        graph[pos2].add(pos1)
    # Dijkstra
    distances = dict()
    queue = collections.deque([(0, entrance)])
    while queue:
        d, pos = queue.popleft()
        if pos in distances:
            assert d >= distances[pos]
            continue
        distances[pos] = d
        if pos == exit:
            break
        for pos2 in graph[pos]:
            if pos2 not in distances:
                queue.append(((d+1), pos2))
    return distances[exit]



def run_tests():
    grid = [
        "         A           ",
        "         A           ",
        "  #######.#########  ",
        "  #######.........#  ",
        "  #######.#######.#  ",
        "  #######.#######.#  ",
        "  #######.#######.#  ",
        "  #####  B    ###.#  ",
        "BC...##  C    ###.#  ",
        "  ##.##       ###.#  ",
        "  ##...DE  F  ###.#  ",
        "  #####    G  ###.#  ",
        "  #########.#####.#  ",
        "DE..#######...###.#  ",
        "  #.#########.###.#  ",
        "FG..#########.....#  ",
        "  ###########.#####  ",
        "             Z       ",
        "             Z       ",
    ]
    assert solve_maze(grid) == 23
    grid = [
        "                   A               ",
        "                   A               ",
        "  #################.#############  ",
        "  #.#...#...................#.#.#  ",
        "  #.#.#.###.###.###.#########.#.#  ",
        "  #.#.#.......#...#.....#.#.#...#  ",
        "  #.#########.###.#####.#.#.###.#  ",
        "  #.............#.#.....#.......#  ",
        "  ###.###########.###.#####.#.#.#  ",
        "  #.....#        A   C    #.#.#.#  ",
        "  #######        S   P    #####.#  ",
        "  #.#...#                 #......VT",
        "  #.#.#.#                 #.#####  ",
        "  #...#.#               YN....#.#  ",
        "  #.###.#                 #####.#  ",
        "DI....#.#                 #.....#  ",
        "  #####.#                 #.###.#  ",
        "ZZ......#               QG....#..AS",
        "  ###.###                 #######  ",
        "JO..#.#.#                 #.....#  ",
        "  #.#.#.#                 ###.#.#  ",
        "  #...#..DI             BU....#..LF",
        "  #####.#                 #.#####  ",
        "YN......#               VT..#....QG",
        "  #.###.#                 #.###.#  ",
        "  #.#...#                 #.....#  ",
        "  ###.###    J L     J    #.#.###  ",
        "  #.....#    O F     P    #.#...#  ",
        "  #.###.#####.#.#####.#####.###.#  ",
        "  #...#.#.#...#.....#.....#.#...#  ",
        "  #.#####.###.###.#.#.#########.#  ",
        "  #...#.#.....#...#.#.#.#.....#.#  ",
        "  #.###.#####.###.###.#.#.#######  ",
        "  #.#.........#...#.............#  ",
        "  #########.###.###.#############  ",
        "           B   J   C               ",
        "           U   P   P               ",
    ]
    assert solve_maze(grid) == 58


def get_solutions():
    grid = get_grid_from_file()
    # print(solve_maze(grid))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
