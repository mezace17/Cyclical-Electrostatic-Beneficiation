from standard import standard
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from data_manipulation import identify_data
from data_manipulation import extract_data_II
from conversion import conversion
import numpy as np
from statistical_analysis import stats_tests
import statsmodels.api as sm
from statsmodels.formula.api import ols

data_path = {insert data path here}
########## Create Master Dataframe with all relevant information ############
data_files, file_count = identify_data(data_path) 
master_dataframe = extract_data_II(data_files, data_path)

########## Perform Statistical Tests ##################
master_dataframe, lmbda_Ti = stats_tests(master_dataframe, 'Ti') 
master_dataframe, lmbda_Fe = stats_tests(master_dataframe, 'Fe') 

######### Importing Data ###########
Ti_groups = [group["Titanium (Transformed)"].to_numpy() 
                  for _, group in master_dataframe.groupby('Pass Number')]
Fe_groups = [group["Iron (Transformed)"].to_numpy() 
                  for _, group in master_dataframe.groupby('Pass Number')]

######### ANOVA ###########
model_Ti = ols('Q("Titanium (Transformed)") ~ Q("Pass Number")', data=master_dataframe).fit()
model_Fe = ols('Q("Iron (Transformed)") ~ Q("Pass Number")', data=master_dataframe).fit()
table_Ti = sm.stats.anova_lm(model_Ti, typ=1)
table_Fe = sm.stats.anova_lm(model_Fe, typ=1)
print(table_Ti)
print(table_Fe)

########## Tukey ###########
print(stats.tukey_hsd(*Ti_groups))
print(stats.tukey_hsd(*Fe_groups))

#### Create Diagnostic Plots ####
plot = 0 # Variable for avoiding plots if tables are of interest
if plot == 1:
    plt.hist(master_dataframe['Titanium Peak Value'])
    plt.xlabel('XRF Spectral Counts')
    plt.ylabel('Frequency')
    plt.title('Histogram of Titanium Spectral Data')
    plt.show()
    plt.hist(master_dataframe['Iron Peak Value'])
    plt.title('Histogram of Iron Spectral Data')
    plt.xlabel('XRF Spectral Counts')
    plt.ylabel('Frequency')
    plt.show()

######### Plotting ###########
if plot == 1:
    plt.boxplot(Ti_groups, label=['Pass 0', 'Pass 1', 'Pass 2', 'Pass 3'])
    plt.title("Box Plot of Titanium Spectral Counts After Multiple Passes")
    plt.ylabel(f'Transformed Spectral Counts (\u03BB = {lmbda_Ti:.4f})')
    plt.xticks(ticks=[1, 2, 3, 4], labels=["0", "1", "2", "3"])
    plt.xlabel("Pass Number")
    plt.show()
    plt.boxplot(Fe_groups, label=['Pass 0', 'Pass 1', 'Pass 2', 'Pass 3'])
    plt.title("Box Plot of Iron Spectral Counts After Multiple Passes")
    plt.ylabel(f'Transformed Spectral Counts (\u03BB = {lmbda_Fe:.4f})')
    plt.xticks(ticks=[1, 2, 3, 4], labels=["0", "1", "2", "3"])
    plt.xlabel("Pass Number")
    plt.show()
####### Convert to Percent Weight ########
# Calculate the means and STDS prior to converting
slope_Ti, intercept_Ti, r_value_Ti, p_value_Ti, _ = standard('Ti', plot = plot)
slope_Fe, intercept_Fe, r_value_Fe, p_value_Fe, _ = standard('Fe', plot = plot)
print(f'R^2: {(r_value_Ti**2):.4f}')
print(f'R^2: {(r_value_Fe**2):.4f}')
master_dataframe, average_Ti, std_Ti = conversion(slope_Ti, intercept_Ti, master_dataframe, 'Ti')
master_dataframe, average_Fe, std_Fe = conversion(slope_Fe, intercept_Fe, master_dataframe, 'Fe')
print(f'Average Titanium Content (0, 1, 2, 3 passes): {average_Ti}')
print(f'Standard Deviation of Titanium Content (0, 1, 2, 3 passes): {std_Ti}')
print(f'Ti Percent Increase (1 cycle): {((average_Ti[1]-average_Ti[0])/average_Ti[0]*100):.4f}')
print(f'Ti Percent Increase (3 cycle): {((average_Ti[3]-average_Ti[0])/average_Ti[0]*100):.4f}')

