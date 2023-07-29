 # -*- coding: utf-8 -*-
"""
Spyder Editor

Code made for the course Data Processing with Python

Plataform: Udemy; Instrutor: Ardite Dulce.

@author: Cristofer

Este código abre, navega entre os diretórios do FTP e fecha o a conexão ftp

"""

from ftplib import FTP

ftp=FTP("ftp.pyclass.com")

ftp.login("student@pyclass.com","student123")

#exibe o conteúdo de um ftp
print(ftp.nlst())

#detalha o conteúdo de uma pasta específica do ftp
print(ftp.nlst("Data"))

#alterando o diretório de trabalho
ftp.cwd("Data")
print(ftp.nlst())

#descendo um nível o diretório
ftp.cwd("..")
print(ftp.nlst())

#close the conection
ftp.close()