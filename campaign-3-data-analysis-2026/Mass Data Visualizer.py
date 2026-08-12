import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

'''
This program takes a CSV file that's formated to illustrate the starting weight of regolith before any passes
and then keeps track of how much regolith remains after each subsiquent pass.

The code plots these weights as they correspond to each pass through the seperator and then fits the equation
a*b^x + c to the data. Whatever value that (b*100) is reflects the percent weight lost over each pass

The writing of this program was assisted by Claud.ai for initial drafting and was further revised, expanded upon,
and checked for accurecy and methedology prior to publicaiton

Code Written by: Daniel Pikovskiy
Revised by: Cesar Meza
'''


data = []


with open('mass_data.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)



for row in data:
    print(row)

def defineData(data):
    '''
    Defines the y values from the imported data and returns them
    '''
    y0 = []
    y1 = []
    y2 = []
    y3 = []
    for row in data:
        try:
            if isinstance(float(row[3]), float):
                y0.append(float(row[3]))
        except ValueError:
            pass

        try:
            if isinstance(float(row[7]), float):
                y1.append(float(row[7]))
        except ValueError:
            pass

        try:
            if isinstance(float(row[8]), float):
                y2.append(float(row[8]))
        except ValueError:
            pass

        try:
            if isinstance(float(row[9]), float):
                y3.append(float(row[9]))
        except ValueError:
            pass

    return (y0, y1, y2, y3)


def exp_decay(x, a, b, c):
    '''
    Define the funciton we want to fit to our data f(x) = a*b^x + c
    '''
    return a * (b ** x) + c

def calculate_r_squared(y_actual, y_predicted):
    '''
    Calculates R^2:
    1 - (sum of squared residuals / total sum of squares)
    '''
    residuals = y_actual - y_predicted
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_actual - np.mean(y_actual))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

def getFit(all_x, all_y, a, b, c):
    '''
    Finds R^2 values and prints them to terminal
    '''
    #predicted values based on our model
    y_predicted = exp_decay(all_x, a, b, c)

    #compare predicted values to actual values to get R^2
    r_squared = calculate_r_squared(all_y, y_predicted)

    #print the equation and R^2
    #change this to reflect formating of whatever funciton is being thrown into curve_fit()
    sign = '+' if c >= 0 else '-'
    equation = f"y = {a:.4f} * {b:.4f}^x {sign} {abs(c):.4f}"
    print(f"\nFitted equation: {equation}")
    print(f"R² = {r_squared:.4f}\n")

def drawFitLine(all_x, a, b, c):
    '''
    Draw the line of best fit
    '''
    x_fit = np.linspace(min(all_x), max(all_x), 200)
    y_fit = exp_decay(x_fit, a, b, c)
    plt.plot(x_fit, y_fit, 'k--', label=f'Fit: $y = {a:.2f} \\cdot {b:.2f}^x + {c:.2f}$') #formatting for readability


def drawPlot(data):
    '''
    Generate the plot using predefined methods
    '''

    y0, y1, y2, y3 = defineData(data)

    x0 = [0] * len(y0)
    x1 = [1] * len(y1)
    x2 = [2] * len(y2)
    x3 = [3] * len(y3)

    #combine all points into flat arrays for curve fitting
    #basicaly just make sure each y value is tied to the correct x value
    all_x = np.array(x0 + x1 + x2 + x3)
    all_y = np.array(y0 + y1 + y2 + y3)

    #uncomment to double check that all the data is gonna line up
    # print(all_x)
    # print(all_y)


    #fit the curve using SciPy curve_fit()
    params, _ = curve_fit(exp_decay, all_x, all_y)
    a, b, c = params

    getFit(all_x, all_y, a, b, c)

    drawFitLine(all_x, a, b, c)

    plt.scatter(x0, y0, label='Data for 0 passes')
    plt.scatter(x1, y1, label='Data for 1 passes')
    plt.scatter(x2, y2, label='Data for 2 passes')
    plt.scatter(x3, y3, label='Data for 3 passes')

    plt.xlabel('Pass Number')
    plt.ylabel('Sample Weight (g)')
    plt.title('Mass Data with Fitted Exponential Model')
    plt.xticks([0, 1, 2, 3])  # ensures only 0, 1, 2, 3 show on x-axis
    plt.legend()
    plt.show()

#more sanity checking
# print(y0)
# print(y1)
# print(y2)
# print(y3)

drawPlot(data)
