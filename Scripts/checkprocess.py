#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####################################################################################################

### Libraries ###

from psutil import pids, pid_exists, process_iter, Process
from sys import argv, exit
from time import sleep
from traceback import format_exc
from signal import signal, SIGTERM, SIGINT

####################################################################################################

### Constants ###


####################################################################################################

### Functions ###

def show_process_pid_name():
    '''Show a list of process PID and names.'''
    process_ids = pids()
    for pid in process_ids:
        p = Process(pid)
        print("{} - {} {}".format(p.pid, p.name(), p.cmdline()))

####################################################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    try:
        if len(argv) < 2:
            show_process_pid_name()        
            print("\nYou need to provided a process PID.")
            finish(1)
        pid = int(argv[1])
        if not pid_exists(pid):
            print("\nPID not found.")
            finish(1)
        p = Process(pid)
        print("Proccess: {} ({})".format(p.name(), p.pid))
        print("----------------------------------------------")
        print("Files opens:")
        files = p.open_files()
        for f in files:
            print(f.path)
        print("----------------------------------------------")
        print("Network Connections:")
        connections = p.connections()
        printed_connections = []
        for c in connections:
            if hasattr(c, "laddr"):
                laddr = c.laddr
                if hasattr(laddr, "ip") and hasattr(laddr, "port"):
                    if laddr not in printed_connections:
                        printed_connections.append(laddr)
                        print("Local - {}:{}".format(laddr.ip, laddr.port))
            if hasattr(c, "raddr"):
                raddr = c.raddr
                if hasattr(raddr, "ip") and hasattr(raddr, "port"):
                    if raddr not in printed_connections:
                        printed_connections.append(raddr)
                        print("Remote - {}:{}".format(raddr.ip, raddr.port))
                print("")
        printed_connections.clear()
    except Exception:
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
