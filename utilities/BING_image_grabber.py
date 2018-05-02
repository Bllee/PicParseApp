'''Script to grab image training data from Bing
via http://blog.yhathq.com/posts/image-classification-in-Python.html'''

from bs4 import BeautifulSoup
import requests
import re
import os

 
 
def get_soup(url):
    return BeautifulSoup(requests.get(url).text)
 
image_type = "cat"
query = "tabby cat"
#url = "http://www.bing.com/images/search?q=" + query + "&qft=+filterui:color2-bw+filterui:imagesize-large&FORM=QBIR"
url = "http://www.bing.com/images/search?q=" + query + "&qft=&FORM=IRFLT"

#https://www.bing.com/images/search?sp=-1&pq=ssbn&sc=6-4&sk=&cvid=986CA03894DC456BA554F7CA52F8B99F&q=ssbn&qft=&FORM=IRFLTR

soup = get_soup(url)
images = [a['src'] for a in soup.find_all("img", {"src": re.compile("mm.bing.net")})]
#images = [a['src'] for a in soup.find_all("img", {"src": re.compile("staticflikr.com")})]
print (images)

for img in images:
    raw_img = requests.get(img).content
    cntr = len([i for i in os.listdir() if image_type in i]) + 1
    f = open(image_type + "_"+ str(cntr) + ".jpg", 'wb')
    f.write(raw_img)
    f.close()

###File rename if necessary
'''count=0
for filename in os.listdir("."):
    newfilename = "cat"+str(count)+".txt"
    os.rename(filename, newfilename)
    count+=1'''