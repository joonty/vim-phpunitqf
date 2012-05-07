import os
import sys
import vim
import re

def print_error(msg):
    vim.command("echohl Error | echo \""+msg+"\" | echohl None")

def parse_test_output( ):
    fd = open("/tmp/caketest_output")
    manager = TestErrorManager()
    parser = TestOutputParser(manager)
    parser.parse(fd)
    fd.close()
    manager.addToQuickfix()

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
        elif self.file == None:
            return False
        elif self.line == None:
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

    def add(self,error):
        if error.assertComplete():
            print "Adding error: "+ error.message
            self.errors.append(error)
        else:
            print_error("Incomplete error object")

    def addToQuickfix(self):
        vimstr = "{"
        idx = 1
        for error in self.errors:
            if idx > 1:
                vimstr += ","
            vimstr += str(idx) + ": {"
            vimstr += "'filename':'"+error.file+"',"
            vimstr += "'lnum':'"+str(error.line)+"',"
            vimstr += "'text':'"+error.message+"',"
            vimstr += "'type':'"+error.type+"'"
            vimstr += "}"
        vimstr += "}"
        vim.command('call setqflist('+vimstr+')')


class TestOutputParser:
    parsingErrors = False
    parsingFailures = False
    currentError = None
    foundErrors = False

    def __init__(self,manager):
        self.errors = manager

    def parse(self,fd):
        k = 0
        found = False
        for line in fd:
            if found == True:
                self.parseLine(fd,line)
            if "Time: " in line:
                found = True
            k = k + 1

    def parseLine(self,fd,line):
        if self.foundErrors == False:
            matchObj = re.match('There (?:were|was) ([0-9]*) (error|failure)',line,re.M)
            if matchObj:
                numfails = matchObj.group(1)
                type = matchObj.group(2)
                self.foundErrors = True
                if type == "error":
                    self.parsingErrors = True
                    print "Parsing errors"
                else:
                    self.parsingFailures = True
                    print "Parsing failures"
        else:
            matchObj = re.match("^[0-9]\) ([^:]+)::(.+)",line)
            if matchObj:
                testClass = matchObj.group(1)
                testMethod = matchObj.group(2)
                message = "[" + testClass + "::" + testMethod + "]"
                message += " " + fd.next()

                if self.parsingErrors:
                    error = TestError()
                else:
                    error = TestFailure()

                error.setMessage(message)

                # Skip blank line
                fd.next()
                testFile = testClass.replace("Case","") + ".php"
                foundFile = False

                while True:
                    fileName = fd.next().strip()
                    if len(fileName) == 0:
                        if foundFile == False:
                            print_error("Failed to find the file for test class "+testClass)
                        break
                    elif foundFile == False and testFile in fileName:
                        matchObj = re.match("^([^:]+):(.+)$",fileName)
                        if matchObj:
                            filePath = matchObj.group(1)
                            lineNo = matchObj.group(2)
                            print "File: "+filePath+", "+lineNo
                            error.setFile(filePath)
                            error.setLine(lineNo)
                            foundFile = True
                            self.errors.add(error)
                        else:
                            print_error("Failed to parse line "+fileName)


