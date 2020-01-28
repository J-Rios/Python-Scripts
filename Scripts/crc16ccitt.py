#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####################################################################################################

### Libraries ###

from sys import exit
from sys import argv as sys_argv
from traceback import format_exc
from signal import signal, SIGTERM, SIGINT

####################################################################################################

### Constants ###

FILE_NAME = sys_argv[0]
CRC16_CCITT_POLY = 0x8408

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
    print("You need to provide a file.")
    print("Example:")
    print("  python {} file.bin".format(FILE_NAME))


def crc16(data, poly, reverse=False):
    '''CRC-16-CCITT Algorithm'''
    crc = 0xFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    if reverse:
        crc = (crc << 8) | ((crc >> 8) & 0xFF)
    return crc & 0xFFFF

####################################################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    try:
        # Get provided file path argument
        argv = get_and_check_args()
        file_path = argv[0]
        # Read the file
        with open(file_path, "rb") as f:
            _bytes = f.read()
        # Get the CRC value and print it as hexadecimal string with leading zeros
        crc_value = crc16(_bytes, CRC16_CCITT_POLY)
        crc_value = "{0:#0{1}x}".format(crc_value, 6)
        print(crc_value)
    except Exception:
        print("\n[ERROR]\n{}".format(format_exc()))
        finish(1)
    finish(0)


def finish(return_code):
    '''Finish function.'''
    print("")
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

###########################################################
