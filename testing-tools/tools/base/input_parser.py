"""
Functions to parse input from command line
"""
import json

_UNSET = object()


class Lexer(object):
    def __init__(self, input_str):
        self._input_str = input_str
        self._pos = 0
        self._skip_whitespaces()

    def next_msg(self):
        ret = dict()
        while not self._isoverflow():
            key = self._next_keyword()
            if key is None:
                raise RuntimeError(
                    "parse keyword in dict failed. input: %s" % self._input_str)

            value = self._next_value()
            if value is None:
                raise RuntimeError(
                    "parse value in dict failed. input: %s" % self._input_str)
            elif value == _UNSET:
                value = None

            ret[key] = value

            self._skip_whitespaces()
        return ret

    def _isoverflow(self):
        return self._pos >= len(self._input_str)

    def _skip_whitespaces(self):
        while not self._isoverflow() and self._input_str[self._pos].isspace():
            self._pos += 1

    def _next_keyword(self):
        self._skip_whitespaces()

        key = self._next_consecutive_literals(lambda x: x.isalpha())
        if key and not self._input_str[self._pos - 1].isspace():
            raise RuntimeError(format(
                "Invalid char '%s' for keyword in input: \"%s\"" % (self._input_str[self._pos - 1], self._input_str)))
        return key

    def _next_value(self):
        self._skip_whitespaces()
        if self._isoverflow():
            return None

        char = self._input_str[self._pos]
        if char == '{':
            dict_end_pos = self._search_block_end('{', '}')
            v = Lexer(self._input_str[self._pos + 1:dict_end_pos]).next_msg()
            self._pos = dict_end_pos + 1
            return v
        elif char == '[':
            return self._next_list()
        elif char in ['\'', '\"']:
            return self._next_string()
        else:
            literals = self._next_consecutive_literals(
                lambda x: not x.isspace())
            if literals.lower() == 'true':
                return True
            elif literals.lower() == 'false':
                return False
            elif literals.lower() == 'nil':
                return _UNSET
            else:
                v = None
                try:
                    v = int(literals)
                except ValueError:
                    try:
                        v = float(literals)
                    except ValueError:
                        v = literals
                return v

    def _next_list(self):
        ret = list()
        block_end_pos = self._search_block_end('[', ']')

        self._pos += 1
        list_vals = Lexer(self._input_str[self._pos:block_end_pos])
        while not list_vals._isoverflow():
            value = list_vals._next_value()
            if value == _UNSET:
                value = None
            ret.append(value)

            list_vals._skip_whitespaces()

        self._pos = block_end_pos + 1
        return ret

    def _next_string(self):
        string_end_pos = self._search_block_end()
        ret_str = self._input_str[self._pos + 1:string_end_pos]
        self._pos = string_end_pos + 1
        return ret_str

    def _search_block_end(self, left_mark=None, right_mark=None):
        if left_mark is None:
            left_mark = self._input_str[self._pos]

        if right_mark is None:
            right_mark = left_mark

        pair_count = 1
        cursor = self._pos + 1
        while cursor < len(self._input_str):
            if self._input_str[cursor] == right_mark:
                pair_count -= 1
                if pair_count == 0:
                    break
            elif self._input_str[cursor] == left_mark:
                pair_count += 1
            cursor += 1
        if cursor >= len(self._input_str):
            raise ValueError(
                format("block not closed in input: \"%s\"" % self._input_str))

        return cursor

    def _next_consecutive_literals(self, filter_fn):
        cursor = self._pos
        while cursor < len(self._input_str):
            char = self._input_str[cursor]
            if filter_fn(char):
                cursor += 1
            else:
                break

        literals = self._input_str[self._pos:cursor]
        self._pos = cursor + 1
        return literals


def parse_input_cmd_args(input_str):
    return Lexer(input_str).next_msg()


def assert_equal(expect, actual):
    if expect != actual:
        raise AssertionError(format(
            "assert equal failed. expect: %s actual: %s" % (expect, actual)))


if __name__ == "__main__":
    assert_equal({'cmd': 'session', 'op': 'open', 'appId': 'hahah"a"h\'a\'ha', 't': 23232323, 'unique': True, 'cid': None, 'live': False},
                 Lexer("cmd 'session' op 'open' appId hahah\"a\"h\'a\'ha \t t     23232323 unique true cid nil live False").next_msg())

    assert_equal({'attr': {'level': 100, 'unique': True, 'cid': None}},
                 Lexer("attr {level 100 unique true  cid    nil}").next_msg())

    assert_equal({'attr': {'level': 100, 'unique': True, 'inner': {'gender': 'male', 'cid': None}}},
                 Lexer("attr {level 100 unique true  inner {gender male cid nil}}").next_msg())

    assert_equal({'attr': {'level': 100, 'unique': True, 'inner': {'gender': 'male', 'cid': None, 'list': ['asdf', 111]}}},
                 Lexer("attr {level 100 unique true  inner {gender male cid nil   list [asdf 111]}}").next_msg())

    assert_equal({'attr': {'level': 100.0, 'inner': {'gender': 'male', 'info': {'age': 100.0, 'company': 'MS'},
                                                     'list': ['asdf', 111.0, True, None, [666, {'haha': 'nihao'}]], 'niu': False}}},
                 Lexer("attr {  level 100 inner {gender male info {  age 100 company MS} list [asdf 111 True nil [ 666 {haha nihao}  ]  ] niu False}}").next_msg())
