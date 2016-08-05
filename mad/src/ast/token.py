#-*- coding: utf-8 -*-

from operator import add, mul

class Token(object):

    ADD = 0
    MUL = 1
    LPAR = 2
    RPAR = 3
    NUM = 4
    EOF = 5
    VAR = 6

    # Binary operators
    binary = [
                ADD,
                MUL,
            ]

    # Unary operators
    unary = [

            ]

    # Defines priority of binary operations
    priority = [
                    MUL, 
                    ADD,
                    EOF,
                ]

    # Map from character to operator
    token_map = {
                    '+':    ADD, 
                    '-':    ADD,
                    '*':    MUL, 
                    '/':    MUL,
                    '(':    LPAR,
                    ')':    RPAR,
                    'EOF':  EOF,
                }

    # Define functions to handle real operations to be computed
    bin_map = {
                ADD: add,
                MUL: mul,
            }

    def __init__(self, value):
        self.__type = Token.token_map.get(value, None)
        if self.__type is None:
            try:
                int(value)
                self.__type = Token.NUM
            except ValueError:
                self.__type = Token.VAR
        self.__value = value

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        if self.type == Token.NUM:
            try:
                return int(self.__value)
            except ValueError:
                raise Exception
        else:
            return self.__value

    def __str__(self):
        return "{0}({1})".format(self.type, self.value)

    def __eq__(self, tok):
        if not isinstance(tok, Token):
            return False
        return self.type == tok.type and self.value == tok.value

    def __ne__(self, tok):
        return not self.__eq__(tok)

    def __lt__(self, tok):
        if not isinstance(tok, Token):
            raise TypeError
        if self.type == Token.NUM and tok.type == Token.NUM:
            return self.value < tok.value
        elif self.type in Token.priority and tok.type in Token.priority:
            return Token.priority.index(self.type) > Token.priority.index(tok.type)
        else:
            raise TypeError("Cannot compare two Tokens of different type: {0} and {1}".format(self.type, tok.type))

    def __gt__(self, tok):
        return not self.__eq__(tok) and not self.__lt__(tok)

    def is_binary(self):
        return self.type in Token.binary

    def is_unary(self):
        return self.type in Token.unary

    def is_num(self):
        return self.type == Token.NUM

    def is_var(self):
        return self.type == Token.VAR

    def is_operand(self):
        return self.type == Token.NUM or self.type == Token.VAR

    def is_left_parenthesis(self):
        return self.type == Token.LPAR

    def is_right_parenthesis(self):
        return self.type == Token.RPAR

    def brain(self):
        if self.is_binary:
            return Token.bin_map[self.type]
        else:
            raise TypeError("Cannot ask for function handler for anything else than binary or unary operation")
