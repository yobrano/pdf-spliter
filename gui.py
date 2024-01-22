"""
    Author: Brian Mburu
    Date: 22/01/2024

    This is gui for a pdf Splitter. 
"""
import tkinter as tk
from tkinter import filedialog as fd




class PdfSplitterGUI:
    """
    Graphical User interface for the pdf splitter project.
    """

    root:tk.Tk
    imported_splits_file:str
    pdf_to_split:str
    pdf_sections:list

    def __init__(self, root):
        """
        sections:
            1. pdf file
            2. a. csv file
               b. split entries.
        """

        self.root = root
        self.files_selection_frame = tk.LabelFrame(self.root)
        self.files_selection_frame.grid(row=0, column=0)

        # Select PDF widgets
        self.select_pdf_label = tk.Label(self.files_selection_frame, text="Select a pdf to be splitted")
        self.select_pdf_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.select_pdf_btn = tk.Button(self.files_selection_frame, text="Select File", command=self.select_pdf)
        self.select_pdf_btn.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Import splitter widgets
        self.impprt_splits_label = tk.Label(self.files_selection_frame, text="Import splits from file")
        self.impprt_splits_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.import_splits_btn = tk.Button(self.files_selection_frame, text="Select File", command=self.import_splits)
        self.import_splits_btn.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # add split entries
        self.add_section_frame = tk.LabelFrame(self.root, text="Add a Section")
        self.add_section_frame.grid(row=2, sticky=tk.W)

        # Name, start and end field for the section
        self.section_name_label = tk.Label(self.add_section_frame, text="Section Name")
        self.section_name_label.grid(row= 0, column=0, padx= 10, pady= 10)

        self.section_name_entry = tk.Entry(self.add_section_frame)
        self.section_name_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        self.section_start_label = tk.Label(self.add_section_frame, text="Staring from")
        self.section_start_label.grid(row=1, column=0, padx=10, pady=10)

        self.section_start_entry = tk.Entry(self.add_section_frame)
        self.section_start_entry.grid(row=1, column=1, padx=10, pady=10)
      
        self.section_end_label = tk.Label(self.add_section_frame, text="Ending at")
        self.section_end_label.grid(row=2, column=0, padx=10, pady=10)

        self.section_end_enry = tk.Entry(self.add_section_frame)
        self.section_end_enry.grid(row=2, column=1, padx=10, pady=20)

        self.add_section_btn = tk.Button(self.add_section_frame, text="Add Section", command=self.add_section)
        self.add_section_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)



    def import_splits(self,):
        """ Prompt for the user to pick a splitter file. """

        filetypes = (
            ("csv files (comma delimiter)", "*.csv"),
            ("text files", "*.txt"),
            ("All files", "*.*")
        )
        self.imported_splits_file = fd.askopenfilename(
            title="Pick a valid csv file (check help).",
            initialdir="/",
            filetypes=filetypes
        )


    def select_pdf(self, ):
        """ Prompts the user to pick a pdf file for splitting. """
        filetypes = (
            ("pdf files", "*.pdf"),
            ("All files", "*.*")
        )
        self.pdf_to_split = fd.askopenfilename(
            title="Pick a valid pdf file to split.",
            initialdir="/",
            filetypes=filetypes
        )


    def add_section(self, ):
        """ Reads in the section attributes.  """
        section_name = self.section_name_entry.get()
        section_start = self.section_start_entry.get()
        section_end = self.section_end_enry.get()

        try:
            self.section_entry_validation(section_name, section_start, section_end)
            self.pdf_sections.append([section_name, int(section_start), int(section_end)])
        except Exception as exc:
            print(exc)


    def section_entry_validation(self, section_name, section_start, section_end):
        """ Validates the section data. """

        # Dont accepty empty values
        assert section_name != "", "The section name should not be empty"
        assert section_start != "", "The section start should not be empty"
        assert section_end != "", "The section end value should not be empty"

        # The seciton start and end should be numbers
        try:
            section_start = int(section_start)
            section_end = int(section_end)
        except ValueError as exc:
            raise ValueError("Both the start and end fields should contain whole numbers.") from exc

        assert section_start <= section_start, \
            "The section end should be larger than the section start."
        return True


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PdfSplitter")

    pdf_splitter_gui = PdfSplitterGUI(root)
    root.mainloop()
