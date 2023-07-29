#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 11:32:01 2020

@author: cristofer
"""

import pandas as pd
import os

FileName='Input_CommaSeparated.txt'
Address='/Users/cristofer/Desktop/Data Processing with Python'

os.chdir(Address)

#importando os dados sem header
df0=pd.read_csv(FileName,header=None)
print(df0)

#importando os dados com o header automático sendo primeira linha
df1=pd.read_csv(FileName)
print(df1)

#importando os dados alterando a coluna de index
df2=pd.read_csv(FileName, index_col=2)
print(df2)

#importando arquivo separado por espaços
#in cases where the number of sdelimiting spaces are not fixed we use a regular expressions
#regular expression for one or more spaces is \s+
df3=pd.read_csv("Input_SpacesSeparated.txt", sep="\s+")
print(df3)

