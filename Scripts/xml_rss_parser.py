# -*- coding: utf-8 -*-
#
# Author: Jose Miguel Rios Rubio
# Description: XML RSS feed parser
# Creation Date: 02/05/2017
# Last modified Date: 02/05/2017
##############################

# Modules
import sys
import requests
import lxml.etree as et

##############################

# Constants
feed_url = "http://hackaday.com/feed/" # Google search url
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'} # Firefox Header

##############################

def main():

    titles = []
    dates = []
    links = []
    descriptions = []

    try:
		# Get and parse the Webpage
		response = requests.get(feed_url, headers=headers) # download the page
		web_text = et.XML(response.content) # Parse Page to Text

		# Obtain titles, links and abstracts of all the search results
		for item in web_text.findall('channel/item'):
			titles.append(item.find('title').text) # Get the title
			links.append(item.find('link').text) # Get the link
			dates.append(item.find('pubDate').text) # Get the date
			description_raw = item.find('description').text
			if "<p>" in description_raw:
				index0_realDescription = description_raw.find("<p>") + 3
				index1_realDescription = description_raw.find("</p>")
				descriptions.append(description_raw[index0_realDescription:index1_realDescription]) # Get the abstract
			else:
				descriptions.append(description_raw) # Get the abstract

		for i in range(len(titles)-1, -1, -1):
			print(titles[i] + "\n----------------------------------\n" + dates[i] + "\n----------------------------------\n" + descriptions[i] + "\n----------------------------------\n" + links[i])
			print("\n\n\n")
            
            
    except:
		print("Error: ", sys.exc_info())
		exit()

##############################

if __name__ == '__main__':
	main()

# Fin del Codigo
