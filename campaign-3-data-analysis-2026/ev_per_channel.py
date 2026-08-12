''' 
Documentation
    Purpose: 
        Get ev per channel from file header.
    Inputs:
        file (string) = title of file being analyzed
    Outputs:
        energy (float) = energy (eV) associated with each channel in XRF file
'''
def ev_per_channel(file):
    with open(file, "r") as f:
        for line in f:
            if "eV per channel" in line: # Checking file for header with value for eV per channel
                parts = line.split(",")
                energy = float(parts[1])
                return energy