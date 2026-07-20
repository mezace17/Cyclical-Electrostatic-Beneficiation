# Data Completeness Check
''' 
Documentation
    Inputs:
        bin_dictionary (dictionary) = dictionary of beneficiation data
    Outputs:
        bin_dictionary (dictionary) = updated for complete data set
'''
def data_check(bin_dictionary):
    for bin in bin_dictionary:
        if bin_dictionary[bin] == []:
            for n in range(29):
                bin_dictionary[bin].append(0) 
        else:
            pass
    return bin_dictionary
