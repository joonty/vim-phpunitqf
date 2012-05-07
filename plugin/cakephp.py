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
    parser.parse(fd)

class TestError:
    message = None
    file = None
    line = None
    type = "E"

    def setMessage(self,message):
        self.message = message

    def setFile(self,file):
        self.file = file

    def setLine(self,line):
        self.line = line

    def assertComplete(self):
        if self.message == None:
            return false
        else if self.file == None:
            return False
        else if self.line == None:
            return False
        else:
            return True


class TestFailure(TestError):
    def __init__(self):
        TestError.__init__(self)
        self.type = "F"


class TestErrorManager:
    def __init__(self):
        self.errors = []
        self.failures = []

    def addError(self,error):
        if error.assertComplete():
            self.errors.add(error)

    def addFailure(self,failure):
        if failure.assertComplete():
            self.failures.add(failure)

class TestOutputParser:
    parsingErrors = False
    parsingFailures = False

    def __init__(self):
        self.errors = TestErrorManager()

    def parse(self,fd):
        for line in fd:
            if found == True:
                self.parseLine(line)
            if "Time: " in line:
                found = True
            k = k + 1

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

