#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Description: Encode a given hexadecimal data string into BASE64

####################################################################################################

### Libraries ###

from sys import exit
from sys import argv as sys_argv
from time import sleep
from traceback import format_exc
from signal import signal, SIGTERM, SIGINT
from base64 import b64encode

####################################################################################################

### Functions ###

def get_and_check_args():
    '''Function that get and check provided script arguments.'''
    argv = sys_argv
    argc = len(sys_argv)-1
    if argc == 0:
        print_script_usage()
        finish(1)
    return argv[1:]


def print_script_usage():
    '''Function that shows script usage help.'''
    print("")
    print("You need to provide a valid hexadecimal string to be encoded.")
    print("Example:")
    print("  python hextob64.py c2889d8f")


def hex_add_left_zero_padding(input_str):
    '''Function that append left padding zero if provided hax string is odd.'''
    output_str = input_str
    if (len(input_str) % 2) != 0:
        output_str = "0{}".format(input_str)
    return output_str


def string_is_hex(input_str):
    '''Function that check if provided string is a valid hexadecimal data.'''
    try:
        int(input_str, 16)
        return True
    except Exception as e:
        return False

####################################################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    try:
        argv = get_and_check_args()
        hex_string = argv[0]
        hex_string = hex_add_left_zero_padding(hex_string)
        if not string_is_hex(hex_string):
            print("\nProvided string is not a valid hexadecimal data.")
            print("Provided string: {}".format(hex_string))
            print_script_usage()
            finish(1)
        hex_string = bytearray.fromhex(hex_string)
        b64_string = b64encode(hex_string)
        b64_string = b64_string.decode("utf-8")
        print(b64_string)
    except Exception as e:
        print("\n[ERROR] {}".format(format_exc()))
        finish(1)
    finish(0)


def finish(return_code):
    '''Finish function.'''
    #print("\nAll resources released, exit({}).\n".format(return_code))
    exit(return_code)

####################################################################################################

### Termination signals handler for program process ###

def signal_handler(signal, frame):
    '''Termination signals (SIGINT, SIGTERM) handler for program process'''
    finish(1)


# Signals attachment
signal(SIGTERM, signal_handler) # SIGTERM (kill pid) to signal_handler
signal(SIGINT, signal_handler)  # SIGINT (Ctrl+C) to signal_handler

####################################################################################################

### Script Input - Main Script ###

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        finish(0)
