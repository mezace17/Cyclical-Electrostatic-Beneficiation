import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from data_manipulation import identify_data
from data_manipulation import extract_data_II
import numpy as np
from statsmodels.formula.api import ols

data_path = {insert data path here}
########## Create Master Dataframe with all relevant information ############
data_files, file_count = identify_data(data_path) 
master_dataframe = extract_data_II(data_files, data_path)

######### Importing Data ###########
master_dataframe.to_csv('comparison.csv', index=False)

one_pass = master_dataframe[master_dataframe["Pass Number"] == '01']["Titanium Peak Value"]
two_pass = master_dataframe[master_dataframe["Pass Number"] == '02']["Titanium Peak Value"]

#### Create Diagnostic Plot ####
plt.boxplot([one_pass, two_pass])
plt.xlabel('Pass Number')
plt.ylabel('XRF Spectral Counts')
plt.title('Comparison of Titanium Spectral Data at 20 kV')
plt.show()

########## Perform Non-Parametric Test ##################
nonpar_test = stats.ranksums(one_pass, two_pass, alternative = 'two-sided')
print(nonpar_test)