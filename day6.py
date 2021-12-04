# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_orbits_from_file(file_path="day6_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def build_graph(orbits):
    graph = dict()
    for orbit in orbits:
       left, right = orbit.split(")")
       graph[right] = left
    return graph


def count_distance(graph):
   d = 0
   for node in graph:
       while node != "COM":
           node = graph[node]
           d+=1
   return d


def run_tests():
    orbits = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
    ]
    graph = build_graph(orbits)
    assert count_distance(graph) == 42


def get_solutions():
    orbits = get_orbits_from_file()
    graph = build_graph(orbits)
    print(count_distance(graph))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
