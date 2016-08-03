#-*- coding: utf-8 -*-

import re
from operator import add, mul

from token import Token

class Expr(object):

    calc_map = {
                    'ADD': add,
                    'MUL': mul,
            }

    def __init__(self, expr):
        self.__expr = expr
        self.__rules = list()
        self.__tokens = list()
        self.__parse()

    def __parse(self):
        split_expr = re.findall('[\d.]+|[%s]' % ''.join(Token.token_map), self.__expr)
        self.__tokens = [Token(x) for x in split_expr]

    def eval(self):
        # TODO For now, no priority of MULT over ADD
        # TODO handle errors (eg if int parsing fails)
        res = int(self.__tokens.pop(0).value)
        while len(self.__tokens) != 0:
            # Get operation
            op = self.__tokens.pop(0).name
            # Get second operand
            right = int(self.__tokens.pop(0).value)
            res = Expr.calc_map[op](res, right)
        return res
