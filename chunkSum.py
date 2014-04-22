#!/usr/bin/python 

gcodeFile = "testfiles/test.gcode"

gcode = open(gcodeFile, 'r')

def checkSum(st):
#    return reduce(lambda x,y:x+y, map(ord, st))
        return sum(ord(c) for c in st)

def generateChunk():
        # Reset file to beginning, just in case
        #gcode.seek(0)
        dataChunk = gcode.read(10236);
	ckChunk = checkSum(dataChunk);
        print dataChunk + hex(ckChunk);

generateChunk();

