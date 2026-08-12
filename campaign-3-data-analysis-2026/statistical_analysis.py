import pandas as pd
from scipy import stats
'''
Documentation
    Author:
        Cesar Meza
    Inputs:
        dataa (dataframe) = complete dataframe
        element (string) = Ti or Fe
    Outputs:
        dataframe (dataframe) = results as dataframe (just appends transformed data)
        lmbda (float) = optimized lambda for transformation
'''
def stats_tests(data, element):
    if element == 'Ti':
        moniker = 'Titanium'
    elif element == 'Fe':
        moniker = 'Iron'
    ######## Shapiro test for normality ############
    shapiro_test = stats.shapiro(data[f'{moniker} Peak Value'])
    test_statistic_norm = shapiro_test.statistic
    p_value_norm = shapiro_test.pvalue
    if p_value_norm >= 0.05:
        print(f'Data is normal. P-value: {p_value_norm}')
    else:
        print(f'Data is not normal. P-value: {p_value_norm}')
        print("Performing data transformation.")
        temporary_data = pd.to_numeric(data[f'{moniker} Peak Value'])
        final_dep, lmbda = stats.boxcox(temporary_data, lmbda = None)
        data[f'{moniker} (Transformed)'] = final_dep
        print(f'Calculated lambda: {lmbda}') 
    ####### Bartlett test for homoscedasticiy ##########
    groups = [group[f'{moniker} (Transformed)'].to_numpy() 
                  for _, group in data.groupby('Pass Number')]
    test_statistic_hom, p_value_hom = stats.bartlett(*groups)
    if p_value_hom >= 0.05:
        print(f'Data is homoscedastic. P-value: {p_value_hom}')
    else:
        print(f'Data is not homoscedastic. Transformation pending.')
    shapiro_test = stats.shapiro(data[f'{moniker} (Transformed)'])
    test_statistic_norm = shapiro_test.statistic
    p_value_norm = shapiro_test.pvalue
    print(test_statistic_norm, p_value_norm, test_statistic_hom, p_value_hom)
    ################# Final Upload ########################
    return data, lmbda