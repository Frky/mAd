#-*- coding: utf-8 -*-

class Token(object):

    token_map = {
                    '+':'ADD', 
                    '-':'ADD',
                    '*':'MUL', 
                    '/':'MUL',
                }

    def __init__(self, value):
        self.__name = Token.token_map.get(value, 'NUM')
        self.__value = value

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    def __str__(self):
        return "{0}({1})".format(self.__name, self.__value)
