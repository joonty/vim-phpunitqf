import os
import sys
import vim
import re

def print_error(msg):
    vim.command("echohl Error | echo \""+msg+"\" | echohl None")

def debug(msg):
    if debugOn == 1:
        print msg

def parse_test_output( ):
    global debugOn 
    try:
        fname = vim.eval("g:phpunit_tmpfile")
        debugOn = int(vim.eval("g:phpunit_debug"))
        fd = open(fname)
    except IOError as e:
        print_error("Failed to find or open the PHPUnit error log - the command may have failed")

    try:
        manager = TestErrorManager()
        parser = TestOutputParser(manager)
        parser.parse(fd)
        fd.close()
        if manager.hasErrors():
            manager.addToQuickfix()
    except:
        print_error("An error has occured in parsing the PHPUnit error log")

" Holds information about a single error "
class TestError:
    message = None
    file = None
    line = None
    type = "E"

    def setMessage(self,message):
        self.message = message

    def getEscapedMessage(self):
        return self._escape(self.message)

    def setFile(self,file):
        self.file = file

    def getEscapedFile(self):
        return self._escape(self.file)

    def setLine(self,line):
        self.line = line

    def getEscapedLine(self):
        return self._escape(self.line)

    def assertComplete(self):
        if self.message == None:
            return false
        elif self.file == None:
            return False
        elif self.line == None:
            return False
        else:
            return True

    def _escape(self,string):
        return string.replace("'","\'")


" Extends TestError, to represent a failure "
class TestFailure(TestError):
    type = "F"


" A wrapper for a list of errors and failures "
class TestErrorManager:
    def __init__(self):
        self.errors = []

    def add(self,error):
        if error.assertComplete():
            debug("Adding error: "+ error.message)
            self.errors.append(error)
        else:
            print_error("Incomplete error object")

    def addToQuickfix(self):
        vimstr = "["
        idx = 1
        for error in self.errors:
            if idx > 1:
                vimstr += ","
            vimstr += "{"
            vimstr += "'filename':'"+error.getEscapedFile()+"',"
            vimstr += "'lnum':'"+error.getEscapedLine()+"',"
            vimstr += "'text':'"+error.getEscapedMessage()+"',"
            vimstr += "'type':'"+error.type+"'"
            vimstr += "}"
            idx += 1
        vimstr += "]"
        debug("Vim list: "+vimstr)
        vim.command('call setqflist('+vimstr+')')
        vim.command('copen')

    def hasErrors(self):
        return len(self.errors) > 0


" A parser for the error log "
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
        matchObj = re.match('There (?:were|was) ([0-9]*) (error|failure)',line,re.M)
        if matchObj:
            numfails = matchObj.group(1)
            type = matchObj.group(2)
            self.foundErrors = True
            if type == "error":
                self.parsingErrors = True
                debug("Parsing errors")
            else:
                self.parsingFailures = True
                self.parsingErrors = False
                debug("Parsing failures")

        self.readError(fd,line)

    def readError(self,fd,line):
        matchObj = re.match("^[0-9]\) ([^:]+)::(.+)",line)
        if matchObj:
            testClass = matchObj.group(1)
            testMethod = matchObj.group(2)

            if self.parsingFailures:
                error = TestFailure()
            else:
                error = TestError()

            message = "(" + testClass + "::" + testMethod + ")"
            message += " " + fd.next()

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
                        debug("File: "+filePath+", "+lineNo)
                        error.setFile(filePath)
                        error.setLine(lineNo)
                        foundFile = True
                        self.errors.add(error)
                    else:
                        print_error("Failed to parse line "+fileName)


