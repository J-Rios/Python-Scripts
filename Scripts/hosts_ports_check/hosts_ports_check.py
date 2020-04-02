#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####################################################################################################

### Libraries ###

from os import path
from sys import exit
from time import sleep
from signal import signal, SIGTERM, SIGINT

from socket import *
from threading import *

####################################################################################################

### Constants ###

# Actual constant.py full path
SCRIPT_PATH = path.dirname(path.realpath(__file__))

# Files Path
F_HOSTS = SCRIPT_PATH + "/hosts.txt"
F_HOSTS_OPEN = SCRIPT_PATH + "/results_hosts_open.txt"

# Ports to check
#PORTS = list(range(65536))
#PORTS = [22, 23, 80, 443, 1883, 1554]
PORTS = [21, 22, 23, 24, 25, 26, 53, 80, 81, 110, 111, 113, 135, 139, 143, 179, 199, 443, 445, \
        465, 514, 515, 548, 554, 587, 646, 993, 995, 1025, 1026, 1027, 1433, 1554, 1720, 1723, \
        1883, 2000, 2001, 3306, 3389, 5060, 5666, 5900, 6001, 8000, 8008, 8080, 8443, 8883, 8888, \
        10000, 11884, 32768, 49152, 49154]

####################################################################################################

### Globals ###

# List open ports
l_open_ports = []

####################################################################################################

### Functions ###

def file_write_line(file_path, line):
    '''Write a file line.'''
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("{}\n".format(line))
    except Exception as e:
        print("Error when opening file \"{}\". {}".format(file_path, str(e)))


def file_read_lines(file_path):
    '''Read file lines content and return them in a list.'''
    l_lines = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                if line is None:
                    continue
                line = line.replace("\r", "")
                line = line.replace("\n", "")
                if (line == ""):
                    continue
                l_lines.append(line)
    except Exception as e:
        print("Error when opening file \"{}\". {}".format(file_path, str(e)))
    return l_lines


def check_port(host, port):
    global l_open_ports
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
        l_open_ports.append(port)
    except:
        pass
    finally:
        sock.close()


def scan_ports(host, ports):
    global l_open_ports
    try:
        host_ip = gethostbyname(host)
    except:
        print("Cannot resolve {}: Unknown host".format(host))
        return
    #try:
    #    host_name = gethostbyaddr(host_ip)
    #    print("Hostname is {}".format(host_name[0]))
    #except:
    #    pass
    l_threads = []
    for port in ports:
        t = Thread(target=check_port, args=(host_ip, int(port)))
        t.start()
        l_threads.append(t)
    for t in l_threads:
        t.join()
    if len(l_open_ports) == 0:
        print("All ports are closed in {}.".format(host_ip))
    else:
        file_write_line(F_HOSTS_OPEN, host)
        print("Open ports in {} -".format(host_ip), end = '')
        for open_port in l_open_ports:
            print(" {}".format(open_port), end = '')
        print("")
        l_open_ports.clear()
    print("")

####################################################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    print("")
    print("Reading list of hosts from {}...".format(F_HOSTS))
    l_hosts = file_read_lines(F_HOSTS)
    if len(l_hosts) == 0:
        print("No hosts in {}, exiting.".format(F_HOSTS))
        finish(1)
    print("Read success.")
    print("")
    print("List of host to scan:")
    for host in l_hosts:
        print(host)
    print("")
    setdefaulttimeout(1)
    for host in l_hosts:
        scan_ports(host, PORTS)
    finish(0)


def finish(return_code):
    '''Finish function.'''
    print("\n All resources released, exit({}).\n".format(return_code))
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

