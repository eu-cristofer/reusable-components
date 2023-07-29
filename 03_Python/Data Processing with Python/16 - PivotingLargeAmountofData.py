#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 14:25:38 2020

@author: cristofer
"""

import pandas as pd
import numpy as np
import os

inFile='input_Concatenated-Merged.csv'
outFile='Pivoted.csv'

df=pd.read_csv(inFile)
df.replace(-9999,np.nan)

#sometimes organizations multiply values by ten to save space in its database
df['Temp']=df['Temp']/10.0

table=pd.pivot_table(df,index=['ID'],columns=['Year'],values='Temp')