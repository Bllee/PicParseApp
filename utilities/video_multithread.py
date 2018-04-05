# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 12:30:21 2018

@author: bllee

Video keyframe extraction utility.
Takes YouTube link, downloads video, extracts keyframes and timestamps,
and saves results to a new folder with name+timestamp+.jpg format

Requires ffmpeg and ffprobe
"""

from pytube import YouTube
import subprocess
import concurrent.futures 
import time
import os


  
        
#List of YouTube video links    
URLS = ['https://www.youtube.com/watch?v=Bs7vPNbB9JM']#, 'https://www.youtube.com/watch?v=PJ4t2U15ACo']#, 'https://www.youtube.com/watch?v=Bv25Dwe84g0']

#Path to ffmpeg/ffprobe
FFMPEGPATH = 'D:\\ffmpeg64\\bin\\'

SAVEPATH = 'D:\\Documents\\PythonStuff\\MyPythonScripts\\tempvids\\'

#SAVEPATH = os.path.join(os.path.sep, 'Documents', 'PythonStuff', 'MyPythonScripts', 'tempvids')

#Simple wrapper to facilitate direct download via pytube with ThreadPoolExecutor
def wrapit(url):
    YouTube(url).streams.first().download(output_path='D:\\Documents\\PythonStuff\\MyPythonScripts\\tempvids\\')  
        
#YouTube('https://www.youtube.com/watch?v=Bs7vPNbB9JM').streams.first().download(output_path='D:\\Documents\\PythonStuff\\MyPythonScripts\\tempvids\\')       

#Multithreading to speed up download     
with concurrent.futures.ThreadPoolExecutor(max_workers= len(URLS)) as executor:
    executor.map(wrapit, URLS)

#Rename videos
os.chdir(SAVEPATH)
for fn in os.listdir():
    os.rename(fn, fn.replace(" ", "_")[:20]+".mp4")
    

#Keyframe timestamps
    
vidnames = [filename for filename in os.listdir() if ".mp4" in filename] #should still be in SAVEPATH

for vidname in vidnames:
 
    subprocess.call(f'{FFMPEGPATH}ffprobe {SAVEPATH}{vidname} \
                -select_streams v -show_entries frame=key_frame,pkt_pts_time -of csv=nk=1:p=0 | findstr "1," \
                > {SAVEPATH}{vidname}.txt', shell=True)

#Keyframe thumbnails

for vidname in vidnames:
    
    subprocess.call(f'{FFMPEGPATH}ffmpeg -i {SAVEPATH}{vidname} -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 {vidname}_%02d.jpg', shell=True)
    
#Rename keyframe thumbnails to include timestamp

