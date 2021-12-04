# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def is_valid(n):
    s = str(n)
    return (len(s) == 6 and
        len(set(s)) <= 5 and
        all(first <= second for first, second in zip(s, s[1:])))


def get_passwords(valid_range):
   mini, maxi = valid_range
   for n in range(mini, maxi):
       if is_valid(n):
           yield n


def run_tests():
    assert is_valid(111111)
    assert not is_valid(223450)
    assert not is_valid(123789)


def get_solutions():
    input_range = 172930, 683082
    print(len(list(get_passwords(input_range))))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
