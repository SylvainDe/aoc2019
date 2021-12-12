# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_intcode_from_string(s):
    return [int(v) for v in s.split(",")]


def get_intcode_from_file(file_path):
    with open(file_path) as f:
        for l in f:
            return get_intcode_from_string(l)


def parse_op_code(op):
    """Return op, mode1, mode2, mode3."""
    p100, de = divmod(op, 100)
    p1000, c = divmod(p100, 10)
    p10000, b = divmod(p1000, 10)
    p100000, a = divmod(p10000, 10)
    assert op == a * 10000 + b * 1000 + c * 100 + de
    return de, c, b, a


def get_value(intcode, pos, immediate):
    val = intcode[pos]
    return val if immediate else intcode[val]


def run(intcode, input_=None):
    intcode = list(intcode)
    output = []
    pos = 0
    while True:
        op, mode1, mode2, _ = parse_op_code(intcode[pos])
        if op == 99:
            return intcode, output
        elif op == 1:
            a = get_value(intcode, pos + 1, mode1)
            b = get_value(intcode, pos + 2, mode2)
            intcode[intcode[pos + 3]] = a + b
            pos += 4
        elif op == 2:
            a = get_value(intcode, pos + 1, mode1)
            b = get_value(intcode, pos + 2, mode2)
            intcode[intcode[pos + 3]] = a * b
            pos += 4
        elif op == 3:
            assert input_ is not None
            intcode[intcode[pos + 1]] = input_
            pos += 2
        elif op == 4:
            a = get_value(intcode, pos + 1, mode1)
            output.append(a)
            pos += 2
        else:
            assert False


def run_verb_noun(intcode, noun, verb):
    intcode = list(intcode)
    intcode[1] = noun
    intcode[2] = verb
    intcode, _ = run(intcode)
    return intcode[0]


def run_diagnostic(intcode):
    _, output = run(intcode, input_=1)
    diag = [v for v in output if v != 0]
    assert len(diag) == 1
    return diag[0]


def run_tests_day2():
    intcode = get_intcode_from_string("1,9,10,3,2,3,11,0,99,30,40,50")
    assert run(intcode) == ([3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50], [])
    assert run_verb_noun(intcode, 9, 10) == 3500
    intcode = get_intcode_from_string("1,0,0,0,99")
    assert run(intcode) == ([2, 0, 0, 0, 99], [])
    assert run_verb_noun(intcode, 0, 0) == 2
    intcode = get_intcode_from_string("2,3,0,3,99")
    assert run(intcode) == ([2, 3, 0, 6, 99], [])
    intcode = get_intcode_from_string("2,4,4,5,99,0")
    assert run(intcode) == ([2, 4, 4, 5, 99, 9801], [])
    intcode = get_intcode_from_string("1,1,1,4,99,5,6,0,99")
    assert run(intcode) == ([30, 1, 1, 4, 2, 5, 6, 0, 99], [])


def run_tests_day5():
    intcode = get_intcode_from_string("1002,4,3,4,33")
    assert run(intcode) == ([1002, 4, 3, 4, 99], [])
    intcode = get_intcode_from_string("1101,100,-1,4,0")
    assert run(intcode) == ([1101, 100, -1, 4, 99], [])


def run_tests():
    run_tests_day2()
    run_tests_day5()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    end = datetime.datetime.now()
    print(end - begin)
