#-*- coding: utf-8 -*-

from src.ast.token import Token

class OpStack(object):
    """
        A single class to handle both operand and operator stacks

    """

    def __init__(self):
        self.__operands = list()
        self.__operators = list()
        self.__operators.append(Token('EOF'))

    def pop_operand(self):
        return self.__operands.pop(-1)

    def push_operand(self, value):
        self.__operands.append(value)

    def top_operand(self):
        return self.__operands[-1]

    def pop_operator(self, ignore=False):
        if ignore:
            self.__operators.pop(-1)
            return
        # Binary operation
        if self.top_operator().is_binary():
            # Get two operands
            t0 = self.__operands.pop(-1)
            t1 = self.__operands.pop(-1)
            # Get operator
            op = self.__operators.pop(-1)
            # Add result to operands
            self.__operands.append(op.brain()(t0, t1))
        # Unary operation
        else:
            # Get operand
            t0 = self.__operands.pop(-1)
            # Get operator
            op = self.__operators.pop(-1)
            # Add result to operands
            self.__operands.append(op.brain(t0))

    def push_operator(self, op, no_pop=False):
        if not no_pop:
            # While there are operators with higher priority
            # in the operator stack, compute them
            while self.__operators[-1] > op:
                self.pop_operator()
        # Add operator to the stack
        self.__operators.append(op)

    def top_operator(self):
        return self.__operators[-1]

