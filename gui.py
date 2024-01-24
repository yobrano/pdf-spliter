"""
    Author: Brian Mburu
    Date: 24/01/2024

    This is gui for a pdf Splitter. 
"""

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import font
import os



def truncate_text(text, max_len= 25, end= "..."):
    """ If a text lenght exceeds the assigned `max_len` then it is truncated."""
    return f"{text[:max_len]}{end if(len(text)>max_len)else('')}"

class PdfSplitterGUI:
    """ Graphical User interface for the pdf splitter project. """

    imported_pdf_path:str
    imported_splits_path:str
    pdf_sections:list

    def __init__(self, root):
        """
        sections:
            1. pdf file
            2. a. csv file
               b. split entries.
        """

        self.root = root
        self.pdf_sections = []
        self.imported_splits_path = ""
        self.imported_pdf_path = ""

        self.default_font = font.nametofont('TkTextFont').actual()
        self.italic_font = f"Arial {self.default_font['size']-1} italic"

        self.files_selection_frame = tk.LabelFrame(self.root)
        self.files_selection_frame.grid(row=0, column=0)

        # Select PDF widgets
        self.select_pdf_label = tk.Label(self.files_selection_frame,
                                         text="Select a pdf to be splitted")
        self.select_pdf_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky=tk.W
        )

        self.select_pdf_btn = tk.Button(self.files_selection_frame,
                                        text="Select File",
                                        command=self.select_pdf)
        self.select_pdf_btn.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.pdf_path_label = tk.Label( self.files_selection_frame,
                                        font= self.italic_font,
                                          text=truncate_text(self.imported_splits_path)
                                            if(self.imported_splits_path)
                                            else("* no file is selected."),
                                        )
        self.pdf_path_label.grid(row=1, column=0, padx=10, pady=1, sticky=tk.W)

        # Import splitter widgets
        self.import_splits_label = tk.Label(self.files_selection_frame,
                                            text="Import splits from file")
        self.import_splits_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.import_splits_btn = tk.Button(self.files_selection_frame,
                                           text="Select File",
                                           command=self.import_splits)
        self.import_splits_btn.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.splits_path_label = tk.Label(self.files_selection_frame,
                                          font= self.italic_font,
                                          text=truncate_text(self.imported_splits_path)
                                            if(self.imported_splits_path)
                                            else("* No file is selected.")
                                        )
        self.splits_path_label.grid(row=3, column=0, padx=10, pady=1, sticky=tk.W)

        # add split entries
        self.add_section_frame = tk.LabelFrame(self.root, text="Add a Section")
        self.add_section_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        # Name, start and end field for the section
        self.section_name_label = tk.Label(self.add_section_frame, text="Section Name")
        self.section_name_label.grid(row= 0, column=0, padx= 10, pady= 10, sticky=tk.W)

        self.section_name_entry = tk.Entry(self.add_section_frame)
        self.section_name_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        self.section_start_label = tk.Label(self.add_section_frame, text="Staring from")
        self.section_start_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.section_start_entry = tk.Entry(self.add_section_frame)
        self.section_start_entry.grid(row=1, column=1, padx=10, pady=10)

        self.section_end_label = tk.Label(self.add_section_frame,
                                          text="Ending at")
        self.section_end_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.section_end_entry = tk.Entry(self.add_section_frame)
        self.section_end_entry.grid(row=2, column=1, padx=10, pady=20, sticky=tk.W)

        self.add_section_btn = tk.Button(self.add_section_frame,
                                         text="Add Section",
                                         command=self.add_section)
        self.add_section_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.split_pdf_btn = tk.Button(self.root, text= "Split", command= self.split_pdf)
        self.split_pdf_btn.grid(row=2, column=0, padx=10, pady=10)


    def import_splits(self,):
        """ Prompt for the user to pick a splitter file. """

        filetypes = (
            ("csv files (comma delimiter)", "*.csv"),
            ("text files", "*.txt"),
            ("All files", "*.*")
        )
        self.imported_splits_path = fd.askopenfilename(
            title="Pick a valid csv file (check help).",
            initialdir="/",
            filetypes=filetypes
        )
        self.splits_path_label.config(text= truncate_text(self.imported_splits_path))


    def select_pdf(self, ):
        """ Prompts the user to pick a pdf file for splitting. """
        filetypes = (
            ("pdf files", "*.pdf"),
            ("All files", "*.*")
        )
        self.imported_pdf_path = fd.askopenfilename(
            title="Pick a valid pdf file to split.",
            initialdir="/",
            filetypes=filetypes
        )

        self.pdf_path_label.config(text= truncate_text(self.imported_pdf_path))


    def add_section(self, ):
        """ Reads in the section attributes.  """
        section_name = self.section_name_entry.get().strip()
        section_start = self.section_start_entry.get().strip()
        section_end = self.section_end_entry.get().strip()

        try:
            self.section_entry_validation(section_name, section_start, section_end)
            self.pdf_sections.append({
                "name": section_name,
                "start":int(section_start),
                "end": int(section_end)
            })

            # Clear the input.
            self.section_name_entry.delete(0, tk.END)
            self.section_start_entry.delete(0, tk.END)
            self.section_end_entry.delete(0, tk.END)
        except AssertionError as exc:
            mb.showerror(title = "Adding the section failed.", message=str(exc))


    def split_pdf(self,):
        """ Splits the imported pdf to sections outlined in the csv file and sections array. """
        try:
            self.required_values_validation()
        except AssertionError as exc:
            mb.showerror(title="A missing parameter", message= str(exc))


    def section_entry_validation(self, section_name, section_start, section_end):
        """ Validates the section data. """

        # Dont accepty empty values
        assert section_name != "", "The section name should not be empty"
        assert section_start != "", "The section start should not be empty"
        assert section_end != "", "The section end value should not be empty"

        # The seciton start and end should be numbers
        assert section_start.isdigit(), "The section start should be a number."
        assert section_end.isdigit(), "The section end should be a number."

        assert int(section_start) < int(section_end), \
            "The section end should be larger than the section start."
        return True


    def required_values_validation(self, ):
        """ validated that all required values before spliting are present. """
        assert self.imported_pdf_path != "", "No pdf file was provided. Select a pdf file."
        assert os.path.exists(self.imported_pdf_path), "The provided pdf path is invalid."
        assert self.imported_pdf_path.endswith(".pdf"), "The provided file is not of pdf format."

        if self.imported_splits_path != "":
            assert self.imported_splits_path.endswith(".csv"),\
                "The provided file is not of csv format."
            assert os.path.exists(self.imported_splits_path),\
                "The provided csv path is invalid."
        elif self.imported_splits_path == "" and len(self.pdf_sections) == 0:
            raise AssertionError(
                "No sections were provided.\nCosider selecting a file or adding you own sections"
            )


if __name__ == "__main__":
    main_root = tk.Tk()
    main_root.title("PdfSplitter")
    pdf_splitter_gui = PdfSplitterGUI(main_root)
    main_root.mainloop()


# ideas:
# Grid manager for the widgets
    # -> grid.col()  will increment the column and return its value before the increment.
