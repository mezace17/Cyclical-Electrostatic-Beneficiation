from ev_per_channel import ev_per_channel
import pandas as pd
''' 
Documentation
    Author:
        Siyona Jain, modified by Cesar Meza
    Purpose: 
        Read raw data and convert into DataFrame for analysis
    Inputs:
        file (string) = title of file being analyzed
    Outputs:
        xrf_data (DataFrame) = table of channels and electron beam intensities
'''
def format_data(file):
    xrf_data =  pd.read_csv(file, skiprows=20) # Header for csv files begins on line 21
    xrf_data.columns = ["Channel", "Counts"] 
    channel = xrf_data["Channel"].values
    energy = channel * ev_per_channel(file) / 1000 # convert to channels to energy in eV
    xrf_data['Energy'] = energy # Create new column with energy
    return xrf_data['Counts'], xrf_data['Energy']