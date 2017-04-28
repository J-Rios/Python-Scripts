# -*- coding: utf-8 -*-
#
# Author: Jose Miguel Rios Rubio
# Description: Monitor for Webpage changes
# Creation Date: 29/04/2017
# Last modified Date: 29/04/2017
##############################################

# Modules
import sys # System module
import time # Time module, to add a delay between checks
import requests # Request module, to download webpages
from bs4 import BeautifulSoup # BeautifulSoup module, to parse what we download
from difflib import SequenceMatcher # SequenceMatcher module, to percentual strings comparison

##############################################

# Constants
url = "http://www.thingiverse.com/newest" # Webpage url to monitor changes
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'} # Firefox Header
wait_s = 60 # Time between changes checks (seconds)
change_percent = 17 # Minimum percent of changes to considere a webpage change

##############################################

# Function that return the percent of differences between two strings
def differences(a, b):
	diff = 0
	max = 1
	min = 1

	if len(a) >= len(b):
		max = len(a)
		min = len(b)
	else:
		max = len(b)
		min = len(a)
	
	for n in xrange(min):
		if a[n] != b[n]:
			diff = diff + 1
			
	if max > 0:
		diff = 100*diff/max
	else:
		diff = 0
	
	return diff

##############################################

# Main Function
def main():

	try:
		# Get and parse the Web Page for initial state
		response = requests.get(url, headers=headers) # Download the page
		web_text_old = BeautifulSoup(response.text, "html.parser") # Parse Page to Text

		while True:
			# Get and parse the Web Page for actual state
			response = requests.get(url, headers=headers) # Download the page
			web_text = BeautifulSoup(response.text, "html.parser") # Parse Page to Text

			if differences(str(web_text), str(web_text_old)) > change_percent: # Check if there is a change of "change_percent" or more, checking strings differences
				print "The webpage has changed" # Webpage changed
				break # Exit while
			else:
				web_text_old = web_text # Update the old state (dummy?)
				time.sleep(wait_s) # Wait until next comparation moment
	except:
		# Catch exceptions
		print("Error: ", sys.exc_info())
		exit()

##############################################

# Main Function call
if __name__ == "__main__":
	main()
