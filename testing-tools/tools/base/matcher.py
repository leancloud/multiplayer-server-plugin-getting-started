
class Any:
    def __str__(self):
        return "ANY"

    def __repr__(self):
        return "ANY"


MATCH_ANY = Any()


def partial_match_json(expect, actual):
    if expect == MATCH_ANY and actual is not None:
        pass
    elif isinstance(expect, bool):
        if expect == False and actual is None:
            return True
        else:
            return actual == expect
    elif isinstance(expect, dict):
        if not isinstance(actual, dict):
            print('type failed %s not equals to %s' % (actual, expect))
            return False
        else:
            for k, expect_v in expect.items():
                if k in actual:
                    actual_v = actual.get(k)
                    if not partial_match_json(expect_v, actual_v):
                        return False
                else:
                    return False
    elif isinstance(expect, set):
        if not isinstance(actual, list):
            print('expect type is set but actual type is not list. expect: %s, actual: %s' % (
                expect, actual))
            return False
        if len(set(actual)) != len(actual):
            print('expect type is set but there are duplicate values in actual. expect: %s, actual: %s' % (
                expect, actual))
            return False
        return set(actual) == expect
    elif isinstance(expect, (list, )):
        if not isinstance(actual, (list, )):
            print('type failed %s not equals to %s' % (actual, expect))
            return False
        for actual_v, expect_v in zip(actual, expect):
            if not partial_match_json(expect_v, actual_v):
                return False
    else:
        if actual != expect:
            return False
    return True


if __name__ == "__main__":
    json_dict = {'a': 1, 'b': "2", 'c': 3, 'd': "4",
                 'e': {'a': 3, 'b': 4, 'c': "5"},
                 'f': ['a', 2, 'c', 3, True, 'd', None],
                 'setV': ['1', 2, 'haha', 'hoho']}
    assert partial_match_json({'a': 1, 'b': MATCH_ANY,
                               'e': {'a': MATCH_ANY, 'c': "5"},
                               'f': ['a', 2, 'c', MATCH_ANY],
                               'setV': set(['1', 2, 'haha', 'haha', 'hoho'])},
                              json_dict)
    assert not partial_match_json({'a': 1, 'b': MATCH_ANY,
                                   'e': {'a': MATCH_ANY, 'c': "5"},
                                   'f': ['a', 2, 'c', MATCH_ANY, 'd', MATCH_ANY]},
                                  json_dict)
    assert not partial_match_json({'a': 2, 'b': MATCH_ANY,
                                   'e': {'a': MATCH_ANY, 'c': "5"},
                                   'f': ['a', 2, 'c', MATCH_ANY]},
                                  json_dict)

    assert not partial_match_json({'a': 1, 'b': MATCH_ANY,
                                   'e': {'a': 66, 'c': "5"},
                                   'f': ['a', 2, 'c', MATCH_ANY]},
                                  json_dict)

    assert not partial_match_json({'a': 1, 'b': MATCH_ANY,
                                   'e': {'a': MATCH_ANY, 'c': "5"},
                                   'f': ['a', 3, 'c', MATCH_ANY]},
                                  json_dict)
