#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:22:02 2020

Code made for the course Data Processing with Python

Method to extract a bucnh o files of various formats

@author: cristofer
"""

import os
import glob
import patoolib

def ExtractFiles(indir="/Users/cristofer/Desktop/Data Processing with Python/Downloaded",out="Extracted"):
    #set the working dir
    os.chdir(indir)
    #create an index of files with the designated extension 
    archives=glob.glob("*.gz")

    #check if the output dir exists and create it if not
    if not os.path.exists(out):
        os.makedirs(out)
    
    #create an index of files into the output directory to avoid overwrite filea
    files=os.listdir(out)
        
    for archive in archives:
        #check if there is the file into the directory and creat if it doesnt
        if archive[:-3] not in files:
            patoolib.extract_archive(archive,outdir=out)