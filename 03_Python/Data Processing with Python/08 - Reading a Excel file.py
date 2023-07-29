#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 20:20:31 2020

@author: cristofer
"""

import pandas


path='/Users/cristofer/Desktop/Data Processing with Python/'
filename='Input_GeoData.xlsx'

df1=pandas.read_excel(path+filename,'Sheet1')
df2=pandas.read_excel(path+filename,'Sheet2')

print(df1)
print(df2)

print(df1['País'])

print(df2['População'].mean())

df2['População']=df2['População']/1000000
print(df2['População'])

print(df1.loc['2':'3','Área'])

