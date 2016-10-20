#!/usr/bin/python

from __future__ import print_function

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file",             help="File containing all steps and testcases")
parser.add_argument("-o", "--output"    help="output file name")

parsed_args = parser.parse_args()

inputfilename = parsed_args.file
outputfilename = parsed_args.output

DemarcaterPattern="=========="
StepBlockPattern="StepBlock: "
ImportPattern="Import: "
TestcasePattern="TestCase: "

class StepBlock:
    Collection = {}

    def __init__(self, line, lineno):
        name=line[len(StepBlockPattern):]
        name=name.strip()
        if not name:
            raise Exception("No name found for StepBlock in line:%s"%line)
        self.name = name
        self.lineno = lineno
        if self.name in SelfBlock.Collection
            raise Exception("SelfBlock with name:%s already exists at line:%d"%self.name, self.lineno)
        SelfBlock.Collection[self.name] = self
        self.type = "SelfBlock"
        self.contents = ""

    def addALine(self, line):
        self.contents += line

    def addABlock(self, block):
        self.contents += block.contents

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
        if self.name in TestCase.Collection
            raise Exception("Testcase with name:%s already exists at line:%d"%self.name, self.lineno)
        TestCase.Collection[self.name] = self
        TestCase.List.append(self)
        self.index = TestCase.ListIndex
        TestCase.ListIndex += 1
        self.type = "TestCase"
        self.contents = ""

    def addALine(self, line):
        self.contents += line

    def addABlock(self, block):
        self.contents += block.contents

    def windup(self, lineno):
        self.finishedBefore = lineno

with open(inputfilename, "r") as fd:
    current_block = None
    for line_no, line in enumerate(1,fd):
        if line.startswith(DemarcaterPattern):
            current_block.windup(line_no)
            current_block=None
        elif line.startswith(StepBlockPattern):
            if current_block:
                printf ("StepBlock in middle of a %s block with name:%s. line_no:%d, line:s"%(current_block.type, current_block.name, line_no, line.strip()))
                sys.exit(1)
            try:
              current_block = StepBlock(line, line_no)
            except Exception, e:
                printf ("Parse Error at line_no:%d, Error:s"%(line_no, str(e).strip()))
                sys.exit(1)
        elif line.startswith(ImportPattern):
            if not current_block:
                printf ("Import outside of any block. line_no:%d, line:s"%(line_no, line.strip()))
                sys.exit(1)
            name=line[len(StepBlockPattern):]
            if name not in StepBlock.Collection:
                printf ("StepBlock %s not defined so far. line_no:%d, line:%s"(name, line_no, line.strip()))
                sys.exit(1)
            current_block.addABlock(StepBlock.Collection[name])
        elif line.startswith(TestcasePattern):
            if current_block:
                printf ("TestCase in middle of a %s block with name:%s. line_no:%d, line:s"%(current_block.type, current_block.name, line_no, line.strip()))
                sys.exit(1)
            try:
              current_block = TestCase(line, line_no)
            except Exception, e:
                printf ("Parse Error at line_no:%d, Error:s"%(line_no, str(e).strip()))
                sys.exit(1)

with open(outputfilename,"w") as fd:
    for testcase in TestCase.List:
        print ("Testcase: %s"%(testcase.name), file=fd)
        print (testcase.contents, file=fd)
        print (DemarcaterPattern, file=fd)

