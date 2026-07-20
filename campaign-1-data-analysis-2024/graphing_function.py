# Graphing Function
'''
Documentation
    Inputs:
        bin_stats (dictionary) = bin_stats fed in
        n = number of trials
    Outputs:
        plot
'''
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score


def data_prep(bin_stats):
    x_axis = [1,2,3,4,5] # Bin number
    y_axis = [] # Mean of data
    error = [] # Sample number dependent error
    for bin in bin_stats:
        y_axis.append(bin_stats[bin][0]) # Access value
        error.append(bin_stats[bin][1]) # Access standard deviation
    return x_axis, y_axis, error

def percent_weight(bin_stats, n, element):
    x_axis, y_axis, error = data_prep(bin_stats)
    figure = plt.subplots()[1]
    figure.bar(x_axis, y_axis, label=y_axis, yerr=error)
    figure.set_ylabel(f'Percent Weight of {element}')
    figure.set_xlabel('Bin Number')
    figure.set_title(f'Percent Weight of {element} per Bin ({n-1} cycles)')
    print(y_axis)
    plt.show()

def quantity(bin_stats, n, element):
    x_axis, y_axis, error = data_prep(bin_stats)
    figure = plt.subplots()[1]
    figure.bar(x_axis, y_axis, label=y_axis, yerr=error)
    figure.set_ylabel('Quantity of {element} (grams)')
    figure.set_xlabel('Bin Number')
    figure.set_title(f'Quantity of {element} per Bin ({n-1} cycles)')
    print(f'{element} Quantity: {y_axis}')
    print(y_axis)
    plt.show()

def recycle_bin_concentrations(cycle_stats, n, mode, element): # n = number of cycles
    figure = plt.subplots()[1]
    x_axis = []
    y_axis = []
    error = []
    for i in range(n):
        x_axis.append(i)
    for i in range(5):
        y_axis.append([])
        error.append([])
        for cycle in cycle_stats:
                y_axis[i].append(cycle_stats[cycle][f'Bin {i+1}'][0])
                error[i].append(cycle_stats[cycle][f'Bin {i+1}'][1])
    for i in range(5):
        plt.errorbar(x_axis, y_axis[i], yerr=error[i], label=f'Bin {i+1}')
    if mode == 'weight':
        title = 'Percent Weight'
        units = ''
    else: 
        title = 'Quantity'
        units = '(grams)'
    figure.set_ylabel(f'{title} of {element} {units}')
    figure.set_xlabel('Number of Passes')
    figure.set_title(f'{title} of {element} per Bin per Beneficiation Cycle ({n-1} cycles)')
    plt.legend()
    plt.show()

def final_quantity(cycle_stats, n, element):
    figure = plt.subplots()[1]
    x_axis = []
    y_axis = []
    error = []
    for i in range(n):
        x_axis.append(i)
    for i in range(5):
        y_axis.append([])
        error.append([])
        cumulative_quantity = 0
        cumulative_error = 0
        for cycle in cycle_stats:
                error_quantity = cycle_stats[cycle][f'Bin {i+1}'][1]
                quantity = cycle_stats[cycle][f'Bin {i+1}'][0]
                if cycle != 'Cycle 0':
                    cumulative_quantity = y_axis[i][-1] + quantity
                    cumulative_error = error[i][-1] + error_quantity
                if f'Bin {i+1}' == 4:
                    y_axis[i].append(quantity)
                    error[i].append(error_quantity)
                else:
                    y_axis[i].append(cumulative_quantity)
                    error[i].append(cumulative_error)
                    
                ''' Bug Fixing Code
                print(cycle)
                print(y_axis[i])
                if cycle != 'Cycle 0':
                    print(f'{quantity} + {y_axis[i][-2]} = {y_axis[i][-1]}')
                    print(quantity + y_axis[i][-2] == y_axis[i][-1])
                '''
        print(f'Final {element} Quantity for Bin {i+1}: {y_axis[i][-1]}')
    for i in range(5):
        plt.errorbar(x_axis, y_axis[i], yerr=error[i], label=f'Bin {i+1}')
    figure.set_ylabel(f'Cumulative Quantity of {element} (grams)')
    figure.set_xlabel('Number of Passes')
    figure.set_title(f'Cumulative Quantity of {element} separated into Bins per Beneficiation Cycle ({n-1} cycles)')
    plt.legend()
    plt.show()

def recycle_bin_concentrations(cycle_stats, n, element): # n = number of cycles
    figure = plt.subplots()[1]
    x_axis = []
    y_axis = []
    error = []
    for i in range(n):
        x_axis.append(i)
    for i in range(5):
        y_axis.append([])
        error.append([])
        for cycle in cycle_stats:
                y_axis[i].append(cycle_stats[cycle][f'Bin {i+1}'][0])
                error[i].append(cycle_stats[cycle][f'Bin {i+1}'][1])
    for i in range(5):
        plt.errorbar(x_axis, y_axis[i], yerr=error[i], label=f'Bin {i+1}')
    figure.set_ylabel(f'Percent Weight of {element}')
    figure.set_xlabel('Number of Passes')
    figure.set_title(f'Percent Weight of {element} per Bin per Beneficiation Cycle ({n-1} cycles)')
    plt.legend()
    plt.show()

def mass_change():
    figure = plt.subplots()[1]
    # Eventually develop more sophisticated method of comparing mass
    x_axis = [10, 10, 10, 10, 10, 6, 4, 4, 3, 3, 3]
    y_axis = [3, 3, 3, 4, 4, 2, 2, 1, 1, 1, 1]
    slope, intercept = np.polyfit(x_axis, y_axis, deg=1)
    x_plot = np.linspace(3, 10, num=100)
    figure.scatter(x_axis, y_axis, label = 'Mass Data')
    figure.plot(x_plot, intercept + x_plot*slope, color='k',linestyle='dashed', label = 'Linear Regression')
    figure.set_ylabel(f'Final Mass (grams)')
    figure.set_xlabel('Initial Mass (grams)')
    figure.set_title('Average Change in Mass of Bin 4')
    print(f'Regression Equation: {intercept} + {slope}*x')
    #### How to get R^2 ####
    y_analysis = []
    for x in x_axis:
        y_analysis.append(intercept + x*slope)
    r_2 = r2_score(y_axis, y_analysis)
    plt.text(4, 2.5, f'Correlation Coeff. = {r_2:.3f}')
    plt.legend()
    plt.show()
    print(f'Regression Equation: {intercept} + x*{slope}')

def bin_analysis(cycle_stats, n, element, bin_number, mode): # Add linear regression
    figure = plt.subplots()[1]
    x_axis = []
    y_axis = []
    error = []
    for i in range(n):
        x_axis.append(i)
    cumulative_quantity = 0
    cumulative_error = 0
    for cycle in cycle_stats:
            error_quantity = cycle_stats[cycle][f'Bin {bin_number}'][1]
            quantity = cycle_stats[cycle][f'Bin {bin_number}'][0]
            if cycle != 'Cycle 0':
                cumulative_quantity = y_axis[-1] + quantity
                cumulative_error = error[-1] + error_quantity
            if f'Bin {i+1}' == 4:
                y_axis.append(quantity)
                error.append(error_quantity)
            else:
                y_axis.append(cumulative_quantity)
                error.append(cumulative_error)
                ''' Bug Fixing Code
                print(cycle)
                print(y_axis[i])
                if cycle != 'Cycle 0':
                    print(f'{quantity} + {y_axis[i][-2]} = {y_axis[i][-1]}')
                    print(quantity + y_axis[i][-2] == y_axis[i][-1])
                '''
    if mode == 'Percent Weight':
        units = ''
    else: 
        units = '(grams)'
    slope_1, slope_2, intercept = np.polyfit(x_axis, y_axis, deg=2)
    x_plot = np.linspace(0, 3, num=100)
    figure.scatter(x_axis, y_axis, label = f'{element} {mode} Data')
    figure.plot(x_plot, intercept + slope_1*x_plot**2 + slope_2*x_plot, color='k',linestyle='dashed', label = 'Regression Curve')
    figure.set_ylabel(f'Final {mode} of {element} {units}')
    figure.set_xlabel('Number of Passes')
    figure.set_title(f'Final {mode} of {element} separated into Bin {bin_number} per Beneficiation Cycle ({n-1} cycles)')
    y_analysis = []
    for x in x_axis:
        y_analysis.append(intercept + slope_1*x**2 + slope_2*x)
    r_2 = r2_score(y_axis, y_analysis)
    plt.text(1, 0.0016, f'Correlation Coeff. = {r_2:.3f}')
    print(f'Regression Equation: {intercept} + {slope_1}*x + {slope_2}*x^2')
    plt.legend()
    plt.show()

def mass_abstraction():
    figure = plt.subplots()[1]
    # Eventually develop more sophisticated method of comparing mass
    x_plot = np.linspace(0, 20, num=100)
    y_plot = 0.3355**x_plot
    figure.plot(x_plot, y_plot, color='k')
    figure.set_ylabel(f'Decimal Percentage of Initial Mass')
    figure.set_xlabel('Number of Cycles')
    figure.set_title('General Trend of Recycled Bin Mass Reduction Per Cycle')
    plt.show()