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
CRC32_POLY = 0x04c11db7

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
    print("")


def make_word(b, poly):
    '''Create a word from a byte.'''
    c = b << 24
    for _ in range(8):
        if c & 0x80000000 :
            c = (c << 1 & 0xFFFFFFFF) ^ poly
        else:
            c = c << 1 & 0xFFFFFFFF
    return c


def crc32b(data, poly, init = 0xFFFFFFFF, xorout = 0x00):
    crc = init
    for i in range(len(data)):
        crc = (crc << 8 & 0xFFFFFFFF) ^ make_word(((crc >> 24) ^ data[i]) & 0xFF, poly)
    crc = crc ^ xorout
    return crc

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
        # Get the CRC-32 value and print it as hexadecimal string with leading zeros
        crc_value = crc32b(_bytes, CRC32_POLY, 0x00, 0x00)
        crc_value = "{:08X}".format(crc_value)
        crc_value = "0x{}".format(crc_value.upper())
        print(crc_value)
    except Exception:
        print("\n[ERROR]\n{}".format(format_exc()))
        finish(1)
    finish(0)


def finish(return_code):
    '''Finish function.'''
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
