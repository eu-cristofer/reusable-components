#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:44:50 2020

Code made for the course Data Processing with Python

Method to extract archives of various formats

@author: cristofer
"""

import os

#Library to create and extract files
import patoolib

#set the local environment (set the working directory)
os.chdir("/Users/cristofer/Desktop/Data Processing with Python")
print(os.listdir())

#create a new directory
if not os.path.exists("TrashIt_unpacked"):
    #create it if not exists
    os.makedirs("TrashIt_unpacked")

print(os.listdir())

#pass the input file and output dir, the output dir should exists in the computer
patoolib.extract_archive("Input_Test_file.zip",outdir="TrashIt_unpacked")
