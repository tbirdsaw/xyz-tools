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
TIMEOUT = 0.1	# We want to block the program until we get a response back
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
SEND_FIRMWARE = MACHINE_INFO + '3'
SEND_FILE = MACHINE_INFO + '4'

#ReturnedStrings:
#SEND_FILE_RESP1 = "OFFLINE_OK" + "\n"

#Open our file
gcode = os.fdopen(os.open(gcodeFile,os.O_RDONLY))

#Open serial port
if SERIALENABLE == 1:
	sport = serial.Serial(DEVICE,baudrate=BAUDRATE,timeout=TIMEOUT,xonxoff=1,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE);
	# Need a raw IO for sending data
	rsio = io.BufferedRWPair(sport,sport)
	# For our return statements and such, note that the EOL is just Linefeed character (0x0a)
	sio = io.TextIOWrapper(rsio,newline='\n')

def errprint(message):
	if DEBUGMODE >= 1:
		sys.stderr.write(message + "\n");

def writeData(data):
	errprint("Sending: " + data)
	if SERIALENABLE == 1:
		sio.write(data)
		sio.flush()

def rawWriteData(data):
	errprint("RAW-Sending: " + data)
	if SERIALENABLE == 1:
		rsio.write(data)
		rsio.flush()

def readData():
	time.sleep(1)
	returnData = ''
	if SERIALENABLE == 1:
		returnData = sio.read()
	else:
		returnData = "Serial Disabled"

	errprint("Received: " + returnData)

	return returnData;

def checkReturnedData(expectedData,returnedData):
	errprint("Is expected: " + expectedData + " equal to " + returnedData + " ?")
	if expectedData == returnedData:
		errprint("Returned Data expected!")
		return 0
	else:
		errprint("Returned Data not expected!")
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

	#Check to see if the length is less than 10236. If so, add our special end value (0x86)
#	if len(byteChunk) < 10236 :
#		errprint("Last chunk of data... added EOF marker")
#		ckStream = ckStream + bytearray.fromhex('86')
	

	errprint("Checksum for chunk is: " + str(checkData));

	# Concatenate the two byte arrays and return
	return dataStream + ckStream

# This sends our required? header
def sendGCodeHeader(fileName,fileLen):
	# Write out our predetermined string
	#writeData(unicode(SEND_FILE))
	#readData()

	#flush buffers
	#sio.flush()
	
	rawWriteData("M1:{:s},{:d},1.3.49,EE1_OK,EE2_OK".format(fileName,fileLen))
	#time.sleep(5)
	returnData = readData();
	if checkReturnedData("OFFLINE_OK",returnData.strip()) == 1:
		errprint("Data doesn't match expected returned?!")
		#sys.exit("Dying because things don't match up!")
	#time.sleep(1)	

# This sends the GCode chunk and makes sure we get a OK response back.
def sendSerialChunk(serialDataChunk):
	# Write our 10K chunk out to the serial port
	rawWriteData(serialDataChunk);
	rsio.flush()
	# See if the response we get back is good
#	statusData = readData()
	


	
def readFile():
	global DEBUGMODE
	# Set our fileOffset so we know where we are in the file
	fileOffset = 0;
	# Get file length for percentage calculator
	fileLen = os.stat(gcodeFile).st_size;

	sendGCodeHeader("MyTest",fileLen)
	# Loop until we run out of file
	while True:
		# Read our first chunk of file
		chunkOfFile = readChunk(fileOffset)
		serialDataChunk = generateSerialChunk(chunkOfFile)
		
		# In the main program, serial handling code and upload code goes here
		#sys.stdout.write(serialDataChunk)
		DEBUGMODE = 1
		sendSerialChunk(serialDataChunk)
		DEBUGMODE = 1

		returnedData = readData();
	
	        if checkReturnedData("CheckSumOK",returnedData.strip()) == 1:
	                
			errprint("Data doesn't match expected returned?!")
			#sys.exit("Dying because of unexpected data!")

		# Check to see if the chunk is smaller than 10236, if so break because we're done uploading.
		if len(chunkOfFile) != 10236:
			break

		# Update our offset point
		fileOffset = fileOffset + 10236
		
		# Let the user know how far we are through the file
		errprint("Sent {:0.2f}% of file.".format((fileOffset / float(fileLen) * 100)))


	rsio.flush()
	sport.close()
	errprint("Finished")

def sendfileToPrinter():
	# Notify our printer that we want to send it a file.
	writeData(unicode(SEND_FILE));
	returnedData = readData();
	if checkReturnedData("OFFLINE_OK",returnedData.strip()) == 1:
		errprint("Data doesn't match expected returned?!")
		sys.exit("Dying because of unexpected returned data!")
	readFile()

# Check to see if our serial port is open...
#print sport.isOpen();

writeData(unicode(MACHINE_INFO));
readData()

#print "Sleeping 5 seconds..."
#time.sleep(5)

# Returns two numbers?
writeData(unicode(MACHINE_LIFE));
readData()


# Returns the following infor:
# unknown, unknown, unknown, unknown, Filament_Cart_Length, Filament_Remaining_Length, Extruder_Temp, Bed_Temp,unknown, unknown,unknown, unknown
writeData(unicode(EXTRUDER1_INFO));
readData()


#Returns Status Info
writeData(unicode(STATUS_INFO));
readData()

#print "Sleeping 5 seconds..."
#time.sleep(5)


#readFile()
sendfileToPrinter()
