import glob
import os

path = 'C:/Users/EMKA/OneDrive - PETROBRAS/Documentos - SRGE_ERGE_EETC_EDC/MÁQUINAS/9- INSPEÇÃO DE FABRICAÇÃO/REFINO/GASLUB/APIR'

os.chdir(path)

files = glob.glob("*pdf")

for file in files:
    print(file)