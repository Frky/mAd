#-*- coding: utf-8 -*-

import re

from src.ast.token import Token
from src.ast.opstack import OpStack

class Expr(object):

    def __init__(self, expr, var_dict):
        """
            @param var_dict     dictionary of values for variables previously defined

        """
        self.__expr = expr
        self.__stack = OpStack()
        self.__tokens = list()
        self.__vars = var_dict
        self.__parse_tokens()

    def __parse_tokens(self):
        """
            From input string, parse tokens

        """
        split_expr = re.findall('[\d.]+|[%s]|[a-z]+' % ''.join(Token.token_map), self.__expr)
        self.__tokens = [Token(x, self.__vars) for x in split_expr]
        self.__tokens.append(Token('EOF'))

    def __next(self):
        """
            Next token to be treated in expression

        """
        # TODO handle EOF
        return self.__tokens[0]

    def __consume(self):
        """
            Return the next token to be treated and remove it from
            the list of tokens

        """
        # TODO handle EOF
        return self.__tokens.pop(0)
    
    def __error(self, msg):
        """
            Raise a syntax error

        """
        raise Exception(msg)

    def __expect(self, tok):
        """
            Is the token what we expected at this point?

        """
        if self.__next() == tok:
            return self.__consume()
        else:
            return self.__error("Token expected ({0}) not found (next: {1})".format(tok, self.__next()))

    def __p(self):
        if self.__next().is_num():
            self.__stack.push_operand(self.__consume().value)
        elif self.__next().is_left_parenthesis():
            self.__consume()
            self.__stack.push_operator(Token('EOF'), no_pop=True)
            self.__e()
            self.__expect(Token(')'))
            self.__stack.pop_operator(ignore=True)
        else:
            self.__error("Syntax Error: {0}".format(self.__next()))

    def __e(self):
        self.__p()
        while self.__next().is_binary():
            self.__stack.push_operator(self.__consume())
            self.__p()
        while self.__stack.top_operator() != Token('EOF'):
            self.__stack.pop_operator()

    def parse(self):
        """
            Parse syntaxically the succession of tokens
            And evaluate the expression

        """
        self.__e()
        self.__expect(Token('EOF'))
        return self.__stack.top_operand()

    def eval(self):
        # TODO handle errors (eg if int parsing fails)
        return self.parse()

