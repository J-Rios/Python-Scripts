#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script:
    TSjson.py
Description:
    Thread-Safe json files read/write library.
Author:
    Jose Rios Rubio
Creation date:
    20/07/2017
Last modified date:
    01/02/2019
Version:
    1.2.1
'''

####################################################################################################

### Imported modules ###

from os import stat, path, remove, makedirs
from json import load as json_load
from json import dump as json_dump
from threading import Lock
from collections import OrderedDict
from sys import version_info

####################################################################################################

### Class ###

class TSjson(object):
    '''Thread-Safe json files read/write library.'''

    def __init__(self, file_name):
        '''Class Constructor'''
        self.lock = Lock()
        self.file_name = file_name


    def read(self):
        '''Read json file.'''
        # Return an empty dictionary if file doesnt exists or is empty
        if not path.exists(self.file_name):
            return {}
        if not stat(self.file_name).st_size:
            return {}
        # The file exists and has content, try to open and read it
        read = {}
        try:
            self.lock.acquire()
            if self._is_running_with_py3():
                with open(self.file_name, "r", encoding="utf-8") as f:
                    read = json_load(f, object_pairs_hook=OrderedDict)
            else:
                with open(self.file_name, "r") as f:
                    read = json_load(f, object_pairs_hook=OrderedDict)
        except Exception as e:
            print("Error - Can't open and read file {} [{}].".format(self.file_name, str(e)))
            read = None
        finally:
            self.lock.release()
        return read


    def write(self, data=None):
        '''Write json file.'''
        fail = False
        # Dont do nothing if no data to write has been provided
        if data is None:
            return False
        # Check and create file parents dirs of path if any doesnt exists
        _create_parents_dirs(self.file_name)
        # Try to open the file and write to it
        try:
            self.lock.acquire()
            # Open file in write mode (overwrite if exists)
            with open(self.file_name, 'w', encoding="utf-8") as f:
                json_dump(data, fp=f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Error - Can't open and write file {} [{}].".format(self.file_name, str(e)))
            fail = True
        finally:
            self.lock.release()
        return (not fail)


    def read_content(self):
        '''Read all json file content (return json data dict).'''
        # Read json file
        read = self.read()
        # Return empty dictionary if read is empty or doesnt has content key
        if read == {}:
            return {}
        if "Content" not in read:
            return {}
        # The file is not empty and has content, return it
        return read["Content"]


    def write_content(self, data=None):
        '''Add new json data to json file content.'''
        fail = False
        # Dont do nothing if no data to write has been provided
        if data is None:
            return False
        # Check and create file parents dirs of path if any doesnt exists
        _create_parents_dirs(self.file_name)
        # Try to open file
        try:
            self.lock.acquire()
            # If file doesnt exists or is empty, create/overwrite file with json content structure
            if (not path.exists(self.file_name)) or (not stat(self.file_name).st_size):
                with open(self.file_name, 'w', encoding="utf-8") as f:
                    f.write('\n{\n    "Content": []\n}\n')
            # Read json content structure
            with open(self.file_name, "r", encoding="utf-8") as f:
                content = json_load(f)
            # Add provided data to readed json content
            content["Content"].append(data)
            # Overwrite json file with new content
            with open(self.file_name, 'w', encoding="utf-8") as f:
                json_dump(content, fp=f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Error - Can't open and write file {} [{}].".format(self.file_name, str(e)))
            fail = True
        finally:
            self.lock.release()
        return (not fail)


    def is_in(self, data):
        '''Check if data is in json file content.'''
        found = False
        file_data = self.read()
        for _data in file_data['Content']:
            if data == _data:
                found = True
                break
        return found


    def is_in_position(self, data):
        '''Check if data is in json file content and where (index) position it is.'''
        found = False
        file_data = self.read()
        i = 0
        for _data in file_data['Content']:
            if data == _data:
                found = True
                break
            i = i + 1
        return found, i


    def remove_by_uide(self, element_value, uide):
        '''
        Remove specific data from json file content, given an unique identifier element (UIDE).
        [Note: Each json data needs at least 1 UIDE, if there is more than 1, just first one will 
        be removed].
        '''
        # Read json file content
        file_content = self.read_content()
        # Search and remove content element with that UIDE
        for data in file_content:
            if data[uide] == element_value:
                file_content.remove(data)
                break
        # Remove file content and write modified content to it
        self.clear_content()
        if file_content:
            self.write_content(file_content[0])


    def search_by_uide(self, element_value, uide):
        '''
        Return specific data from json file content, given an unique identifier element (UIDE).
        [Note: Each json data needs at least 1 UIDE, if there is more than 1, just first one will 
        be returned].
        '''
        result = dict()
        result["found"] = False
        result["data"] = None
        # Read json file content
        file_content = self.read_content()
        # Search and get content element
        for element in file_content:
            if element:
                if element_value == element[uide]:
                    result["found"] = True
                    result["data"] = element
                    break
        return result


    def update(self, data, uide):
        '''
        Update specific data from json file content, given an unique identifier element (UIDE).
        [Note: Each json data needs at least 1 UIDE, if there is more than 1, just first one will 
        be updated].
        '''
        fail = False
        # Read json file
        file_data = self.read()
        # Search and get content element position
        found = False
        i = 0
        for msg in file_data["Content"]:
            if data[uide] == msg[uide]:
                found = True
                break
            i = i + 1
        # Check if element with that UIDE was found
        if found:
            # Update json content with new data
            file_data["Content"][i] = data
            self.write(file_data)
        else:
            print("Error - Can't update json element with UIDE \"{}\" in file {}. " \
                  "Element not found or file doesn't exists.")
            fail = True
        return fail


    def update_twice(self, data, uide1, uide2):
        '''
        Update specific data from json file content, given two unique identifier elements (UIDE).
        [Note: Each json data needs at least 1 UIDE, if there is more than 1, just first one will 
        be updated].
        '''
        fail = False
        # Read json file
        file_data = self.read()
        # Search and get content element position
        found = False
        i = 0
        for msg in file_data["Content"]:
            if (data[uide1] == msg[uide1]) and (data[uide2] == msg[uide2]):
                found = True
                break
            i = i + 1
        # Check if element with that UIDE was found
        if found:
            # Update json content with new data
            file_data["Content"][i] = data
            self.write(file_data)
        else:
            print("Error - Can't update json element with UIDE \"{}\" in file {}. " \
                  "Element not found or file doesn't exists.")
            fail = True
        return fail


    def clear_content(self):
        '''Clear all json content data of file.'''
        fail = False
        try:
            self.lock.acquire()
            if path.exists(self.file_name) and stat(self.file_name).st_size:
                with open(self.file_name, 'w', encoding="utf-8") as f:
                    f.write('\n{\n    "Content": [\n    ]\n}\n')
        except Exception as e:
            print("Error - Can't open and clear file {} [{}].".format(self.file_name, str(e)))
            fail = True
        finally:
            self.lock.release()
        return (not fail)
    

    def delete(self):
        '''Delete json file.'''
        Fail = False
        if not path.exists(self.file_name):
            return False
        try:
            self.lock.acquire()
            remove(self.file_name)
            self.lock.release()
        except Exception as e:
            print("Error - Can't remove file {} [{}].".format(self.file_name, str(e)))
            Fail = True
        return Fail


    def _create_parents_dirs(self, file_path, permissions=0o775):
        '''Create all parents directories from provided file path (mkdir -p $file_path).'''
        fail = False
        try:
            parentdirpath = path.dirname(file_path)
            if not path.exists(parentdirpath):
                makedirs(parentdirpath, permissions)
        except Exception as e:
            print("Error - Can't create parents directories of {} [{}].".format(file_path, str(e)))
            fail = True
        return fail


    def _is_running_with_py2(self):
        '''Check if script is running using Python 2.'''
        if version_info[0] == 2:
            return True
        return False


    def _is_running_with_py3(self):
        '''Check if script is running using Python 3.'''
        if version_info[0] == 3:
            return True
        return False
