#-*- coding: utf-8 -*-

import glob
import os

from src.parser import MadParser

class UnitTest(object):

    def __init__(self, testid, testdir, verbose=True):
        self.__id = testid
        self.__testdir = testdir
        self.__verbose = verbose
        self.__nb_ok = 0
        self.__nb_tot = 0

    def __ok(self, msg):
        self.__nb_ok += 1
        self.__nb_tot += 1
        if self.__verbose:
            print "[ok] {0}".format(msg)

    def __ko(self, msg):
        self.__nb_tot += 1
        if self.__verbose:
            print "[ko] {0}".format(msg)

    def run(self):
        # Perform computation of test file
        MadParser("{0}/{1}.mad".format(self.__testdir, self.__id)).parse()
        # Parse result 
        return self.__result()

    def __result(self):
        # Open oracle
        with open("{0}/{1}.oracle".format(self.__testdir, self.__id), "r") as oracle:
            # Open source file
            with open("{0}/{1}.mad".format(self.__testdir, self.__id), "r") as mad:
                # Open result file
                with open("{0}/{1}.md".format(self.__testdir, self.__id), "r") as md:
                    for ora, inp, out in zip(oracle.readlines(), mad.readlines(), md.readlines()):
                        if ora == out:
                            self.__ok("{0}:{1}".format(self.__id, inp[:-1]))
                        else:
                            self.__ko("{3}:{0} [ expected {1} | got {2} ]".format(inp[:-1], ora[:-1], out[:-1], self.__id))
        return self.__nb_ok, self.__nb_tot

class MadTest(object):

    def __init__(self, test_dir="test"):
        self.__nb_ok = 0
        self.__nb_ko = 0
        self.__nb_tot = 0
        self.__testdir = test_dir

    def __ok(self, test_id="", verbose=True):
        self.__nb_ok += 1
        self.__nb_tot += 1
        if verbose:
            print "[ok] {0}".format(test_id)

    def __ko(self, test_id, verbose=True):
        self.__nb_ko += 1
        self.__nb_tot += 1
        if verbose:
            print "[ko] {0}".format(test_id)

    def run(self):
        for test in glob.glob("{0}/*.mad".format(self.__testdir)):
            # Get test file name without path and without extension
            test_name = os.path.splitext(os.path.basename(test))[0]
            # Run Unit Test
            ok, tot = UnitTest(test_name, self.__testdir).run()
