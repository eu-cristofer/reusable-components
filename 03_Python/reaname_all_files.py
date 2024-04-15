# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 23:48:06 2023

@author: Cristofer Antoni Souza Costa
@e-mail: cristoferantoni@me.com
"""

import os

def rename_pdf_files(directory_path, suffix="VC_EMKA"):
    """
        Renames all PDF files in a directory by appending a specified suffix 
        to their original names.

    Args:
        directory_path (str): The path to the directory containing PDF files.
        suffix (str, optional): The suffix to be appended to the original file 
            names. Default is "VC_EMKA".
    """
    # Ensure the provided path is a directory
    if not os.path.isdir(directory_path):
        raise Exception("Directory path doesn't exist.")
    
    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Check if the file is a PDF
        if filename.lower().endswith('.pdf'):
            # Construct the new filename by appending the specified suffix
            new_filename = f"{os.path.splitext(filename)[0]}_{suffix}.pdf"
            
            # Construct the new file path
            new_file_path = os.path.join(directory_path, new_filename)
            
            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed: {filename} to {new_filename}")

if __name__ == "__main__":
    
        # Replace 'your_directory_path' with the actual path to your directory
        directory_path = 'C:/Users/EMKA/OneDrive - PETROBRAS/Desktop/docs'
        # Optionally, you can provide a different suffix when calling the function
        rename_pdf_files(directory_path)
