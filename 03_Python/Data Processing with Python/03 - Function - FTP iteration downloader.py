#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 15:00:01 2020

@author: cristofer
"""

#import the libraries

import os
from ftplib import FTP, error_perm

def ftpDownloader(stationId,startYear,endYear,host="ftp.pyclass.com",username="student@pyclass.com",passwd="student123"):
    #create a ftp objetc
    ftp=FTP(host)
    #login into the fto site
    ftp.login(username,passwd)
    #specify the working directory of the ftp site
    ftp.cwd("Data")
    


    #prepare local environment - specify where the file will be saved
    location="Downloaded"
    #check if the directory exists
    if not os.path.exists(location):
        #create it if not exists
        os.makedirs(location)
    #set the local directory (this command only works if the directory already exists)
    os.chdir(location)
    
    #create a iteration loop to download
    for year in range(startYear,endYear+1):
        #ftp server path auxiliary variable
        fullpath="/Data/%s/%s-%s.gz" % (year,stationId,year)
        
        filename=os.path.basename(fullpath)
        
        try: #estrutura para o caso de não existir o arquivo no servidor, assim o código não pára
            with open(filename, 'wb') as file:
                ftp.retrbinary('RETR %s' % fullpath, file.write)
                print("%s successfully downloaded" % filename)
        except error_perm:
            print ("%s is not avaliable" % filename)
            #if the remote file does not exist, the empty file created will be deleted
            os.remove(filename)
    ftp.close()
    
ftpDownloader("010160-99999", 2010, 2015)





