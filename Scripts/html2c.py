# -*- coding: utf-8 -*-
'''
Script:
    html2c.py
Description:
    Python script that format a html code to C/C++ language constant element that can be placed 
	inside C/C++ code (i.e. for html pages builtin in microcontroller C/C++ code).
Author:
    Jose Rios Rubio
Creation date:
    13/02/2018
Last modified date:
    22/02/2018
Version:
    1.0.0
'''

####################################################################################################

### Libraries/Modules ###

from sys import argv

####################################################################################################

### Auxiliar Functions ###
def str_count_start_same_chars(str_in):
	'''Count the number of consecutive same characters at beginning of a string'''
	num_same_chars = 0
	last_char = str_in[0]
	for char in str_in:
		if char == last_char:
			num_same_chars = num_same_chars + 1
		else:
			break
	return num_same_chars

def str_spaces_to_tabs(str_in):
	'''Convert all the initial spaces of a string to tabs (" " to "\t")'''
	str_out = ""
	num_first_spaces_tabs = 0
	# Determine number of consecutive space/tab characters
	last_char = str_in[0]
	if last_char == ' ' or last_char == '\t':
		num_first_spaces_tabs = num_first_spaces_tabs + 1
		for char in str_in:
			if char == ' ' or last_char == '\t':
				num_first_spaces_tabs = num_first_spaces_tabs + 1
			else:
				break
	# Get spaces substring, convert them to tabs and overwrite that in str_out
	str_spaces = str_in[:num_first_spaces_tabs]
	str_tabs = str_spaces.replace("    ", "\t")
	str_out = '{}{}'.format(str_tabs, str_in[num_first_spaces_tabs:])
	return str_out

def str_just_tab_eol(str_in):
	'''Check if a string has only \t and \n characters'''
	just_tab_eol = True
	for char in str_in:
		if char != '\t' and char != '\n':
			just_tab_eol = False
			break
	return just_tab_eol

####################################################################################################

### Main function ###
def main(argc, argv):
	'''Main Function'''
	# Check if an argument has been provided
	if argc == 2:
		html_original_lines = []
		html_modified_lines = []
		# Read file content by lines
		file_html = open(str(argv[1]), "r")
		html_original_lines = file_html.readlines()
		file_html.close()
		# Modify text line by line
		for line in html_original_lines:
    		# Ignore empty lines
			if not str_just_tab_eol(line):
    			# Replace all initial "    " with "\t" (if any)
				line = str_spaces_to_tabs(line)
				# Replace \ with \\
				line = line.replace("\\", "\\\\")
				# Replace " with \"
				line = line.replace("\"", "\\\"")
				# Modify start of the lines (keep identation and set a " before the text)
				if line[0] == '\t':
					num_tabs = str_count_start_same_chars(line)
					if num_tabs:
						start_str = '{}"'.format(line[:num_tabs])
						end_str = line[num_tabs:]
						for _ in range(0, num_tabs):
							start_str = '{}\\t'.format(start_str)
						line = '{}{}'.format(start_str, end_str)
					else:
						line = '"{}'.format(line)
				else:
					line = '"{}'.format(line)
				# Add one level of identation
				line = '\t{}'.format(line)
				# Set an " at the end of the line text (relace '\n' with '"\n')
				line = line.replace("\n", "\\n\"\n")
				#if "// " not in line: # Just keep lines without comments (// )
				#	if "/*" not in line: # Just keep lines without comments (/*)
				#		if "*/" not in line: # Just keep lines without comments (*/)
				html_modified_lines.append(line) # Keep this line
				html_modified_text = ''.join(html_modified_lines) # Convert string list to one string
				html_modified_text = "const char HTML_PAGE_NAME[] /*PROGMEM*/ = \n{}\";".format(html_modified_text) # Add initial and end structure ("#define CHANGE_NAME " \ \ntext\n")
		# Write output file
		file_html = open("output.c", "w")
		file_html.write(html_modified_text)
		file_html.close()
		print("    [OK] HTML successfully converted in \"output.c\" file.")
	else:
		print("    [Error] You need to specify an input argument for the html file to convert.")

####################################################################################################

### Execute the main function if the file is not an imported module ###
if __name__ == '__main__':
	main(len(argv), argv)
else:
	print("    [Error] html2c.py is a main file, it can not be imported.")
