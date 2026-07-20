# Single Trial Analysis
''' 
Documentation
    Inputs:
        beneficiation_pass (string) = number of passes through system (second character in trial code)
        data_type (string) = select between percent weight iron of each bin and grade of each bin
        element (string) = select element to analyze
    Outputs:
        bin_stats (dictionary) = dictionary with mean and standard deviation of single 
            beneficiation pass data
'''

###################################################
################ Importing Packages ############### 
###################################################

from data_extraction import data_extraction
from identify_data import identify_data
from dictionary_maker import dictionary_maker_bins
from grade_conversion import grade_conversion
from data_check import data_check
import statistics

###################################################
################# Extracting Data ################# 
###################################################

def single_analysis(beneficiation_pass, data_type, element):
    path_select = 'trial_' + beneficiation_pass
    base_path = f'' # insert directory here
    data_folders, folder_count = identify_data(base_path)
    bin_dictionary = dictionary_maker_bins()
    for folder in range(folder_count):
        folder_name = data_folders[folder]
        narrow_path = f'{base_path}/{folder_name}'
        data_point, bin_number = data_extraction(narrow_path, element) # element percent weight
        weighted_data_point = grade_conversion(data_point, folder_name)
        if data_type == 'weight':
            bin_dictionary['Bin ' + bin_number].append(data_point*100) # multiplied by 100 for percentage
        else:
            bin_dictionary['Bin ' + bin_number].append(weighted_data_point)
    bin_dictionary = data_check(bin_dictionary)
    for bin in bin_dictionary:
        mean = statistics.mean(bin_dictionary[bin])
        std = statistics.stdev(bin_dictionary[bin])
        std_error = std / len(bin_dictionary[bin])
        bin_dictionary[bin] = [mean, std_error] 
    return bin_dictionary

#print(single_analysis('0', 'bin')) #Debugging

