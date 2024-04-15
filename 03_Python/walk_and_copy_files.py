# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:52:41 2023

@author: Cristofer Antoni Souza Costa
@e-mail: cristoferantoni@me.com
"""

import os
import shutil

def copy_files_in_list(origin_path, destination_path, file_list):
    """
    Copy files from the subfolders of the origin path to the destination path,
    based on the provided list of filenames.

    Args:
        origin_path (str): The path of the origin folder.
        destination_path (str): The path of the destination folder.
        file_list (list): A list of filenames to be copied.

    Returns:
        None
    """
    # Ensure the destination folder exists
    if not os.path.exists(destination_path):
        raise Exception("Destination path doesn't exist.")
    
    counter = 0
    
    # Walk through all subfolders of the origin path
    for foldername, subfolders, filenames in os.walk(origin_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            # Check if the file is in the specified list
            if filename in file_list:
                # Construct the destination path
                destination_file_path = os.path.join(destination_path, filename)

                # Copy the file to the destination folder
                shutil.copy2(file_path, destination_file_path)
                
                # Remove the found item from the list
                file_list.remove(filename)

                print(f"File '{filename}' copied to '{destination_path}'")
                
                counter += 1;
                
    print("\n%d files copied." % counter)
    
    print("\nMissing files:\n")
    for file in file_list:
        print(file)

if __name__ == "__main__":
    # Example usage:
    origin_folder = 'C:/Users/EMKA/PETROBRAS/GASLUB-HIDW (Básico) Verificação de consistência - General/Documentos Extraídos do SIGEM'
    destination_folder = 'C:/Users/EMKA/OneDrive - PETROBRAS/Desktop/docs'
    files_to_copy = ['I-ET-5000.00-0000-300-PEI-001=C.pdf', 'I-ET-5400.00-5700-311-PEI-301=A.pdf', 'I-ET-5400.00-5700-312-PEI-301=0.pdf', 'I-ET-5400.00-5700-322-PEI-301=0.pdf', 'I-ET-5400.00-5700-322-PEI-302=0.pdf', 'I-ET-5400.00-5700-322-PEI-303=0.pdf', 'I-ET-5400.00-5700-392-PEI-301=0.pdf', 'I-ET-5400.00-5700-854-PEI-302=0.pdf']

    
    copy_files_in_list(origin_folder, destination_folder, files_to_copy)

