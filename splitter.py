"""  
    Author: Brian Mburu 
    Date: 24/01/2024

    Splitter is a simple script that splits a large pdf to smaller sections.
    It has both a cli and a gui.
"""

import os
import random
import pandas as pd

from PyPDF2 import PdfReader, PdfWriter

def save_pdf(writer, name, output_dir, mkdir):
    """Saves out the pdf splits"""

    if mkdir:
        file_name = f"{output_dir}/{name}/{name}.pdf"
        if not os.path.exists(f"{output_dir}/{name}"):
            os.makedirs(f"{output_dir}/{name}")
    else:
        file_name = f"{output_dir}/{name}.pdf"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    with open(file_name, "wb") as f:
        writer.write(f)



def split_by_row(row, pdf=None, mkdir=True, print_results= False, output_dir="."):
    """Split the pdf based on dataframe rows"""
    name, start, end = row["name"], row["start"], row["end"]
    name = name.strip()
    writer = PdfWriter()

    _ = [writer.add_page(pdf.pages[pg]) for pg in range(start - 1, end)]
    save_pdf(writer, name, output_dir, mkdir)

    if print_results:
        print(f"{name:20} | {start:5} | {end:5}|")


def cli_main(pdf_file, csv_file, output_dir, no_dirs=False):
    """Read in files, ie. the datafame and the pdf. Call this method when in the cli """

    df = pd.read_csv(csv_file)
    df = df[["name", "start", "end"]]

    print("Splits DataFrame Loaded...")

    pdf = PdfReader(open(pdf_file, "rb"))
    print("Pdf Loaded...\n")

    print(f'{"-"*21}*{"-"*7}*{"-"*6}*')
    print(f'{"Name":20} | {"End":5} | {"Start":5}|')
    print(f'{"-"*21}|{"-"*7}|{"-"*6}*')

    df.apply(
        split_by_row,
        axis=1,
        pdf=pdf,
        mkdir=not no_dirs,
        output_dir=output_dir,
        print_results=True,
    )
    print(f'{"-"*21}*{"-"*7}*{"-"*6}*')
    print("\nSplitting completed successfully. \nBye.")

    return True

def gui_main(pdf_file, csv_file, additional_sections, output_dir, mkdir=True):
    """ reads in the csv and pdf files. Call this when in the gui """
    df = pd.read_csv(csv_file)

    if additional_sections:
        _df = pd.DataFrame(additional_sections)
        df = pd.concat([df, _df])

    with open(pdf_file, "rb") as contents:
        pdf = PdfReader(contents)
        df.apply(
            split_by_row,
            axis=1,
            pdf=pdf,
            mkdir=mkdir,
            output_dir=output_dir,
            print_results=True,
        )
        file_name = os.path.basename(pdf_file).split(".")[0]
        file_path = f"{output_dir}/{file_name}-splits.csv"

        while True:
            if os.path.exists(file_path):
                file_path = f"{output_dir}/{file_name}-splits({random.randint(0, 10000)}).csv"
            else:
                break

        df.to_csv(file_path, index=False)

    return True
