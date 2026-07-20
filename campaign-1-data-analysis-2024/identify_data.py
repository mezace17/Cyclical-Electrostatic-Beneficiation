# Identify data
''' 
Documentation
    Inputs:
        base_path (string) = google drive path where SEM data can be found
    Outputs:
        folder_count (int) = number of data folders identified
        data_folders (list) = list of folders to analyze
'''
import os, os.path
def identify_data(base_path):
    values = os.listdir(base_path)
    data_folders = []
    folder_count = 0
    for item in values:
        if 'analysis_1_region' in item:
            data_folders.append(item)
            folder_count += 1
        else:
            pass
    return data_folders, folder_count