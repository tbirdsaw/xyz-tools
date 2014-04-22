#!/usr/bin/python

import serial;
import io; #Suggested to handle LineFeeds and buffering and whatnot

# Hardcode parameters for now
# Parameters set for XYZ from watching the traffic
#DEVICE = "/dev/ttyACM0"
DEVICE='/dev/ttyACM0'
TIMEOUT = 1
BAUDRATE = 115200

#Known Commands
MACHINE_INFO = 'XYZ_@3D:'
MACHINE_LIFE = MACHINE_INFO + '5'
EXTRUDER1_INFO = MACHINE_INFO + '6'
EXTRUDER2_INFO = MACHINE_INFO + '7'
STATUS_INFO = MACHINE_INFO + '8'
SEND_FILE = MACHINE_INFO + '4'


#Load a file
filename = "test.gcode"
gcode = open(filename, "r")

#Open serial port
sport = serial.Serial(DEVICE,baudrate=BAUDRATE,timeout=TIMEOUT,xonxoff=1,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE);
sio = io.TextIOWrapper(io.BufferedRWPair(sport,sport),newline='\n')

def writeData(data):
	sio.write(data)

def readData():
	return sio.readline()

def readFile():
	for line in gcode:
		print '.' + line.strip(),


# Open our serialport

print sport.isOpen();

writeData(unicode(MACHINE_INFO));
sio.flush()
print sio.read()

# Returns two numbers?
writeData(unicode(MACHINE_LIFE));
sio.flush()
print sio.read()


# Returns the following infor:
# unknown, unknown, unknown, unknown, Filament_Cart_Length, Filament_Remaining_Length, Extruder_Temp, Bed_Temp,unknown, unknown,unknown, unknown
writeData(unicode(EXTRUDER1_INFO));
sio.flush()
print sio.read()


#Returns Status Info
writeData(unicode(STATUS_INFO));
sio.flush()
print sio.read()


#Send a test file?
#writeData(unicode(SEND_FILE));
#sio.flush()
#print sio.read()

readFile()

