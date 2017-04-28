# -*- coding: utf-8 -*-
#
# Author: Jose Miguel Rios Rubio
# Description: Get a Google search webpage and extract titles, links and abstract of every result
# Creation Date: 28/04/2017
# Last modified Date: 28/04/2017
##############################################

# Modules
import sys # System module
import requests # Request module, to download webpages
from bs4 import BeautifulSoup # BeautifulSoup module, to parse what we download

##############################################

# Constants
google_search_url = "https://www.google.es/search?q=site:telegra.ph&tbs=sbd:1,qdr:d" # Google search url
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'} # Firefox Header

##############################################

# Global variables
titles    = [] # List for search results Titles
links     = [] # List for search results links
abstracts = [] # List for search results abstracts

# Main Function
def main():
	
	global titles
	global links
	global resumenes
	
	try:
		# Get and parse the Web Page
		response = requests.get(google_search_url, headers=headers) # Download the page
		web_text = BeautifulSoup(response.text, "html.parser") # Parse Page to Text
		
		# Obtain titles, links and abstracts of all the search results
		for result in web_text.body.findAll(class_='g'): # For every search result
			titles.append(result.find(class_='r').text) # Get the title
			links.append(result.find('cite').text) # Get the link
			abstracts.append(result.find(class_='st').text) # Get the abstract
			#dates.append(result.find(class_='f').text) # Get the date
		
		# Show the obtained results
		for i in xrange(0, len(titles)):
			print(titles[i])
			print(links[i])
			print(abstracts[i])
			print(" ")
	except:
		# Catch exceptions
		print("Error: ", sys.exc_info())
		exit()

##############################################

# Main Function call
if __name__ == "__main__":
	main()
