import os, pandas as pd

FileName='Input_SmallFile.dat'

df1=pd.read_csv(FileName,index_col=0)

print(df1['Value'].mean())

print(df1.loc['Day4','Value'])

print(df1.iloc[3,0])

print(df1.loc['Day4'])