"""
    Author: Brian Mburu
    Date: 24/01/2024

    This is the command line interface of the splitter script.
"""
import argparse
from splitter import cli_main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("PdfInput", help="Pass in a pdf file to be splited.")
    parser.add_argument("CsvInput", help="Pass in a Csv file with split rows.")
    parser.add_argument(
        "OutputDir", 
        help="Specify where the output files will be placed."
    )
    parser.add_argument(
        "--no-dirs", 
        action="store_true", 
        help="Don't create directories for each split"
    )

    args = parser.parse_args()

    cli_main(args.PdfInput, args.CsvInput, args.OutputDir, no_dirs=args.no_dirs)
