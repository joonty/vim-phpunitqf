import os
import sys
import vim
import re

def parse_test_output( ):
    fd = open("/tmp/caketest_output")
    found = False
    parsing = False
    k = 0
    firsterr = -1
    numfails = 0
    parser = TestOutputParser()
    for line in fd:
        if found == True:
            parser.parseLine(line)
        if "Time: " in line:
            found = True
        k = k + 1

class TestError:
    type = "E"
    def __init__(self,message,file,line):
        self.message = message
        self.file = file
        self.line = line

class TestFailure(TestError):
    def __init__(self,message,file,line):
        TestError.__init__(self,message,file,line)
        self.type = "F"


class TestErrorManager:
    
    def __init__(self):
        self.errors = []
        self.failures = []

    def addError(self,error):
        self.errors.add(error)

    def addFailure(self,failure):
        self.failures.add(failure)

class TestOutputParser:
    parsingErrors = False
    parsingFailures = False

    def __init__(self):
        self.errors = TestErrorManager()

    def parseLine(self,line):

        matchObj = re.match('There (?:were|was) ([0-9]*) (error|failure)',line,re.M)
        if matchObj:
            numfails = matchObj.group(1)
            type = matchObj.group(2)
            if type == "error":
                self.parsingErrors = True
                print "Parsing errors"
            else:
                self.parsingFailures = True
                print "Parsing failures"
        else:
            print "No match"
        print line

