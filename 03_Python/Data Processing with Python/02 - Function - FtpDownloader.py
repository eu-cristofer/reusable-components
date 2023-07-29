#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:00:10 2020

Code made for the course Data Processing with Python

Plataform: Udemy; Instrutor: Ardite Dulce.

@author: cristofer

"""

from ftplib import FTP
import os


#create a function, define four paramenters, set default values for the last three paramenters
def ftpDownloader(filename,host="ftp.pyclass.com",username="student@pyclass.com",passwd="student123"):
    #create a ftp objetc
    ftp=FTP(host)
    #login into the fto site
    ftp.login(username,passwd)
    #specify the working directory of the ftp site
    ftp.cwd("Data")
    #specify where the file will be saved
    os.chdir("/Users/cristofer/Desktop")
    
    #Use the with method to create a file and store it to a variable named file
    with open(filename,"wb") as file:
        #while we keep the file open we grab the content of the remoete file
        #pass into the first argument RETR and the remote file name,
        #then pass in the secondary argument what we want to do
        #Finally we write the content of the remote file into the local file
        ftp.retrbinary("RETR %s" % filename,file.write)

    #exibe o conteúdo de um ftp
    print(ftp.nlst())

    ftp.close()
    
ftpDownloader("isd-lite-format.pdf")