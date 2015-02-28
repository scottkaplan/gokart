import serial
import time
import pprint
import binascii
import string
import re


command_map = {'brake' : 
				{'command':'brake',
				 'value':'B', 'is_reg': True, 
				 'channel_required': True},
			   'baud' : {'command':'baud','value':'b','is_reg': True, 'req_channel': True},
			   'inputcontrol' : {'command':'inputcontrol','value':'C'},
			   'copy' : {'command':'copy','value':'c'},
			   'channelmix' : {'command':'channelmix','value':'x'},
			   'drive' : {'command':'drive','value':'d'},
			   'slew' : {'command':'slew','value':'s'},
			   'save' : {'command':'save','value':'w'},
			   'localecho' : {'command':'localecho','value':'l'},
			   'ProportionalGain' : {'command':'ProportionalGain','value':'P'},
			   'servomode' : {'command':'servomode','value':'d'},
			   'controlinputselect' : {'command':'controlinputselect','value':'j'},
			   'parms' : {'command':'parms','value':'p'},

			}

def read_rfid_byte(n=1):
    if (n==1):
        b = radio.read
    else:
        b = radio.read(n)
    return b


def setupScreen():
    openscreen  = "Welcome to the GoKart Setup System. Please enter your command in the following syntax: get baud 0 val"
    
    pp.pprint(command_map)
    
    return openscreen
    
def interpretCommand(textcommand):
	serialcommand = ''
	
	mode = ''
	channel = ''
	controlcommand = ''
	value = ''
	

	parm = textcommand.split()
	
	for i in range(len(parm)):
		if i==0:
			mode = parm[0]
			if mode == "get":
				com_mode = "g"
			elif mode == "set":
				com_mode = "s"
			elif mode == "actual":
				com_mode = "a"

		elif i==1:
			controlcommand = parm[2]
			commanditem = command_map[controlcommand]
			finalcommand = commanditem['value']

		elif i==2:
			channel = parm[1]

		elif i==3:
			value = parm[3]
	
	serialcommand += '@'
	serialcommand += channel
	serialcommand += com_mode
	serialcommand += finalcommand
	serialcommand += value

	return serialcommand

def sendReceive(plaincommand):

	command = interpretCommand(plaincommand)
	pp.pprint("Command:" + command)
	radio.write(command)
	radio.write("\r")

	response_str = ""
	line = ""

	while True:

		line = radio.readline()
		
		if (line == ">"):
			break

		line = line.replace("\r\n","")

		response_str += line
	
	line = line.replace(">","")
	return(response_str)

radio = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=0.1)

print "Serial now available"

radio.parity = serial.PARITY_NONE
radio.stopbits = serial.STOPBITS_ONE
radio.xonxoff = False
radio.rtscts = False
radio.dsrdtr = False
pp = pprint.PrettyPrinter(indent=2)

try:
    radio.open()

except Exception, e:
    print "error opening serial port:" + str(e)
    exit()

if radio.isOpen():
    print "Port Set Up Complete"
    print setupScreen()
    
    input = 1
    while 1:
        input = raw_input(">>")
        command_response = sendReceive(input)
        pp.pprint(command_response)
else:
    print "cannot open serial port"
