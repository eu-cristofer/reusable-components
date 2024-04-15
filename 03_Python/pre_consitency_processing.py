# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 23:56:33 2023

@author: Cristofer Antoni Souza Costa
@e-mail: cristoferantoni@me.com
"""
import os
import fitz  # PyMuPDF
from datetime import datetime

def highlight_text(pdf_path, search_texts, highlight_color=(0, 1, 0)):
    """Open a PDF file, search for specified texts, and highlight them.

    Args:
        pdf_path (str): The path to the PDF file.
        search_texts (list): A list of texts to search for in the PDF.
        highlight_color (tuple, optional): RGB color values for highlighting.
            Default is green (0, 1, 0).
    """
    doc = fitz.open(pdf_path)
    page_count = doc.page_count

    for page_num in range(page_count):
        page = doc[page_num]
        for search_text in search_texts:
            text_instances = page.search_for(search_text)
            for inst in text_instances:
                rect = fitz.Rect(inst)
                highlight = page.add_highlight_annot(rect)
                highlight.set_colors(fill=highlight_color)
                highlight.update()

    doc.saveIncr()

def add_annotation_to_first_page(pdf_path, annotation_text, date_format="%d/%m/%Y"):
    """Add a rectangle with annotation text to the center of the first page of a PDF.

    Args:
        pdf_path (str): The path to the PDF file.
        annotation_text (str): The text to be added to the rectangle.
        date_format (str, optional): The format for displaying the current date. Default is "%d/%m/%Y".
    """
    doc = fitz.open(pdf_path)
    first_page = doc[0]

    # Calculate the center of the page
    page_rect = first_page.rect
    center_x = page_rect.width / 2
    center_y = page_rect.height / 2

    # Create a rectangle in the center
    rect_width = 200
    rect_height = 60
    rect = fitz.Rect(center_x - rect_width / 2, center_y - rect_height / 2,
                     center_x + rect_width / 2, center_y + rect_height / 2)

    # Add the rectangle to the page
    first_page.add_rect_annot(rect, text=annotation_text, opacity=0.7)

    # Save the modified PDF
    doc.save(pdf_path)

def annotate_summary(directory_path, summary_filename, execution_summary):
    """Write a summary of the function execution to a text file.

    Args:
        directory_path (str): The path to the directory containing PDF files.
        summary_filename (str): The name of the summary file.
        execution_summary (str): The summary text to be written to the file.
    """
    summary_filepath = os.path.join(directory_path, summary_filename)
    with open(summary_filepath, 'w') as summary_file:
        summary_file.write(execution_summary)

def rename_and_highlight_pdf_files(directory_path, suffix="_VC_EMKA"):
    """Renames all PDF files in a directory by appending a specified suffix to their original names.
    Highlights specified texts in the PDF, adds annotations to the first page, and saves the modified files.
    Writes a summary of the execution.

    Args:
        directory_path (str): The path to the directory containing PDF files.
        suffix (str, optional): The suffix to be appended to the original file names. Default is "VC_EMKA".
    """
    execution_summary = ""

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
            new_file_path = os.path.join(directory_path, new_filename)

            # Open the PDF file and highlight specified texts
            # highlight_text(file_path, ["UNIDADE DE HIDROISODESPARAFINA – U-5700",
                                       #"HCC E HDT PARA PRODUÇÃO DE LUBRIFICANTES E COMBUSTÍVEIS – GASLUB ITABORAÍ"])

            # # Add annotations to the first page
            # annotation_text = f"Revisado por Cristofer Antoni\n{datetime.now().strftime('%d/%m/%Y')}"
            # add_annotation_to_first_page(file_path, annotation_text)

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed: {filename} to {new_filename}")

    # # Write a summary of the execution
    # annotate_summary(directory_path, "summary.txt", execution_summary)

if __name__ == "__main__":
        # Replace 'your_directory_path' with the actual path to your directory
        directory_path = 'C:/Users/EMKA/OneDrive - PETROBRAS/Desktop/docs'
        # Optionally, you can provide a different suffix when calling the function
        rename_and_highlight_pdf_files(directory_path)
