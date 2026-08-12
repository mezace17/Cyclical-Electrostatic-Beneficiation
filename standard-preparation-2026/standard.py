import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from data_manipulation import identify_data
from data_manipulation import extract_data
''' 
Documentation
    Author:
        Cesar Meza and Siyona Jain
    Purpose: 
        Create standard from XRF data for iron or titanium
    Inputs:
        element_selection (string) = Fe or Ti for standard created
        plot (int) = 1 or 0 for plotting standard
    Outputs:
        xrf_data (DataFrame) = table of channels and electron beam intensities
        slope, intercept, r_value, p_value, std_err (floats) = relevant linear regression
            values for standard
'''
def standard(element_selection, plot = 0):
    ############## Read CSV File with Standard Mass Measurements #################
    standard_measurements = pd.read_csv('regolith_standard_measurements.csv') # already sorted
    percent_weight_ilm = standard_measurements['Ilmenite (%w)']

    ############## Loop through files to extract percent weight ##################
    data_path = {insert data path here}
    data_files, file_count = identify_data(data_path) 
    data_list = extract_data(data_files, data_path, element_selection)
    counts = data_list['Average']
    standard_deviation = data_list['Standard Deviation']
    print(data_list)
    ########################## Adjust for Element ##############################
    percent_weight_ilm_const_Ti = 0.657 # percentage of ilm made of TiO2 from Exolith
    percent_weight_ilm_const_Fe = 0.269 # percentage of ilm made of Fe2O3 from Exolith
    mass_Ti = 47.867 # g/mol
    mass_Fe = 55.845 # g/mol
    mass_O = 15.999 # g/mol
    mass_Ti_O2 = mass_O*2 + mass_Ti
    mass_Fe2_O3 = mass_O*3 + mass_Fe*2
    percent_weight_Ti_O2 = mass_Ti / mass_Ti_O2 # percent weight titanium of TiO2
    percent_weight_Ti = percent_weight_ilm * percent_weight_ilm_const_Ti * percent_weight_Ti_O2
    percent_weight_Fe2_O3 = 2*mass_Fe / mass_Fe2_O3 # percent weight iron of FeO2
    percent_weight_Fe = percent_weight_ilm * percent_weight_ilm_const_Fe * percent_weight_Fe2_O3

    ############################## Plot Standard #################################
    # Perform linear regression 
    if element_selection == 'Ti':
        percent_weight_selection = percent_weight_Ti
        element = 'Titanium'
    elif element_selection == 'Fe':
        percent_weight_selection = percent_weight_Fe
        element = 'Iron'    
    slope, intercept, r_value, p_value, std_err = stats.linregress(percent_weight_selection, counts) 
    line = slope*percent_weight_selection+intercept
    if plot:
        plt.plot(percent_weight_selection, line, color = 'r', label=f'y={slope:.2f}x+{intercept:.2f}') # Code sourced from Stack Overflow
        plt.legend(loc='upper left', fontsize=15)
        # Final plotting
        plt.errorbar(percent_weight_selection, counts, standard_deviation, fmt = 'x', color = 'k', ecolor = 'k')
        plt.title('Internal Standard for XRF Measurements', fontsize=16)
        plt.xlabel(f'Percent Weight of {element}', fontsize=16)
        plt.ylabel(f'Spectral Counts of {element}', fontsize=16)
        plt.show()
    return slope, intercept, r_value, p_value, std_err
