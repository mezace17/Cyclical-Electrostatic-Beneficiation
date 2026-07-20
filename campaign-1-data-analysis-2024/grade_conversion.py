# Grade Conversion Function
'''
Documentation
    Inputs:
        data_point (string) = google drive path where SEM data can be found
        folder_name (string) = name of folder currently analyzed
    Outputs:
        weighted_data_point (float) = grade of sample
'''
import pandas as pd
import string
def grade_conversion(data_point, folder_name):
    folder_path = f'' # insert directory here
    file = open(folder_path + "mass_data.csv")
    
    # Add to account for different recycle indices
    trial_type = string.ascii_uppercase.index(folder_name[0]) # Gets index for A, B, C, D, E
    cycle_number = float(folder_name[1])
    trial_number = trial_type + (cycle_number*7) + 2
    
    bin_number = str(folder_name[folder_name.index('-B') + 2])
    csv_reader = pd.read_csv(file)
    mass = csv_reader.loc[trial_number, f'Adjusted B{bin_number}']
    ### Consider deleting ###
    # initial_mass = csv_reader.loc[trial_number, f'Initial Mass']
    weighted_data_point = data_point * mass 
    return weighted_data_point
