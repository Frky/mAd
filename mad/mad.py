#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

from src.parser import MadParser
from src.test import MadTest

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: {0} infile [outfile]"
        exit()
    if sys.argv[1] == "test":
        # Run all tests for mad
        MadTest().run()
    else:
        # Normal use
        if len(sys.argv) > 2:
            out = sys.argv[2]
        else:
            out = ""
        madparser = MadParser(sys.argv[1], out)
        madparser.parse()

