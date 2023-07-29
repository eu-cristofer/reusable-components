#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 18:27:34 2020

Course Data Processing with Python

Script to iterate between csv files and add a column and populate it with values

@author: cristofer
"""

import os, pandas, glob

InputFilesDir='/Input_Practice No.3'
WDir='/Users/cristofer/Desktop/Data Processing with Python'

def addField(indir=WDir+InputFilesDir):
    os.chdir(indir)
    fileList=glob.glob('*')
    for filename in fileList:
        df1=pandas.read_csv(filename,sep='\s+',header=None)
        #Criando uma nova 
        #Split the the filename considering the stated separator and return the first part
        #Using the shape method we discover the length of the column and multiple the value
        df1['Station']=[filename.rsplit('-',1)[0]]*df1.shape[0]
        df1.to_csv('TrashIt_'+filename+'.csv',index=None,header=None)