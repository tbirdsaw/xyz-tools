#!/usr/bin/python 
from struct import *
import sys
import os

offsetFile = 0;

gcodeFile = "testfiles/test.gcode"

gcode = open(gcodeFile, 'r')

def errprint(message):
	sys.stderr.write(message + "\n");


def checkSum(st):
        # Generate checksum for the given data by adding up all the values
	return sum(ord(c) for c in st)

def readChunk():
	global offsetFile;
        #Read 10236 bytes of data
	gcode.seek(offsetFile)
	dataChunk = gcode.read(10236);
	#ckChunk = checkSum(dataChunk);
        #print dataChunk + hex(ckChunk);
	return dataChunk;

def generateSerialChunk(byteChunk):
	# Convert the string into a byte array
	dataStream = bytearray(byteChunk,"ascii");
	# Generate our checksum
	checkData = checkSum(byteChunk)

	# Convert the integer into a byte array
	ckStream = bytearray(pack('>i',checkData));
	
#	sys.stderr.write("Checksum for chunk is: " + str(checkData) + "\n")
	errprint("Checksum for chunk is: " + str(checkData));

	# Concatenate the two byte arrays and return
	return dataStream + ckStream
	
def readFile():
	global offsetFile
	chunkFile = readChunk();
	offsetFile = offsetFile + 10236
	print str(len(chunkFile))
	errprint("OffsetFile is: " + str(offsetFile))
	while len(chunkFile) == 10236 :
		errprint( "at position " + str(gcode.tell()) + " in file")
		#sys.stdout.write(generateSerialData(chunkFile))
		offsetFile = offsetFile + 10236
		chunkFile = readChunk();
		print str(len(chunkFile))
	errprint("Finished")

print os.stat(gcodeFile).st_size
readFile()
