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
    for line in fd:
        if k == firsterr:
            parsing = True
        if parsing:
            print line
        if found == True:
            p = re.compile('There (?:were|was) ([0-9]*) failure',line)
            m = p.match(line)
            numfails = m.group(1)
            firsterr = k+2
            break
        if "Time: " in line:
            found = True
        k = k + 1
    

