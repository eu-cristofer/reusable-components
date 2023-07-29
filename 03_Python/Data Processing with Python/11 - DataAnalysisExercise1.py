import pandas as pd

FileName=('Input_Income-By-State-1984.xls')

df1=pd.read_excel(FileName,skiprows=[0,1,2])

df1.to_csv('TrashIt_DataAnalysisExercise.csv',index=None)