#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    libsetup.py
Description:
    Parse a "libraries.txt" file to get/update all required project library
    dependencies from remote Git repositories at a specific Git Tag/Commit.
    The libraries will be added to a ".libdeps" directory of the project by
    git clone and git checkout to specified Git tag/commit/branch of each
    library.
    Requirement:
      python3 -m pip install GitPython
Author:
    Jose Miguel Rios Rubio
Creation date:
    18/04/2024
Last modified date:
    18/04/2024
Version:
    1.0.0
'''

###############################################################################
# Standard Libraries
###############################################################################

# Logging Library
import logging

# System Operations Library
from os import path as os_path
from os import makedirs as os_makedirs

# System Library
from sys import argv as sys_argv
from sys import exit as sys_exit

# Error Traceback Library
from traceback import format_exc


###############################################################################
# Third-Party Libraries
###############################################################################

from git import Repo, GitCommandError


###############################################################################
# Logger Setup
###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


###############################################################################
# Constants
###############################################################################

# Libraries Directory
LIBDEPS_DIR = ".libdeps"


###############################################################################
# Auxiliary Elements
###############################################################################

class RC():
    '''Program Result Code.'''
    OK = 0
    ERROR = 1
    MISSING_ARGS = 2
    FILE_NOT_FOUND = 3
    INVALID_DATA = 4

class Library():
    '''Library information.'''
    name = ""
    url = ""
    tag = ""


###############################################################################
# Auxiliary Functions
###############################################################################

def make_dir(dir_path: str):
    '''
    Create all parents directories from provided path (mkdir -p $dir_path).
    '''
    success = False
    try:
        if not os_path.exists(dir_path):
            os_makedirs(dir_path, 0o775)
        success = True
    except Exception:
        logger.error(format_exc())
        logger.error("Can't create directories for %s.", dir_path)
    return success


def file_read_text(file_path):
    '''Read all text file content and return it in a string.'''
    # Check if file doesnt exists
    if not os_path.exists(file_path):
        logger.error("File %s not found.", file_path)
        return None
    # File exists, so open and read it
    read = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            read = f.read()
    except Exception:
        logger.error(format_exc())
        logger.error("Can't open and read file %s.", file_path)
        return None
    return read


def git_repo_open(git_repo_name, local_path):
    '''
    Git access to local repository.
    '''
    success = False
    try:
        Repo(local_path)
        success = True
    except GitCommandError as e:
        logger.error(f"Git Repo Open fail")
        logger.error(f"Repository: {git_repo_name}")
        logger.error(f"Local Path: {local_path}")
        logger.error(f"{e}")
    return success


def git_clone(url, local_path):
    '''
    Git clone a repository.
    '''
    git_repo = None
    try:
        git_repo = Repo.clone_from(url, local_path)
    except GitCommandError as e:
        logger.error(f"Git Clone fail")
        logger.error(f"Repository: {url}")
        logger.error(f"Local Path: {local_path}")
        logger.error(f"{e}")
    return git_repo


def git_checkout(git_repo_name, git_repo, tag):
    '''
    Git checkout a repository to specified tag/commit/branch.
    '''
    success = False
    try:
        git_repo.git.checkout(tag)
        success = True
    except GitCommandError as e:
        logger.error("Git checkout fail")
        logger.error(f"Repository: {git_repo_name}")
        logger.error(f"Checkout: {tag}")
        logger.error(f"{e}")
    return success


def show_bad_lib(bad_lib, line_n):
    logger.error("Invalid/Malformed Library found in libraries.txt")
    logger.error("%d: %s", line_n, bad_lib)


def parse_libraries(lib_data):
    '''
    Parse, validate and get Libraries from libraries.txt file data.
    '''
    libraries = []
    # Check if there is any library data
    if (lib_data is None) or (lib_data == ""):
        return None
    # DOS to UNIX EOLs
    lib_data = lib_data.replace("\r\n", "\n")
    # Iterate over each line detecting which ones must be used/ignored
    lib_data = lib_data.split("\n")
    for i in range(len(lib_data)-1):
        line = lib_data[i]
        # Ignore empty and comment lines
        if (len(line) == 0) or (line[0] == "#"):
            continue
        # Check if Library line is malformed/invalid
        if " == " not in line:
            show_bad_lib(line, i)
            return None
        lib = line.split(" == ")
        # Get Library info
        library = Library()
        library.name = lib[0].split("/")[-1][:-4]
        library.url = lib[0]
        library.tag = lib[1]
        # Check if URL is valid
        if "/" not in library.url:
            show_bad_lib(line, i)
            return None
        if len(library.url) < len("git@X.git"):
            show_bad_lib(line, i)
            return None
        # Store valid Library in list
        libraries.append(library)
    return libraries


def setup_libraries(libraries, lib_dir):
    '''
    Get/Update project libraries and skip the ones that are already setup.
    '''
    if not make_dir(lib_dir):
        return False
    for library in libraries:
        lib_dir = f"{lib_dir}/{library.name}"
        # If Library doesn't exists, clone it
        if not os_path.isdir(lib_dir):
            git_repo = git_clone(library.url, lib_dir)
        else:
            git_repo = git_repo_open(library.name, lib_dir)
        if git_repo is None:
            return False
        if not git_checkout(library.name, git_repo, library.tag):
            return False
    return True


###############################################################################
# Main Function
###############################################################################

def main(argc, argv):
    '''
    Main Function.
    '''
    # Check and parse input arguments
    if argc == 0:
        print("You need to provide a libraries.txt file:")
        print("  python3 libsetup.py libraries.txt")
        return RC.MISSING_ARGS
    libs_file = argv[0]
    libs_data = file_read_text(libs_file)
    if libs_data is None:
        return RC.FILE_NOT_FOUND
    libraries = parse_libraries(libs_data)
    if libraries is None:
        return RC.INVALID_DATA
    lib_file_dir_path = os_path.dirname(os_path.realpath(libs_file))
    libraries_dir = f"{lib_file_dir_path}/{LIBDEPS_DIR}"
    if not setup_libraries(libraries, libraries_dir):
        return RC.ERROR
    return RC.OK


###############################################################################
# Exit Function
###############################################################################

def program_exit(return_code):
    '''
    Program exit function.
    '''
    logger.debug("Application Exit (%d)", return_code)
    sys_exit(return_code)


###############################################################################
# Runnable Main Script Detection
###############################################################################

if __name__ == "__main__":
    return_code = main(len(sys_argv) - 1, sys_argv[1:])
    program_exit(return_code)
