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


def is_empty(c):
    return c == "."

def is_free(c, keys):
    return is_empty(c) or is_key(c) or is_entrance(c) or c.lower() in keys

def at(maze, pos):
    x, y = pos
    return maze[x][y]

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


def distances_to_keys(maze, pos, keys, keys_to_find):
    # print("distances_to_keys:", keys_to_find)
    # Dijkstra algorithm
    distances = dict()
    heap = [(0, pos)]
    neighbours = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
    while heap:
        d, pos = heapq.heappop(heap)
        distances[pos] = d
        x, y = pos
        for dx, dy in neighbours:
            pos2 = x + dx, y + dy
            if pos2 not in distances and is_free(at(maze, pos2), keys):
                heapq.heappush(heap, (d+1, pos2))
    return {
        k: distances[k] for k in keys_to_find if k in distances and at(maze, k) not in keys
    }


def get_all_keys(maze):
    entrance = find_entrance(maze)
    keys_to_find = find_keys(maze)
    print(entrance, len(keys_to_find), keys_to_find)
    # Create heap with values
    #  (distance travelled, nb_keys_to_find, position, keys_found)
    #                                        ~~~~~~~~~~~~~~~~~~~~ <- enough to provide full state
    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ <- the smaller, the better
    heap = [(0, len(keys_to_find), entrance, [])]
    while heap:
        # For each state, check reachables keys and associated distances with Dijsktra
        # add new state to heap
        dist, nb_keys, pos, keys_found = heapq.heappop(heap)
        # print(dist, pos, nb_keys)
        assert len(keys_to_find) - len(keys_found) == nb_keys
        if len(keys_found) == len(keys_to_find):
            print(dist, keys_found)
            return dist
        for k, d in distances_to_keys(maze, pos, keys_found, keys_to_find).items():
            assert k not in keys_found
            # print("key:", k)
            heapq.heappush(heap, (dist + d, nb_keys - 1, k, keys_found + [at(maze, k)]))
    assert 0


def run_tests():
    maze = [
        "########################",
        "#f.D.E.e.C.b.A.@.a.B.c.#",
        "######################.#",
        "#d.....................#",
        "########################",
    ]
    assert get_all_keys(maze) == 86
    maze = [
        "########################",
        "#...............b.C.D.f#",
        "#.######################",
        "#.....@.a.B.c.d.A.e.F.g#",
        "########################",
    ]
    assert get_all_keys(maze) == 132
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
