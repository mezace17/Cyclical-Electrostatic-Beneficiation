# Peak Isolation 
from format_data import format_data
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

''' 
Documentation
    Author:
        Cesar Meza and Siyona Jain
    Inputs:
        counts (data frame) = XRF spectral signature counts
        energy (data frame) = list of energy indices
    Outputs:
        titanium_peak (float) = counts of identified peak value 
        plot (optional) = plot 
'''

def peak_isolation(counts, energy, element, plot = 0):
    peaks, _ = find_peaks(counts, height=max(counts)*0.02, distance=20) # identify peaks
    peak_energy = energy[peaks] # find the energies at indices of the peaks
    peak_counts = counts[peaks] # find counts at indices of peaks
    index = -1
    if element == 'Ti':
        bound_lower = 4.25 # keV
        bound_upper = 4.7 # keV
    elif element == 'Fe':
        bound_lower = 6.1 # keV
        bound_upper = 6.6 # keV
    for x in peak_energy:
        index += 1
        if x < bound_upper and x > bound_lower: # identify titanium peak
            element_energy = x
            element_peak = peak_counts.iloc[index]
    if plot: # Use for troubleshooting
        plt.plot(energy,counts, color = 'b')
        plt.scatter(peak_energy, peak_counts, color = 'r')
        plt.show()
    return element_peak, peak_energy