#!/usr/bin/python
# Rough code to communicate with the DaVinci Printer. 
# Note: I intend to clean this up later; this was a proof of concept to see if I could talk with the printer



import serial;
import io; #Suggested to handle LineFeeds and buffering and whatnot

# Hardcode parameters for now
# Parameters set for XYZ from watching the traffic
#DEVICE = "/dev/ttyACM0"
DEVICE='/dev/ttyACM0'
TIMEOUT = 0.1
BAUDRATE = 115200

#Known Commands
MACHINE_INFO = 'XYZ_@3D:'
MACHINE_LIFE = MACHINE_INFO + '5'
EXTRUDER1_INFO = MACHINE_INFO + '6'
EXTRUDER2_INFO = MACHINE_INFO + '7'
STATUS_INFO = MACHINE_INFO + '8'
SEND_FILE = MACHINE_INFO + '4'

#Open serial port
sport = serial.Serial(DEVICE,baudrate=BAUDRATE,timeout=TIMEOUT,xonxoff=1,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE);
sio = io.TextIOWrapper(io.BufferedRWPair(sport,sport),newline='\n')

def writeData(data):
	sio.write(data)

def readData():
	return sio.readline()


# Open our serialport

print sport.isOpen();

# Returns model, serial number, etc...
writeData(unicode(MACHINE_INFO));
sio.flush()
print sio.read()

# Returns two numbers which indicate some sort of life
writeData(unicode(MACHINE_LIFE));
sio.flush()
print sio.read()


# Returns the following info:
# unknown, unknown, unknown, unknown, Filament_Cart_Length, Filament_Remaining_Length, Extruder_Temp, Bed_Temp,unknown, unknown,unknown, unknown
writeData(unicode(EXTRUDER1_INFO));
sio.flush()
print sio.read()


#Returns Status Info
writeData(unicode(STATUS_INFO));
sio.flush()
print sio.read()

