'''
This code opens ilastik batch output .csv files, finds the structures of interest and counts them.
It then gives back a new csv file in which the counted numbers are written

Sarah V. Schweighofer, November 2021, Göttingen, Max Planck Institute for Biophysical Chemistry
'''


import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog  #needed for .askdirectory
import os
import pandas as pd
import numpy as np
import csv



def main():
    # ask user to specify path to the folder
    path = filedialog.askdirectory()  # prompts user to choose directory. From tkinter

    # prints out the number of files in the selected folder with the .csv file format and puts them into the list [filenames]
    file_format = ".csv"
    filenames = [filename for filename in sorted(os.listdir(path)) if filename.endswith(file_format)]
    print("There are {} files with this format.".format(len(filenames)))
    if not filenames:  # pythonic for if a list is empty
        print("There are no files with this format.")

    #create all the empty lists which are to be filled when iterating over the individual files and then serve as colums for the final table
    rings_Bax = []
    rings_Bax_stuff = []
    rings_Bak = []
    rings_Bak_stuff = []
    rings_merge = []
    rings_merge_stuff = []

    column_headers = []

    # create empty output table
    output_table = []

    for filename in filenames:

            file = os.path.join(path, filename)
            print(file)

            # reads in the original table via Pandas package:
            original_table = pd.read_csv(file, delimiter=',')
            print(original_table)

            if "Bax.STED" in filename:
                # count objects per class, "Predicted class" is hte column header in the original table
                number_of_rings = len(original_table[original_table["Predicted Class"] == "rings"])
                print("There are {} rings.".format(number_of_rings))
                rings_Bax.append(number_of_rings)

                number_of_rings_with_stuff = len(original_table[original_table["Predicted Class"] == "rings_with_stuff"])
                print("There are {} rings with stuff.".format(number_of_rings_with_stuff))
                rings_Bax_stuff.append(number_of_rings_with_stuff)

            if "Bak.STED" in filename:
                 # count objects per class, "Predicted class" is hte column header in the original table
                number_of_rings = len(original_table[original_table["Predicted Class"] == "rings"])
                print("There are {} rings.".format(number_of_rings))
                rings_Bak.append(number_of_rings)

                number_of_rings_with_stuff = len(original_table[original_table["Predicted Class"] == "rings_with_stuff"])
                print("There are {} rings with stuff.".format(number_of_rings_with_stuff))
                rings_Bak_stuff.append(number_of_rings_with_stuff)

            if "merge" in filename:
                 # count objects per class, "Predicted class" is hte column header in the original table
                number_of_rings = len(original_table[original_table["Predicted Class"] == "rings"])
                print("There are {} rings.".format(number_of_rings))
                rings_merge.append(number_of_rings)

                number_of_rings_with_stuff = len(original_table[original_table["Predicted Class"] == "rings_with_stuff"])
                print("There are {} rings with stuff.".format(number_of_rings_with_stuff))
                rings_merge_stuff.append(number_of_rings_with_stuff)

                #fill the column_header list only from the merged files
                column_header = get_spl_name(filename)
                column_headers.append(column_header)

    output_table.append(rings_Bax)
    output_table.append(rings_Bak)
    output_table.append(rings_merge)
    output_table.append(rings_Bax_stuff)
    output_table.append(rings_Bak_stuff)
    output_table.append(rings_merge_stuff)

    # create rowheaders for output table
    row_headers = ('rings_Bax', 'rings_Bak', 'rings_merge', 'rings_with_stuff_Bax', 'rings_with_stuff_Bak', 'rings_with_stuff_merge')


    # print(output_table)
    # print(column_headers)

    name = "table_of_BaxK_structures.csv"
    numpy_and_save(output_table, path, name, column_headers, row_headers)

    #print(rings_Bax, rings_Bax_stuff, rings_Bak, rings_Bak_stuff, rings_merge, rings_merge_stuff)


def get_spl_name(filename):
    split = filename.split("pos") # splits a string by removing the separator in "", then makes a list with the created substrings
    IF_spl = split[0]
    pos = "pos" + split[1][0:2]
    spl_name = IF_spl + pos
    return spl_name


def numpy_and_save(input_table, table_path, name, column_headers, row_headers):
    # transforms table to numpy array
    np_table = np.asarray(input_table)
    print("\n", np_table)
    # need to transpose because want replicates as columns
    # transposed = np.transpose(np_table)
    # print("\n", transposed)

    # if len(column_headers) != transposed.shape[1]:
    #     raise RuntimeError('Anzahl der Spalten der Daten ungleich der Anzahl der Spaltennamen')
    # if len(row_headers) != transposed.shape[0]:
    #     raise RuntimeError('Zeilen in Daten ungleich Anzahl der Zeilennamen')

    result = os.path.join(table_path, name)

    # mit csv package
    with open(result, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([''] + column_headers)  # [''] macht die erste Zelle leer
        for i in range(len(row_headers)):
            writer.writerow([row_headers[i]] + [value for value in np_table[i, :]]) # schreibt Zeile für Zeile wobei die erste Spalte mit den Headers gefüllt wird und die restlichen Zellen dann mit den Werten



if __name__ == '__main__':

    # ask user which what part in the name we are looking for with Tkinter:
    # ROOT = tk.Tk()  # no idea what this does but is needed for the prompt to work
    # ROOT.withdraw()  # no idea what this does but is needed for the prompt to work
    # namepart1 = simpledialog.askstring(title="namepart1", prompt="Please enter the namepart you are looking for - best: copy-paste (eg STED, Confocal, Bax, Tom etc ..):")

    main()