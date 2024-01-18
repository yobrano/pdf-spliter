import pandas as pd
import os, argparse
from PyPDF2 import PdfReader, PdfWriter


def save_pdf(writer, name, mkdirs):
    """ Saves out the pdf splits """

    file_name = f'{name}.pdf'
    # check wheather to create a directory or not
    if mkdirs:
        try:
            os.mkdir(name)
            file_name = f'{name}/{name}.pdf'

        except Exception as e:
            # folder alreader existed
            file_name = f'{name}/{name}.pdf'

    with open(file_name, 'wb') as f:
        writer.write(f)


def split_by_row(row, pdf= None, mkdir= True):
    """ Split the pdf based on dataframe rows  """
    name, start, end = row['name'], row['start'], row['end']
    name= name.strip()
    writer = PdfWriter()

    [writer.add_page(pdf.pages[pg]) for pg in range(start-1, end)]
    save_pdf(writer, name, mkdir)

    print(f'{name:20} | {start:5} | {end:5}|')

def splitter(mkdir= True, pdf= None, df= None):
    """ Use loaded files to begin spliting files. """

    df.apply( split_by_row,
              axis= 1, 
              pdf= pdf,
              mkdir= mkdir)

def main(pdf_file, csv_file, no_dirs = False):
    """ Read in files, ie. the datafame and the pdf.  """

    df = pd.read_csv(csv_file)
    df = df[['name', 'start', 'end']]  

    print('Splits DataFrame Loaded...')

    pdf  = PdfReader(open(pdf_file, 'rb'))
    print('Pdf Loaded...\n')

    splitter(df= df, pdf= pdf, mkdir= not no_dirs)
    print('Splitting completed successfully. Bye.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("PdfInput", help = "Pass in a pdf file to be splited.")
    parser.add_argument("CsvInput", help = "Pass in a Csv file with split rows.")
    parser.add_argument('--no-dirs', action= "store_true", help= "Don't create directories for each split")

    args = parser.parse_args() 
    
    main( args.PdfInput, args.CsvInput, no_dirs= args.no_dirs)
