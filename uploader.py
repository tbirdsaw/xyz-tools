#!/usr/bin/python
from struct import *
import sys
import os
import serial;
import io;
import time;

offsetFile = 0;


# Hardcode parameters for now
# Parameters set for XYZ from watching the traffic
DEVICE='/dev/ttyACM0'
TIMEOUT = 1	# We want to block the program until we get a response back
BAUDRATE = 115200
gcodeFile = "testfiles/test.gcode"
DEBUGMODE = 1
SERIALENABLE = 1


#Known Commands
MACHINE_INFO = 'XYZ_@3D:'
MACHINE_LIFE = MACHINE_INFO + '5'
EXTRUDER1_INFO = MACHINE_INFO + '6'
EXTRUDER2_INFO = MACHINE_INFO + '7'
STATUS_INFO = MACHINE_INFO + '8'
SEND_FILE = MACHINE_INFO + '4'


#Open our file
gcode = os.fdopen(os.open(gcodeFile,os.O_RDONLY))

#Open serial port
if SERIALENABLE == 1:
	sport = serial.Serial(DEVICE,baudrate=BAUDRATE,timeout=TIMEOUT,xonxoff=1,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE);
	sio = io.TextIOWrapper(io.BufferedRWPair(sport,sport),newline='\n')

def errprint(message):
	sys.stderr.write(message + "\n");

def writeData(data):
	if DEBUGMODE == 1:
		errprint("Sending: " + data)
	if SERIALENABLE == 1:
		sio.write(data)
		sio.flush()

def readData():
	time.sleep(1)
	returnData = ''
	if SERIALENABLE == 1:
		returnData = sio.readline()
	else:
		returnData = "Serial Disabled"

	if DEBUGMODE == 1:
		errprint("Received: " + returnData)

	return returnData;

def checkReturnedData(expectedData,returnedData):
	if expectedData == returnedData:
		return 0
	else:
		return 1


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
	
	errprint("Checksum for chunk is: " + str(checkData));

	# Concatenate the two byte arrays and return
	return dataStream + ckStream

# This sends our required? header
def sendGCodeHeader(fileName,fileLen):
	# Write out our predetermined string
	writeData(SEND_FILE)
	readData()
	
	writeData("M1:{:s},{:d},2.55.43,EE1_OK,EE2_OK".format(fileName,fileLen))
	if checkReturnedData("OFFLINE_OK..",readData()) == 1:
		errprint("Data doesn't match expected returned?!")
	

# This sends the GCode chunk and makes sure we get a OK response back.
def sendSerialChunk(serialDataChunk):
	# Write our 10K chunk out to the serial port
	writeData(serialDataChunk);
	
	# See if the response we get back is good
	statusData = readData()
	


	
def readFile():
	global DEBUGMODE
	# Set our fileOffset so we know where we are in the file
	fileOffset = 0;
	# Get file length for percentage calculator
	fileLen = os.stat(gcodeFile).st_size;

	sendGCodeHeader("FileName",fileLen)
	# Loop until we run out of file
	while True:
		# Read our first chunk of file
		chunkOfFile = readChunk(fileOffset)
		serialDataChunk = generateSerialChunk(chunkOfFile)
		
		# In the main program, serial handling code and upload code goes here
		#sys.stdout.write(serialDataChunk)
		DEBUGMODE = 0
		sendSerialChunk(serialDataChunk)
	
	        if checkReturnedData("CheckSumOK:PN:0.",readData()) == 1:
	                errprint("Data doesn't match expected returned?!")

		DEBUGMODE = 1
		# Check to see if the chunk is smaller than 10236, if so, break.
		if len(chunkOfFile) != 10236:
			break

		# Update our offset point
		fileOffset = fileOffset + 10236
		
		# Let the user know how far we are through the file
		errprint("Processed {:0.2f}% of file.".format((fileOffset / float(fileLen) * 100)))


	errprint("Finished")



# Check to see if our serial port is open...
#print sport.isOpen();

writeData(unicode(MACHINE_INFO));
print readData()

# Returns two numbers?
writeData(unicode(MACHINE_LIFE));
print readData()


# Returns the following infor:
# unknown, unknown, unknown, unknown, Filament_Cart_Length, Filament_Remaining_Length, Extruder_Temp, Bed_Temp,unknown, unknown,unknown, unknown
writeData(unicode(EXTRUDER1_INFO));
print readData()


#Returns Status Info
writeData(unicode(STATUS_INFO));
print readData()


readFile()
