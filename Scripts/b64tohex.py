#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Description: Decode a given BASE64 data string into hexadecimal

####################################################################################################

### Libraries ###

from sys import exit
from sys import argv as sys_argv
from time import sleep
from traceback import format_exc
from signal import signal, SIGTERM, SIGINT
from base64 import b64decode

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
    print("You need to provide a valid BASE64 string.")
    print("Example:")
    print("  python b64tohex.py woidjw==")

####################################################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    try:
        argv = get_and_check_args()
        b64_string = argv[0]
        b64_string = "{}==".format(b64_string) # Add padding to avoid fail if not present
        hex_string = b64decode(b64_string)
        hex_string = hex_string.hex()
        print(hex_string)
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
