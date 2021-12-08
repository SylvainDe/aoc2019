# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import string
import heapq

def get_maze_from_file(file_path="day18_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]

def is_entrance(c):
    return c == "@"


def is_key(c):
    return c in string.ascii_lowercase


def is_empty(c, keys):
    return c == "." or c.lower() in keys


def find(maze, func):
    for i, l in enumerate(maze):
        for j, c in enumerate(l):
            if func(c):
                yield i, j

def find_entrance(maze):
    entrances = list(find(maze, is_entrance))
    assert len(entrances) == 1
    return entrances[0]


def find_keys(maze):
    return list(find(maze, is_key))


def distances_to_keys(maze, position, keys):
    # Dijkstra algorithm
    raise NotImplementedError


def get_all_keys(maze):
    entrance = find_entrance(maze)
    print(entrance)
    keys_to_find = find_keys(maze)
    # Create heap with values
    #  (distance travelled, -nb_keys_to_find, position, keys_found)
    #                                         ~~~~~~~~~~~~~~~~~~~~ <- enough to provide full state
    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ <- the smaller, the better
    heap = [(0, 0, entrance, [])]
    while heap:
        # For each state, check reachables keys and associated distances with Dijsktra
        # add new state to heap
        dist, nb_keys, pos, keys_found = heapq.heappop(heap)
        assert len(keys_found) == -nb_keys
        if len(keys_found) == len(keys_to_find):
            print(dist, keys_found)
            return dist
        for k, d in distances_to_keys(maze, pos, keys_found):
            assert k not in keys_found
            heappush(heap, (dist + d, nb_keys - 1, k, keys_found + [k]))


def run_tests():
    maze = [
        "########################",
        "#f.D.E.e.C.b.A.@.a.B.c.#",
        "######################.#",
        "#d.....................#",
        "########################",
    ]
    print(get_all_keys(maze)) # 86
    maze = [
        "########################",
        "#...............b.C.D.f#",
        "#.######################",
        "#.....@.a.B.c.d.A.e.F.g#",
        "########################",
    ]
    print(get_all_keys(maze)) # 132
    maze = [
        "#################",
        "#i.G..c...e..H.p#",
        "########.########",
        "#j.A..b...f..D.o#",
        "########@########",
        "#k.E..a...g..B.n#",
        "########.########",
        "#l.F..d...h..C.m#",
        "#################",
    ]
    print(get_all_keys(maze)) # 136
    maze = [
        "########################",
        "#@..............ac.GI.b#",
        "###d#e#f################",
        "###A#B#C################",
        "###g#h#i################",
        "########################",
    ]
    print(get_all_keys(maze)) # 81


def get_solutions():
    maze = get_maze_from_file()
    # print(get_all_keys(maze))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
