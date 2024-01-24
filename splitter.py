"""  
    Author: Brian Mburu 
    Date: 24/01/2024

    Splitter is a simple script that splits a large pdf to smaller sections.
    It has both a cli and a gui.
"""

import csv
import pandas as pd
import os

from PyPDF2 import PdfReader, PdfWriter


def save_pdf(writer, name, mkdirs):
    """Saves out the pdf splits"""

    file_name = f"{name}.pdf"
    # check wheather to create a directory or not
    if mkdirs:
        try:
            os.mkdir(name)
            file_name = f"{name}/{name}.pdf"

        except Exception as e:
            # folder alreader existed
            print(e)
            file_name = f"{name}/{name}.pdf"

    with open(file_name, "wb") as f:
        writer.write(f)


def split_by_row(row, pdf=None, mkdir=True, print_results= False):
    """Split the pdf based on dataframe rows"""
    name, start, end = row["name"], row["start"], row["end"]
    name = name.strip()
    writer = PdfWriter()

    _ = [writer.add_page(pdf.pages[pg]) for pg in range(start - 1, end)]
    save_pdf(writer, name, mkdir)
    
    if print_results:
        print(f"{name:20} | {start:5} | {end:5}|")


def splitter(pdf, df, mkdir=True, print_results = False):
    """ Use loaded files to begin spliting files."""

    df.apply(split_by_row, axis=1, pdf=pdf, mkdir=mkdir, print_results=print_results )


def cli_main(pdf_file, csv_file, no_dirs=False):
    """Read in files, ie. the datafame and the pdf. Call this method when in the cli """

    df = pd.read_csv(csv_file)
    df = df[["name", "start", "end"]]

    print("Splits DataFrame Loaded...")

    pdf = PdfReader(open(pdf_file, "rb"))
    print("Pdf Loaded...\n")

    print(f'{"-"*21}*{"-"*7}*{"-"*6}*')
    print(f'{"Name":20} | {"End":5} | {"Start":5}|')
    print(f'{"-"*21}|{"-"*7}|{"-"*6}*')

    splitter(pdf, df, mkdir=not no_dirs, print_results = True)

    print(f'{"-"*21}*{"-"*7}*{"-"*6}*')
    print("\nSplitting completed successfully. \nBye.")


def gui_main(pdf_file, csv_file, no_dirs=False):
    """ reads in the csv and pdf files. Call this when in the gui """

    with open(pdf_file, "rb") as contents:
        pdf = PdfReader(contents)
        contents.close()

    splits_df = pd.read_csv(csv_file)
    splitter(pdf, splits_df, mkdir=not no_dirs)
