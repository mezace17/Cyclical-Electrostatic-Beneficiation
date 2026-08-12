# Identify data

from format_data import format_data
import os
import pandas as pd
import numpy as np
from peak_isolation import peak_isolation

''' 
Documentation
    Author:
        Cesar Meza
    Inputs:
        base_path (string) = google drive path where SEM data can be found
    Outputs:
        file_count (int) = number of data folders identified
        data_files (list) = list of folders to analyze
'''

def identify_data(base_path):
    values = os.listdir(base_path)
    data_files = []
    file_count = 0
    for item in values:
        if '.csv' in item: # logic for getting files
            data_files.append(item)
            file_count += 1
        else:
            pass
    return data_files, file_count

''' 
Documentation
    Author:
        Cesar Meza
    Inputs:
        base_path (string) = google drive path where SEM data can be found
        data_files (list) = list of folders to analyze
        element (string) = element to analyze (Ti or Fe)
    Outputs:
        data_list (dataframe) = sorted table of average and standard deviation counts for titanium peak
'''
def extract_data(data_files, base_path, element):
    data_list = pd.DataFrame({"Percent Weight": [], "Average": [], "Standard Deviation": []})
    temp_storage = [] # Empty list to store values from runs 1, 2, and 3 - used to calculate average, standard deviation, etc.
    index_tracker = 0
    data_files.sort()
    for file in data_files:
        split_name = file.split("_")
        percent_weight = float(split_name[2]) # Extracts percent weight
        run_number = int(split_name[5][7]) # Extracts run number (1 , 2, 3)
        counts, energy = format_data(base_path + f'/{file}') # Extracts counts and energy from data
        element_count, _ = peak_isolation(counts, energy, element, 0) # Change last argument to 1 if need to see each spectra
        element_count = float(element_count) # need to convert into float
        temp_storage.append(element_count)
        if run_number == 1 and index_tracker != percent_weight:
            index_tracker = percent_weight
        if run_number == 3 and len(temp_storage) == 3:
            new_row = pd.DataFrame([percent_weight, np.mean(temp_storage), np.std(temp_storage, ddof=1)]).T
            new_row.columns = data_list.columns
            data_list = pd.concat([data_list, new_row], ignore_index=True)
            temp_storage = []
        elif len(temp_storage) != 3 and index_tracker != percent_weight:
            print(f'Data missing for {file}. Substituting with number 0.')
            temp_storage += [0] * (3-len(temp_storage))
            new_row = pd.DataFrame([percent_weight, np.mean(temp_storage), np.std(temp_storage, ddof=1)]).T
            new_row.columns = data_list.columns
            data_list = pd.concat([data_list, new_row], ignore_index=True)
            temp_storage = []
    data_list = data_list.sort_values(by=["Percent Weight"], axis = 0, ascending = True)
    return data_list


'''
Documentation
    Author:
        Cesar Meza
    Inputs:
        base_path (string) = google drive path where SEM data can be found
        data_files (list) = list of folders to analyze
        element (string) = element to analyze (Ti or Fe)
    Outputs:
        data_list (dataframe) = table of raw data for all data collected
'''

def extract_data_II(data_files, base_path):
    data_list = pd.DataFrame({"Sample Number": [], "Pass Number": [],  "Simulant Year": [],  
                              "Titanium Peak Value": [],  "Iron Peak Value": [], 'Titanium Content': [], 'Iron Content': []})
    data_files.sort()
    for file in data_files:
        split_name = file.split(".")
        sample_number = split_name[0] # extracts sample number
        pass_number = split_name[1] # extracts pass number
        simulant_year = split_name[2] # extracts simulant year
        counts, energy = format_data(base_path + f'/{file}') # Extracts counts and energy from data
        Ti_count, _ = peak_isolation(counts, energy, 'Ti', 0) # Change last argument to 1 if need to see each spectra
        Fe_count, _ = peak_isolation(counts, energy, 'Fe', 0) # Change last argument to 1 if need to see each spectra
        Ti_count = float(Ti_count) # need to convert into float
        Fe_count = float(Fe_count) # need to convert into float
        new_row = pd.DataFrame([sample_number, pass_number, simulant_year, Ti_count, Fe_count, 0, 0]).T
        new_row.columns = data_list.columns
        data_list = pd.concat([data_list, new_row], ignore_index=True)
    return data_list