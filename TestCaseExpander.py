#!/usr/bin/python

from __future__ import print_function

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file",             help="File containing all steps and testcases")
parser.add_argument("-o", "--output",   help="output file name")
parser.add_argument("-w", "--warnDangSB",   help="warning unreferenced StepBlocks", action="store_true")
#parser.add_argument("-e", "--exitOnWarning",   help="exit on warnings", action="store_true")

parsed_args = parser.parse_args()

inputfilename = parsed_args.file
outputfilename = parsed_args.output

DemarcaterPattern="=========="
StepBlockPattern="StepBlock: "
ImportPattern="Import: "
TestcasePattern="TestCase: "
NonImportedStepBlocks="NonImportedStepBlocks"

class StepBlock:
    Collection = {}

    def __init__(self, line, lineno):
        name=line[len(StepBlockPattern):]
        name=name.strip()
        if not name:
            raise Exception("No name found for StepBlock in line:%s"%line)
        self.name = name
        self.lineno = lineno
        if self.name in StepBlock.Collection:
            raise Exception("StepBlock with name:%s already exists at line:%d"%(self.name, StepBlock.Collection[self.name].lineno))
        StepBlock.Collection[self.name] = self
        self.type = "StepBlock"
        self.contents = ""
        self.referredCount = 0
        print ("Created StepBlock:%s"%self.name)

    def addALine(self, line):
        self.contents += line

    def addABlock(self, block):
        self.contents += ("\n#" + block.name + '\n')
        self.contents += block.contents
        block.referredCount += 1

    def windup(self, lineno):
        self.finishedBefore = lineno

class TestCase:
    Collection = {}
    List = []
    ListIndex = 0

    def __init__(self, line, lineno):
        name=line[len(TestcasePattern):]
        name=name.strip()
        if not name:
            raise Exception("No name found for TestCase in line:%s"%line)
        self.name = name
        self.lineno = lineno
        if self.name in TestCase.Collection:
            raise Exception("Testcase with name:%s already exists at line:%d"%(self.name, TestCase.Collection[self.name].lineno))
        TestCase.Collection[self.name] = self
        TestCase.List.append(self)
        self.index = TestCase.ListIndex
        TestCase.ListIndex += 1
        self.type = "TestCase"
        self.tccontents = ""
        print ("Created TestCase:%s"%self.name)

    def addALine(self, line):
        self.tccontents += line

    def addABlock(self, block):
        self.tccontents += ("\n#" + block.name + '\n')
        self.tccontents += block.contents
        block.referredCount += 1

    def windup(self, lineno):
        self.finishedBefore = lineno

with open(inputfilename, "r") as fd:
    current_block = None
    for line_no,line in enumerate(fd,1):
        if line.startswith(DemarcaterPattern):
            current_block.windup(line_no)
            current_block=None
        elif line.startswith(StepBlockPattern):
            if current_block:
                print ("StepBlock in middle of a %s block with name:%s. line_no:%d, line:s"%(current_block.type, current_block.name, line_no, line.strip()))
                sys.exit(1)
            try:
              current_block = StepBlock(line, line_no)
            except Exception, e:
                print ("Parse Error at line_no:%d, Error:%s"%(line_no, str(e).strip()))
                sys.exit(1)
        elif line.startswith(ImportPattern):
            if not current_block:
                print ("Import outside of any block. line_no:%d, line:s"%(line_no, line.strip()))
                sys.exit(1)
            name=line[len(ImportPattern):]
            name=name.strip()
            if name not in StepBlock.Collection:
                print ("StepBlock %s not defined so far. line_no:%d, line:%s"%(name, line_no, line.strip()))
                sys.exit(1)
            current_block.addABlock(StepBlock.Collection[name])
        elif line.startswith(TestcasePattern):
            if current_block:
                print ("TestCase in middle of a %s block with name:%s. line_no:%d, line:s"%(current_block.type, current_block.name, line_no, line.strip()))
                sys.exit(1)
            try:
              current_block = TestCase(line, line_no)
            except Exception, e:
                print ("Parse Error at line_no:%d, Error:%s"%(line_no, str(e).strip()))
                sys.exit(1)
        else:
            current_block.addALine(line)

if parsed_args.warnDangSB:
    exit = 0
    for name,sb in StepBlock.Collection.iteritems():
        if sb.referredCount == 0 and name != NonImportedStepBlocks:
            print ("Warning: StepBlock %s, line:%d not imported anywhere"%(name,sb.lineno))
            exit = 1
    if exit:
        sys.exit(0)


with open(outputfilename,"w") as fd:
    for testcase in TestCase.List:
        print ("%s%s"%(TestcasePattern, testcase.name), file=fd)
        print (testcase.tccontents, file=fd)
        print (DemarcaterPattern, file=fd)

