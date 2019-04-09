#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####################################################################################################

### Libraries ###

from sys import argv
from sys import exit

####################################################################################################

### Functions ###

def value_in_list_element(value, in_list, key):
    '''Check if provided list has any element with that key value.'''
    for element in in_list:
        if element[key] == value:
            return True
    return False


def file_read(file_path):
    '''Read file lines content and return them in a list.'''
    lines = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                if line is None:
                    continue
                if (line == "") or (line == "\r\n") or (line == "\r") or (line == "\n"):
                    continue
                line = line.replace("\r", "")
                line = line.replace("\n", "")
                lines.append(line)
    except Exception as e:
        print("Error when opening file \"{}\". {}".format(file_path, str(e)))
        finish(1)
    if len(lines) == 0:
        print("No topics found in file \"{}\".".format(file_path))
        finish(1)
    return lines

####################################################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    # Check if script is running with expected argument
    if len(argv) != 2:
        print("Error: This script needs 1 argument (file to read).")
        finish(1)
    # Read file lines
    print("Reading file lines...")
    lines = file_read(argv[1])
    # Check for occurrences
    try:
        counted_lines = []
        for line in lines:
            # Check if line is in any "text" attribute of any elemnt inside counted_lines list
            if not value_in_list_element(line, counted_lines, "text"):
                line_info = {"text":"", "num":""}
                line_info["text"] = line
                line_info["num"] = 1
                counted_lines.append(line_info)
            else:
                for element in counted_lines:
                    if line == element["text"]:
                        element["num"] = element["num"] + 1
        # Order list by number of occureences
        counted_lines = sorted(counted_lines, key=lambda k: k["num"])
        # Show result
        print("Lines and number of occurrences:")
        for element in counted_lines:
            print("[{}] {}".format(element["num"], element["text"]))
    except Exception as e:
        print("Error: {}".format(e))
        finish(1)
    finish(0)


def finish(return_code):
    '''Finish function.'''
    print("\nExit({}).\n\n".format(return_code))
    exit(return_code)

####################################################################################################

### Script Input - Main Script ###

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        finish(0)
