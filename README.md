This is a script that splits a single pdf to multiple smaller pdfs. 
It only requires three parameters, 
1. starting page number, 
2. ending page number and 
3. the section name.

The three are provided in a csv file. 

The script is executed in a terminal and three arguments (2 necessary, 1 mandatory ) are be passed. 
1. The pdf file (include the extention),
2. The csv file (again, include the extention) and 
3. *[optional]* <u>--no-dir</u>  &rarr; each section will be within a directory

Here is how to use the script.

`python split_from_file.py pdf_file_name.pdf csv_file_name.csv [--no-dir]`

