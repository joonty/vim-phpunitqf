import sys
import vim
import re

def print_error(msg):
    vim.command("echohl Error | echo \""+msg+"\" | echohl None")

""" 
" Super intelligent debug function
"""
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
        elif parser.foundTestSummary == False:
            vim.command('echohl Error | echo "phpunit failed to run (or so it seems)" | echohl None') 
            vim.command('cclose')
            vim.command('call setqflist([])')
        else:
            vim.command('echohl WarningMsg | echo "No test errors or failures" | echohl None') 
            vim.command('cclose')
            vim.command('call setqflist([])')
    except ParserException, e:
        print_error("An error has occured in parsing the PHPUnit error log: " + e.args[0])
    except Exception, e:
        print_error("An error has occured: " + str(sys.exc_info()))

" Holds information about a single error "
class TestError:
    message = None
    file = None
    line = None

    def __init__(self,type):
        self.type = type

    def setMessage(self,message):
        self.message = message

    def getEscapedMessage(self):
        return self._escape(self.message)

    def setFile(self,file):
        self.file = file

    def getType(self):
        return self.type

    def getEscapedFile(self):
        return self._escape(self.file)

    def setLine(self,line):
        self.line = line

    def getEscapedLine(self):
        return self._escape(self.line)

    def assertComplete(self):
        if self.message == None:
            return False
        elif self.file == None:
            return False
        elif self.line == None:
            return False
        else:
            return True

    def _escape(self,string):
        return string.replace("'","\"")


" A wrapper for a list of errors and failures "
class TestErrorManager:
    def __init__(self):
        self.errors = []

    def add(self,error):
        if error.assertComplete():
            debug("Adding error: \""+ error.message+"\"")
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
            vimstr += "'type':'"+error.getType()+"'"
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
    parsingType = False
    currentError = None
    foundErrors = False
    foundTestSummary = False
    fileReg = "^([^:]+):([0-9]+)$"

    def __init__(self,manager):
        self.errors = manager

    def parse(self,fd):
        k = 0
        try:
            for line in fd:
                if self.foundTestSummary == True:
                    self.parseLine(fd,line)
                if "Time: " in line:
                    self.foundTestSummary = True
                k = k + 1
        except StopIteration:
            pass

    def parseLine(self,fd,line):
        matchObj = re.match('There (?:were|was) ([0-9]*) (error|failure|skipped|incomplete)',line,re.M)
        if matchObj:
            type = matchObj.group(2)
            self.foundErrors = True
            debug("Parsing "+type)
            self.parsingType = type[0].upper()
        if self.foundErrors:
            self.readError(fd,line)

    def readError(self,fd,line):
        matchObj = re.match("^[0-9]\) ([^:]+)::(.+)",line)
        if matchObj:
            testClass = matchObj.group(1)
            testMethod = matchObj.group(2)

            error = TestError(self.parsingType)

            message = "(" + testClass + "::" + testMethod + ")"

            # Get multi-line message
            while True:
                line = fd.next().strip()
                if re.match(self.fileReg,line):
                    break

                message += "\n" + line

            error.setMessage(message)

            testFile = testClass.replace("Case","") + ".php"
            foundFile = False
            firstLine = line

            while True:

                fileName = line
                if len(fileName) == 0:
                    if foundFile == False:
                        print_error("Failed to find the file for test class "+testClass+", using top file")
                        ret = self.parseFileLine(firstLine,error)
                        if ret == False:
                            raise ParserException("Failed to parse the log")
                    break
                elif foundFile == False and testFile in fileName:
                    foundFile = self.parseFileLine(fileName,error)
                    if foundFile == False:
                        print_error("Failed to parse line "+line)
                try:
                    line = fd.next().strip()
                except StopIteration:
                    line = ""

    def parseFileLine(self,line,error):
        matchObj = re.match(self.fileReg,line)
        if matchObj:
            filePath = matchObj.group(1)
            lineNo = matchObj.group(2)
            debug("File: "+filePath+", "+lineNo)
            error.setFile(filePath)
            error.setLine(lineNo)
            self.errors.add(error)
            return True
        else:
            debug("Failed to parse file from line: "+line)
            return False


class ParserException(Exception):
    pass
