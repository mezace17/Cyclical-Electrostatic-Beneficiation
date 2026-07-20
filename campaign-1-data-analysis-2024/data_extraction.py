# Data Extraction Function
''' 
Documentation
    Inputs:
        folder_path (string) = name of folder to be extracted
        element (string) = two letter abbreviation of element to be identified
    Outputs:
        data (float) = iron percent weight point number 
        bin_number (str) = bin number associated with data
'''
import csv
def data_extraction(folder_path, element):
    file = open(folder_path + "/quantification.csv")
    bin_number = str(folder_path[folder_path.index('-B') + 2])
    csv_reader = csv.reader(file)
    data = 0
    for row in csv_reader:
        if row[1] == element:
            data = float(row[4]) # 4 = weight percent, 3 = atomic percent
    return data, bin_number

