#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 17:57:56 2020

@author: cristofer
"""

import pandas

df1=pandas.read_csv('Input_IncomeByState1984.csv')

df1['Multi1']=df1['1984']/2

df1['Multi2']=df1['1984']/100

df1.to_csv('TrashIt_IncomePlusTwoColumns.csv',index=None)