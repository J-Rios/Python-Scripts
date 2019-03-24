#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####################################################################################################

from sys import exit
from os import path, makedirs
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep

####################################################################################################

SEARCH_CHANNELS_URL = "https://en.tgchannels.org/category/all?page={}&size=100&lang=all"
TELEGRAM_LINK_BASE_URL = "https://t.me/{}"
TO_WRITE_CHAT_INFO = "Chat Title: {}\nChat Link: {}\n\n------------------------------\n\n"

####################################################################################################

def create_parents_dirs(file_path):
    '''Create all parents directories from provided file path (mkdir -p $file_path).'''
    try:
        parentdirpath = path.dirname(file_path)
        if not path.exists(parentdirpath):
            makedirs(parentdirpath, 0o775)
    except Exception as e:
        print("ERROR - Can't create parents directories of {}. {}".format(file_path, str(e)))


def file_write(file_path, text=""):
    '''Write text to provided file.'''
    create_parents_dirs(file_path)
    # Determine if file exists and set open mode to write or append
    if not path.exists(file_path):
        print("File {} not found, creating it...".format(file_path))
    # Try to Open and write to file
    try:
        with open(file_path, 'a', encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print("ERROR - Can't write to file {}. {}".format(file_path, str(e)))


def get_web_html(url):
    print(f"HTTP GET {url}")
    try:
        web =  urlopen(url)
        if web.code != 200:
            print(f"Bad response code: {web.code}")
            # If service unavailable, just return None
            if web.code == 503:
                return None
            else:
                finish(1)
    except HTTPError as e:
        print(f"Bad response code: {e.code}")
        # If service unavailable, just return None
        if e.code == 503:
            return None
        else:
            finish(1)
    return web.read()

####################################################################################################

### Main and Finish Functions ###

def main():
    '''Main Function.'''
    web_page_num = 1584
    while True:
        try:
            # Get Titles
            web_page = SEARCH_CHANNELS_URL.format(web_page_num)
            web_html = get_web_html(web_page)
            if web_html is None:
                sleep(10)
                continue
            web_page_num = web_page_num + 1
            soup = BeautifulSoup(web_html, "lxml")
            l_a_channels = soup.findAll("a", {"class": "channel-item"})
            num_channels = len(l_a_channels)
            if num_channels == 0:
                print("No more links found, exiting")
                finish(0)
            i = 0
            while i < num_channels:
                chat_title = "None"
                chat_link = "None"
                #Get Title
                chat_title = l_a_channels[i].find("h1", {"class": "channel-item__title"}).string
                # Get Link
                chat_url = l_a_channels[i]["href"]
                if chat_url is not None:
                    chat_url = chat_url.replace("/channel/", "")
                    chat_url = chat_url.split('?', 1)[0]
                    chat_link = TELEGRAM_LINK_BASE_URL.format(chat_url)
                chat_info = TO_WRITE_CHAT_INFO.format(chat_title, chat_link)
                file_write("./chats.txt", chat_info)
                i = i + 1
        except Exception as e:
            print(f"{e}")
            finish(1)
    finish(0)


def finish(return_code):
    '''Finish function.'''
    print(f"\n All resources released, exit({return_code}).\n")
    exit(return_code)

####################################################################################################

### Script Input - Main Script ###

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        finish(0)
