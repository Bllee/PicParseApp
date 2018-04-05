# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 13:26:04 2018

@author: bllee
"""
'''Simple script to download images based on URLs from GDELT provided list.
Workflow:
    Download GDELT URLs into spreadsheet from API
    Save URLs to plain text file (Use Open Document and plain (not encoded) text)
    Put the file in the same directory as this script
    Run it

To do:
    Improve Multi-threading '''
    

import requests
import os
import threading

#Load URLs from text file and strip carriage returns to read into requests
with open("uranium.txt", "r") as f:
    urls = [line.rstrip("\n").rstrip("\r") for line in f]

  
def download(url):
    try:
        r = requests.get(url)
        filename = os.path.basename(url)
        with open (filename, "wb") as g:
            g.write(r.content)
        r.raise_for_status()
    except Exception as e:
        print ("Gag!: %s" % (e))
    
#Start the thread to speed downloads
threads = [threading.Thread(target=download, args=(url,)) for url in urls]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

#Rename files in directory for easier handling

titlecount = 1
for item in os.listdir():
    oldext = os.path.splitext(item)[1]
    os.rename(item, str(titlecount)+"UraniumImage" + oldext)
    titlecount +=1 

 

    
