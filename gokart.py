#!/usr/bin/python

import serial
import time
import pprint
import binascii
import string
import re

command_map = {
    'brake' : 
    {'command':	'brake',
     'value':	'B',
     'is_reg':	 True, 
     'chan_req': True
     },

    'position_error_dead_band' : 
    {'command':	'position_error_dead_band',
     'value':	'd',
     'is_reg':	 True, 
     'chan_req': True
     },				

    'velocity_error_gain' : 
    {'command':	'velocity_error_gain',
     'value':	'D',
     'is_reg':	 True, 
     'chan_req': True
     },

    'position' : 
    {'command':	'position',
     'value':	'e',
     'is_reg':	 True, 
     'chan_req': True
     },

    'back_emf_factor' : 
    {'command':	'back_emf_factor',
     'value':	'E',
     'is_reg':	 True, 
     'chan_req': True
     },

    'input_factor' : 
    {'command':	'input_factor',
     'value':	'F',
     'is_reg':	 True, 
     'chan_req': True
     },

    'integral_error_gain' : 
    {'command':	'integral_error_gain',
     'value':	'l',
     'is_reg':	 True, 
     'chan_req': True
     },

    'input_select' : 
    {'command':	'input_select',
     'value':	'j',
     'is_reg':	 True, 
     'chan_req': True
     },

    'feedback_select' : 
    {'command':	'feedback_select',
     'value':	'J',
     'is_reg':	 True, 
     'chan_req': True
     },

    'position_limit' : 
    {'command':	'position_limit',
     'value':	'L',
     'is_reg':	 True, 
     'chan_req': True
     },

    'minimum_drive' : 
    {'command':	'minimum_drive',
     'value':	'M',
     'is_reg':	 True, 
     'chan_req': True
     },

    'mode' : 
    {'command':	'mode',
     'value':	'm',
     'is_reg':	 True, 
     'chan_req': True
     },

    'position_set_point' : 
    {'command':	'position_set_point',
     'value':	'p',
     'is_reg':	 True, 
     'chan_req': True
     },

    'position_error_gain' : 
    {'command':	'position_error_gain',
     'value':	'P',
     'is_reg':	 True, 
     'chan_req': True
     },

    'servo_loop_rate' : 
    {'command':	'servo_loop_rate',
     'value':	'r',
     'is_reg':	 True, 
     'chan_req': True
     },

    'power_slew' : 
    {'command':	'power_slew',
     'value':	's',
     'is_reg':	 True, 
     'chan_req': True
     },

    'torque_set_point' : 
    {'command':	'torque_set_point',
     'value':	't',
     'is_reg':	 True, 
     'chan_req': True
     },

    'torque_limit' : 
    {'command':	'torque_limit',
     'value':	'T',
     'is_reg':	 True, 
     'chan_req': True
     },				

    'unit_amount_for_manual_move' : 
    {'command':	'unit_amount_for_manual_move',
     'value':	'u',
     'is_reg':	 True, 
     'chan_req': True
     },

    'unit_amount_for_minimum_move' : 
    {'command':	'unit_amount_for_minimum_move',
     'value':	'U',
     'is_reg':	 True, 
     'chan_req': True
     },

    'velocity_set_point' : 
    {'command':	'velocity_set_point',
     'value':	'v',
     'is_reg':	 True, 
     'chan_req': True
     },

    'velocity_limit' : 
    {'command':	'velocity_limit',
     'value':	'V',
     'is_reg':	 True, 
     'chan_req': True
     },

    'baud' : 
    {'command':	'baud',
     'value':	'b',
     'is_reg':	 True, 
     'chan_req': False
     },

    'user_interface_mode' : 
    {'command':	'user_interface_mode',
     'value':	'l',
     'is_reg':	 True, 
     'chan_req': False
     },

    'compatible_preset' : 
    {'command':	'compatible_preset',
     'value':	'Q',
     'is_reg':	 True, 
     'chan_req': False
     },

    'write_load_values_eeprom' : 
    {'command':	'write_load_values_eeprom',
     'value':	'w',
     'is_reg':	 True, 
     'chan_req': False
     },

    'pwm_drive' : 
    {'command':	'pwm_drive',
     'value':	'd',
     'is_reg':	 False, 
     'chan_req': False
     },

    'encoder_count' : 
    {'command':	'encoder_count',
     'value':	'e',
     'is_reg':	 False, 
     'chan_req': False
     },

    'print_paramaters' : 
    {'command':	'print_paramaters',
     'value':	'p',
     'is_reg':	 False, 
     'chan_req': False
     },

    'reset_servo' : 
    {'command':	'reset_servo',
     'value':	'r',
     'is_reg':	 False, 
     'chan_req': False
     },

    'streaming_parameters' : 
    {'command':	'streaming_parameters',
     'value':	'S',
     'is_reg':	 False, 
     'chan_req': False
     },

    'temperature' : 
    {'command':	'temperature',
     'value':	't',
     'is_reg':	 False, 
     'chan_req': False
     },	

    'velocity' : 
    {'command':	'velocity',
     'value':	'v',
     'is_reg':	 False, 
     'chan_req': False
     },			
    }

def setupScreen():
    openscreen  = "Welcome to the GoKart Setup System. Please enter your command in the following syntax: get baud 0 val"
    
    pp.pprint(command_map)
    
    return openscreen

def createCtrlStr():

    serialcommand = ''
    mode = ''
    channel = ''
    controlcommand = ''
    value = ''

    parm[0]
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

    return

def sendCtrlStr(str):

    radio.write(str)
    radio.write("\r")

    # handle multi-line response
    response = []
    while True:
        line = radio.readline()

        # We're done when we see '>' on a line by itself
        if (line == ">"):
            break

        # lines come from the controller
        # beginning with '>' and \r\n terminated
        # Strip those
	line = line.replace(">","")
        line = line.replace("\r\n","")
        response.append(line)

    if (len(response) == 1):
        # If there is only one line,
        # don't use line termination
        return (response[0])
    else:
        return ("\n".join(response))

def runCmd(parms):
    err,cmd_str = createCtrlStr(parms)
    if (err):
        return err, False

    err,result = sendCtrlStr(cmd_str)
    if (err):
        return err, False

    return False, result

def parseCmd(textcommand):

    if(len(textcommand)==0):
        return "Missing A Command", False

    parm_idx = 0
    parms = textcommand.split()

    cmd = parms[parm_idx]
    parm_idx += 1

    cmd_parms = command_map[cmd]

    if(cmd_parms == None):
        return "Bad Command", False

    result = {}
    result['cmd'] = cmd

    if(cmd_parms['is_reg'] == False):
        return False, parms

    mode = parms[parm_idx]
    parm_idx += 1

    if (mode != "get" and mode != "set" and mode != "actual"):
        return "Bad Mode", False

    result['mode'] = mode

    if (cmd_parms['chan_req']):
        channel = parms[parm_idx]
        parm_idx += 1

        if(channel == None):
            return "no Channel", False
        if(channel == 0 or channel == 1 or channel == 2):
            result['channel'] == channel

    if (mode == 'set'):
        value = parms[parm_idx]
        parm_idx += 1

        if(value == None):
            return "No Value", False
        
        result['value'] = value

    return False, result


def runCli():
    print setupScreen()
    
    input = 1
    while 1:
        input = raw_input(">>")
        cli(input)

def cli(str):
    err, result = parseCmd(str)

    if(err):
        return err, False

    return False, result


def init():
    radio = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=0.1)

    radio.parity = serial.PARITY_NONE
    radio.stopbits = serial.STOPBITS_ONE
    radio.xonxoff = False
    radio.rtscts = False
    radio.dsrdtr = False

    global pp
    pp = pprint.PrettyPrinter(indent=2)

    try:
        radio.open()

    except Exception, e:
        print "error opening serial port:" + str(e)
        exit()

def main ():
    err = init()
    if(err):
        return err, False

    err, result  = cli("baud get")

    if(err):
        return err, False

    return False, result

err, result = main()

if(err):
    pp.pprint(err)

pp.pprint(result)
