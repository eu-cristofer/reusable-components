#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 21:25:27 2020

@author: cristofer
"""

import os
import glob
import pandas as pd

#filelist

def concatenate(inDir='/Users/cristofer/Desktop/Data Processing with Python/Input_incomeByState'\
                ,outFile='/Users/cristofer/Desktop/Data Processing with Python/TrashIt_Concatenate.csv'):
    
    os.chdir(inDir)
    fileList=glob.glob('*.xls')
    dfList=[]
    colNames=['GEOID','Income','year']
    
    for fileName in fileList:
        df=pd.read_excel(fileName,skiprows=4,header=None)
        df['2']=fileName.rsplit('State')[1].replace('.xls','')
        dfList.append(df)
        print(fileName)
    concatDF=pd.concat(dfList,axis=0)
    concatDF.columns=colNames
    concatDF.to_csv(outFile,index=None)
    
concatenate()