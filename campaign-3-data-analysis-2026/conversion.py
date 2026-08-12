'''
Documentation
    Author:
        Cesar Meza
    Inputs:
        slope (float) = slope of regression
        intercept (float) = intercept of regression
        element (string) = Fe or Ti
    Outputs:
        converted_data (dataframe) = converted data 
        average_run (dataframe) = Averages for each treatment
        standard_deviation_run = Standard deviation for each treatment
'''

def conversion(slope, intercept, dataframe, element):
    if element == 'Ti':
        name = 'Titanium'
    elif element == 'Fe':
        name = 'Iron'
    dataframe[f'{name} Content'] = (dataframe[f'{name} Peak Value'] - intercept) / (slope)
    zero_passes = dataframe[dataframe['Pass Number'] == '00']
    one_pass = dataframe[dataframe['Pass Number'] == '01']
    two_passes = dataframe[dataframe['Pass Number'] == '02']
    three_passes = dataframe[dataframe['Pass Number'] == '03']
    average_run = [(zero_passes[f'{name} Content'].mean()).item(), (one_pass[f'{name} Content'].mean()).item(), (two_passes[f'{name} Content'].mean()).item(), (three_passes[f'{name} Content'].mean()).item()]
    standard_deviation_run = [(zero_passes[f'{name} Content'].std()).item(), (one_pass[f'{name} Content'].std()).item(), (two_passes[f'{name} Content'].std()).item(), (three_passes[f'{name} Content'].std()).item()]
    # Relic of troubleshooting
    #average_run = [(zero_passes[f'{name} Peak Value'].mean()).item(), (one_pass[f'{name} Peak Value'].mean()).item(), (two_passes[f'{name} Peak Value'].mean()).item(), (three_passes[f'{name} Peak Value'].mean()).item()]
    #standard_deviation_run = [(zero_passes[f'{name} Peak Value'].std()).item(), (one_pass[f'{name} Peak Value'].std()).item(), (two_passes[f'{name} Peak Value'].std()).item(), (three_passes[f'{name} Peak Value'].std()).item()]
    return dataframe, average_run, standard_deviation_run

