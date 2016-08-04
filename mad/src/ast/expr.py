#-*- coding: utf-8 -*-

import re

from src.ast.token import Token
from src.ast.opstack import OpStack

class Tree(object):

    def __init__(self, tok, left=None, right=None):
        self.__token = tok
        self.__left = left
        self.__right = right
        # Compute node value
        if tok.type == Token.NUM:
            self.__value = tok.value
        elif tok.is_binary():
            self.__value = tok.brain()(left.value, right.value)

    @property
    def value(self):
        return self.__value

class Expr(object):

    def __init__(self, expr):
        self.__expr = expr
        self.__stack = OpStack()
        self.__tokens = list()
        self.__parse_tokens()

    def __parse_tokens(self):
        split_expr = re.findall('[\d.]+|[%s]' % ''.join(Token.token_map), self.__expr)
        self.__tokens = [Token(x) for x in split_expr]
        self.__tokens.append(Token('EOF'))

    def __next(self):
        # TODO handle EOF
        return self.__tokens[0]

    def __consume(self):
        # TODO handle EOF
        return self.__tokens.pop(0)
    
    def __error(self, msg):
        raise Exception(msg)

    def __expect(self, tok):
        if self.__next() == tok:
            return self.__consume()
        else:
            return self.__error("Token expected ({0}) not found (next: {1})".format(tok, self.__next()))

    def __p(self):
        if self.__next().is_num():
            self.__stack.push_operand(self.__consume().value)
        else:
            self.__error("Syntax Error")

    def __e(self):
        self.__p()
        while self.__next().is_binary():
            self.__stack.push_operator(self.__consume())
            self.__p()
        while self.__stack.top_operator() != Token('EOF'):
            self.__stack.pop_operator()

    def parse(self):
        self.__e()
        self.__expect(Token('EOF'))
        return self.__stack.top_operand()

    def eval(self):
        # TODO handle errors (eg if int parsing fails)
        return self.parse()
