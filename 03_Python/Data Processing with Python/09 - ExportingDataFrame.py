'''

Exporting dataframes

'''

import os
import pandas as pd

InputFileName='Input_CommaSep.txt'
Endere�o='C:\\Users\\emka\\Desktop\\Python\\'

os.chdir(Endere�o)

#Importando um csv
df1=pd.read_csv(Endere�o+InputFileName)

df1.to_csv('TrashIt_ColonSep.txt',sep=':')

df1.to_csv('TrashIt_To_CSV.csv')

df1.to_csv('TrashIt_To_CVS_NoHeader_NoIndex.csv',header=None,index=None)

df1.to_html('TrashIt_To_HTML_NoHeader_NoIndex.html',header=None,index=None)

