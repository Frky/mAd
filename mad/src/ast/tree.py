#-*- coding: utf-8 -*-

class Tree(object):
    """
        Used to create an AST and evaluate the expression

    """

    def __init__(self, token, left=None, right=None):
        # Check consistancy
        if token.is_binary():
            if left is None or right is None:
                # TODO explicit syntax error
                raise Exception
        elif token.is_unary():
            if left is None or right is not None:
                # TODO explicit syntax error
                raise Exception
        else:
            if left is not None or right is not None:
                # TODO explicit syntax error
                raise Exception
        self.__left = left
        self.__right = right
        self.__token = token
        self.__value = None

    @property
    def right(self):
        return self.__right

    @property
    def left(self):
        return self.__left

    def eval(self, var_dict=None):
        """
            Evaluate the value of the node
            Recursively evaluate the value of children if
            any

            @param var_dict     dictionary of variables defined previously
                                needed to evaluate Token.VAR

        """
        if self.__value is None:
            # Binary operation
            if self.__token.is_binary():
                # Return a function
                op = self.__token.brain()
                # Evaluate left operand
                t0 = self.left.eval(var_dict)
                # Evaluate right operand
                t1 = self.right.eval(var_dict)
                # Comput the value
                self.__value = op(t0, t1)
            # Unary operation
            elif self.__token.is_unary():
                # Return a function
                op = self.__token.brain()
                # Evaluate the operand
                t0 = self.left.value
                self.__value = op(t0)
            # Leaf: either a NUM or a variable
            elif self.__token.is_num():
                self.__value = self.__token.value
            elif self.__token.is_var():
                # If variable
                try:
                    # Try to get its actual value from the dict
                    self.__value = var_dict[self.__token.value]
                except KeyError:
                    # TODO explicit error (variable not previously declared)
                    raise Exception
        return self.__value

