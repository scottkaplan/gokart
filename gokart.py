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
     'reg_name':'B',
     'is_reg':	 True, 
     'chan_req': True
     },

    'position_error_dead_band' : 
    {'command':	'position_error_dead_band',
     'reg_name':'d',
     'is_reg':	 True, 
     'chan_req': True
     },				

    'velocity_error_gain' : 
    {'command':	'velocity_error_gain',
     'reg_name':'D',
     'is_reg':	 True, 
     'chan_req': True
     },

    'position' : 
    {'command':	'position',
     'reg_name':'e',
     'is_reg':	 True, 
     'chan_req': True
     },

    'back_emf_factor' : 
    {'command':	'back_emf_factor',
     'reg_name':'E',
     'is_reg':	 True, 
     'chan_req': True
     },

    'input_factor' : 
    {'command':	'input_factor',
     'reg_name':'F',
     'is_reg':	 True, 
     'chan_req': True
     },

    'integral_error_gain' : 
    {'command':	'integral_error_gain',
     'reg_name':'l',
     'is_reg':	 True, 
     'chan_req': True
     },

    'input_select' : 
    {'command':	'input_select',
     'reg_name':'j',
     'is_reg':	 True, 
     'chan_req': True
     },

    'feedback_select' : 
    {'command':	'feedback_select',
     'reg_name':'J',
     'is_reg':	 True, 
     'chan_req': True
     },

    'position_limit' : 
    {'command':	'position_limit',
     'reg_name':'L',
     'is_reg':	 True, 
     'chan_req': True
     },

    'minimum_drive' : 
    {'command':	'minimum_drive',
     'reg_name':'M',
     'is_reg':	 True, 
     'chan_req': True
     },

    'mode' : 
    {'command':	'mode',
     'reg_name':'m',
     'is_reg':	 True, 
     'chan_req': True
     },

    'position_set_point' : 
    {'command':	'position_set_point',
     'reg_name':'p',
     'is_reg':	 True, 
     'chan_req': True
     },

    'position_error_gain' : 
    {'command':	'position_error_gain',
     'reg_name':'P',
     'is_reg':	 True, 
     'chan_req': True
     },

    'servo_loop_rate' : 
    {'command':	'servo_loop_rate',
     'reg_name':'r',
     'is_reg':	 True, 
     'chan_req': True
     },

    'power_slew' : 
    {'command':	'power_slew',
     'reg_name':'s',
     'is_reg':	 True, 
     'chan_req': True
     },

    'torque_set_point' : 
    {'command':	'torque_set_point',
     'reg_name':'t',
     'is_reg':	 True, 
     'chan_req': True
     },

    'torque_limit' : 
    {'command':	'torque_limit',
     'reg_name':'T',
     'is_reg':	 True, 
     'chan_req': True
     },				

    'unit_amount_for_manual_move' : 
    {'command':	'unit_amount_for_manual_move',
     'reg_name':'u',
     'is_reg':	 True, 
     'chan_req': True
     },

    'unit_amount_for_minimum_move' : 
    {'command':	'unit_amount_for_minimum_move',
     'reg_name':'U',
     'is_reg':	 True, 
     'chan_req': True
     },

    'velocity_set_point' : 
    {'command':	'velocity_set_point',
     'reg_name':'v',
     'is_reg':	 True, 
     'chan_req': True
     },

    'velocity_limit' : 
    {'command':	'velocity_limit',
     'reg_name':'V',
     'is_reg':	 True, 
     'chan_req': True
     },

    'baud' : 
    {'command':	'baud',
     'reg_name':'b',
     'is_reg':	 True, 
     'chan_req': False
     },

    'user_interface_mode' : 
    {'command':	'user_interface_mode',
     'reg_name':'l',
     'is_reg':	 True, 
     'chan_req': False
     },

    'compatible_preset' : 
    {'command':	'compatible_preset',
     'reg_name':'Q',
     'is_reg':	 True, 
     'chan_req': False
     },

    'write_load_values_eeprom' : 
    {'command':	'write_load_values_eeprom',
     'reg_name':'w',
     'is_reg':	 True, 
     'chan_req': False
     },

    'pwm_drive' : 
    {'command':	'pwm_drive',
     'reg_name':'d',
     'is_reg':	 False, 
     'chan_req': False
     },

    'encoder_count' : 
    {'command':	'encoder_count',
     'reg_name':'e',
     'is_reg':	 False, 
     'chan_req': False
     },

    'print_paramaters' : 
    {'command':	'print_paramaters',
     'reg_name':'p',
     'is_reg':	 False, 
     'chan_req': False
     },

    'reset_servo' : 
    {'command':	'reset_servo',
     'reg_name':'r',
     'is_reg':	 False, 
     'chan_req': False
     },

    'streaming_parameters' : 
    {'command':	'streaming_parameters',
     'reg_name':'S',
     'is_reg':	 False, 
     'chan_req': False
     },

    'temperature' : 
    {'command':	'temperature',
     'reg_name':'t',
     'is_reg':	 False, 
     'chan_req': False
     },	

    'velocity' : 
    {'command':	'velocity',
     'reg_name':'v',
     'is_reg':	 False, 
     'chan_req': False
     },			
    }

def good_channel (channel):
    return channel == 0 or channel == 1 or channel == 2

def good_mode (mode):
    return mode == "get" or mode == "set" or mode == "actual"

def createCtrlStr(parms):
    # Take a dictionary with the keys:
    #   cmd, mode, channel, value
    # and creates a string of the form
    #   @<channel>['g'|'s'|'a']<register><value>

    cmd = parms['cmd']
    # cmd_parms contains the meta info for cmd
    cmd_parms = command_map[cmd]
    if (cmd_parms == None):
        return "Bad Command", False

    if (cmd_parms['is_reg'] == False):
        # This is not a register command
        # Just send the string for this command
        return False, cmd_parms['reg_name']

    # if we fall thru to here, we have a register command
    ctrl_str = '@'

    if (cmd_parms['chan_req']):
        if (parms['channel']):
            channel = parms['channel']
            if (good_channel (channel)):
                ctrl_str += parms['channel']
            else:
                return "bad channel %s" % channel, False
        else:
            return "no channel", False
    else:
        # have to include a placeholder for channel
        ctrl_str += '0'

    if (parms['mode']):
        mode = parms['mode']
        if (not good_mode(mode)):
            return "bad mode '%s'" % mode, False
        # append the first char of the mode to the control str
        ctrl_str += mode[0]
    else:
        return "no mode", False

    if (cmd_parms['reg_name']):
        ctrl_str += cmd_parms['reg_name']
    else:
        return "no register name", False

    return False, ctrl_str

def sendCtrlStr(str):
    # send str to the controller (serial port)
    # and return the string that the controller sends back

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
        return False, response[0]
    else:
        return False, "\n".join(response)

def parseCmd(cmd_str):
    # takes a string of the form:
    #   <cmd> [<mode>] [<channel>] [<value>]
    #     where mode ::= 'get' | 'set' | 'actual' 
    #           channel ::= 0 | 1 | 2
    # and returns a dictionary
    # containing the parameters needed to call kart_api

    if (len(cmd_str)==0):
        return "No command", False

    parms = cmd_str.split()

    cmd = parms.pop(0)

    # cmd_parms contains the meta info for cmd
    cmd_parms = command_map[cmd]
    if (cmd_parms == None): return "bad command", False

    # result is the dictionary that can be passed to kart_api
    result = {}
    result['cmd'] = cmd

    if (cmd_parms['is_reg'] == False):
        # if this is not a register command, we're done
        return False, parms

    mode = parms.pop(0)
    if (not good_mode (mode)): return "bad mode", False
    result['mode'] = mode

    if (cmd_parms['chan_req']):
        channel = parms.pop(0)
        if (channel == None): return "no channel", False
        if (good_channel (channel)):
            result['channel'] == channel

    if (mode == 'set'):
        # value is only used for register set commands
        value = parms.pop(0)
        if (value == None): return "No Value", False
        result['value'] = value

    return False, result


def cli(str):
    err, api_parms = parseCmd(str)
    if (err): return err, False

    err, result = kart_api (api_parms)
    if (err): return err, False

    return False, result

def kart_api(parms):
    err,cmd_str = createCtrlStr(parms)
    if (err): return err, False

    err,result = sendCtrlStr(cmd_str)
    if (err): return err, False

    return False, result

def init():
    global radio
    radio = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=0.1)
    radio.parity = serial.PARITY_NONE
    radio.stopbits = serial.STOPBITS_ONE
    radio.xonxoff = False
    radio.rtscts = False
    radio.dsrdtr = False
    try:
        radio.open()
    except Exception, e:
        return "error opening serial port:" + str(e)

    global pp
    pp = pprint.PrettyPrinter(indent=2)

    return

def expect (cmd, expected_err, expected_result):
    print "Running command '%s'" % cmd
    err, result = cli(cmd)

    if (expected_err):
        print "\tExpect error '%s'" % expected_err
        if (err):
            if (err == expected_err):
                print "\tPassed"
            else:
                print "\tFailed: Got error '%s'" % err
        elif (result):
            print "\tFailed: Got result '%s'" % result

    if (expected_result):
        print "\tExpect result '%s'" % expected_result
        if (result):
            if (result == expected_result):
                print "\tPassed"
            else:
                print "\tFailed: Got result '%s'" % result
        elif (err):
            print "\tFailed: Got error '%s'" % err
    return

def test ():
    expect("baud get", False, "5")
    expect("", "No command", False)
    return

def main ():
    err = init()
    if (err): return err, False

    test()

main()
