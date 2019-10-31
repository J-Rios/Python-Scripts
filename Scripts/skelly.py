#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####################################################################################################

### Libraries ###

from sys import exit
from time import sleep
from traceback import format_exc
from signal import signal, SIGTERM, SIGINT

####################################################################################################

### Constants ###

TEXT_HELLO = "Hello World"

####################################################################################################

### Functions ###

def function_1():
    '''Function Description.'''
    print(TEXT_HELLO)


####################################################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    print("Setup")
    while True:
        try:
            function_1()
            sleep(1)
        except Exception as e:
            print("\n[ERROR] {}".format(format_exc()))
            finish(1)
    finish(0)


def finish(return_code):
    '''Finish function.'''
    print("\nAll resources released, exit({}).\n".format(return_code))
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
