# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_intcode_from_string(s):
    return [int(v) for v in s.split(",")]


def get_intcode_from_file(file_path):
    with open(file_path) as f:
        for l in f:
            return get_intcode_from_string(l)


def run(intcode):
    intcode = list(intcode)
    pos = 0
    while True:
        op = intcode[pos]
        if op == 99:
            return intcode
        elif op == 1:
            intcode[intcode[pos + 3]] = (
                intcode[intcode[pos + 1]] + intcode[intcode[pos + 2]]
            )
        elif op == 2:
            intcode[intcode[pos + 3]] = (
                intcode[intcode[pos + 1]] * intcode[intcode[pos + 2]]
            )
        pos += 4


def run_verb_noun(intcode, noun, verb):
    intcode = list(intcode)
    intcode[1] = noun
    intcode[2] = verb
    return run(intcode)[0]


def run_tests_day2():
    intcode = get_intcode_from_string("1,9,10,3,2,3,11,0,99,30,40,50")
    assert run(intcode) == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    assert run_verb_noun(intcode, 9, 10) == 3500
    intcode = get_intcode_from_string("1,0,0,0,99")
    assert run(intcode) == [2, 0, 0, 0, 99]
    assert run_verb_noun(intcode, 0, 0) == 2
    intcode = get_intcode_from_string("2,3,0,3,99")
    assert run(intcode) == [2, 3, 0, 6, 99]
    intcode = get_intcode_from_string("2,4,4,5,99,0")
    assert run(intcode) == [2, 4, 4, 5, 99, 9801]
    intcode = get_intcode_from_string("1,1,1,4,99,5,6,0,99")
    assert run(intcode) == [30, 1, 1, 4, 2, 5, 6, 0, 99]


def run_tests_day5():
    pass


def run_tests():
    run_tests_day2()
    run_tests_day5()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    end = datetime.datetime.now()
    print(end - begin)
