#!/usr/bin/python 
from struct import *
import sys
import os

offsetFile = 0;


#Open our file
gcodeFile = "testfiles/test.gcode"
gcode = os.fdopen(os.open(gcodeFile,os.O_RDONLY))


def errprint(message):
	sys.stderr.write(message + "\n");


def checkSum(st):
        # Generate checksum for the given data by adding up all the values
	return sum(ord(c) for c in st)

def readChunk(fileOffset):
        #Seek to the given location and read 10236 bytes of data
	gcode.seek(fileOffset)
	dataChunk = gcode.read(10236);
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
	# Set our fileOffset so we know where we are in the file
	fileOffset = 0;
	# Get file length for percentage calculator
	fileLen = os.stat(gcodeFile).st_size;

	# Loop until we run out of file
	while True:
		# Read our first chunk of file
		chunkOfFile = readChunk(fileOffset)
		serialDataChunk = generateSerialChunk(chunkFile)
		
		# In the main program, serial handling code and upload code goes here
		sys.stdout.write(serialDataChunk)
		
		# Check to see if the chunk is smaller than 10236, if so, break.
		if len(chunkFile) != 10236:
			break

		# Update our offset point
		fileOffset = fileOffset + 10236
		
		# Let the user know how far we are through the file
		errprint("Processed {:0.2f}% of file.".format((fileOffset / float(fileLen) * 100)))


	errprint("Finished")

readFile()
