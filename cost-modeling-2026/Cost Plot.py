import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.optimize import curve_fit
import Equation_3_2_File_Input as sp
import Equation_3_6 as value

######### Iron Production #########
def metalProduced(fileName):
    data = []
    with open(fileName, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    del data[0]

    m_regolith = sp.getMdot((10000 *1000)/(15.999*31556952), data) * 31556952 #(regolith / second) * seconds -> total regolith that needs to be processed to meet given oxygen production level

    ironIndex = None
    for i in range(len(data)):
         if data[i][0] == "FeO":
            ironIndex = i
            #print("looking at row: " + str(ironIndex))
            break


    percentWeightIronOxide = float(data[ironIndex][1])/100
    molecularWeightIron = 55.845
    molecularWeightIronOxide = float(data[ironIndex][2])
    e_frac_IronOxide = float(data[ironIndex][10])

    value = m_regolith*percentWeightIronOxide*(molecularWeightIron/molecularWeightIronOxide)*e_frac_IronOxide #in kg

    print(f'Produces {value:.2f} kg iron per year')
    return value



######### Assigning variables #########
costLHS1, ironLHS1 = value.productValue('constants - LHS-1.csv'), metalProduced('constants - LHS-1.csv')
costSchreinerHS, ironSchreinerHS = value.productValue('constants - Shreiner.csv', True), metalProduced('constants - Shreiner.csv')
cost0_02ilm, iron0_02ilm = value.productValue('constants - 0.02 ilm.csv'), metalProduced('constants - 0.02 ilm.csv')
cost0_35ilm, iron0_35ilm = value.productValue('constants - 0.35 ilm.csv'), metalProduced('constants - 0.35 ilm.csv')
costQuinn, ironQuinn = value.productValue('constants - 0.97 ilm.csv'), metalProduced('constants - 0.97 ilm.csv')
cost100ilm, iron100ilm = value.productValue('constants - 100.00 ilm.csv'), metalProduced('constants - 100.00 ilm.csv')
costSchreinerHiTi, ironSchreinerHiTi = value.productValue('constants - Shreiner Hi Ti Mare.csv', True), metalProduced('constants - Shreiner Hi Ti Mare.csv')
costs = [costLHS1, cost0_02ilm, cost0_35ilm, costQuinn, cost100ilm, costSchreinerHS, costSchreinerHiTi]
ironProduction = [ironLHS1, iron0_02ilm, iron0_35ilm, ironQuinn, iron100ilm, ironSchreinerHS, ironSchreinerHiTi]
dollar_per_kg_iron = [c / i for c, i in zip(costs, ironProduction)]

######### Specificaly for curve fit line ########
cost1ilm, iron1ilm = value.productValue('constants - 1.0 ilm.csv'), metalProduced('constants - 1.0 ilm.csv')
cost10ilm, iron10ilm = value.productValue('constants - 10 ilm.csv'), metalProduced('constants - 10 ilm.csv')
cost15ilm, iron15ilm = value.productValue('constants - 15 ilm.csv'), metalProduced('constants - 15 ilm.csv')
cost25ilm, iron25ilm = value.productValue('constants - 25 ilm.csv'), metalProduced('constants - 25 ilm.csv')
cost50ilm, iron50ilm = value.productValue('constants - 50 ilm.csv'), metalProduced('constants - 50 ilm.csv')
cost75ilm, iron75ilm = value.productValue('constants - 75 ilm.csv'), metalProduced('constants - 75 ilm.csv')
fittedCosts = [costLHS1, cost1ilm, cost10ilm, cost15ilm, cost25ilm, cost50ilm, cost75ilm, cost100ilm]
fittedIronProduction = [ironLHS1, iron1ilm, iron10ilm, iron15ilm, iron25ilm, iron50ilm, iron75ilm, iron100ilm]
fitted_dollar_per_kg_iron = [c / i for c, i in zip(fittedCosts, fittedIronProduction)]



######## Plotting #########

######## Bar Graph ########
plt.clf()
xaxis = ['0.4% (LHS-1)', '0.02% (0 Passes)', '0.35% (3 Passes)', '0.97 (Quinn)', '100%', 'Schreiner HS', 'Schreiner (High-Ti Mare)']
plt.bar(xaxis, dollar_per_kg_iron)
plt.title('Cost to Make 1 kg Iron From Regolith of Varying %Weight Ilmenite')
plt.xlabel('Regolith Composition')
plt.ylabel('Cost ($/Kg)')
plt.show()

######### Scatter Plot #########
plt.clf()
xaxisNotFitted = [0.4, 0.02, 0.35, 0.97]
xaxisFitted = [0.4, 1, 10, 15, 25, 50, 75, 100] #some sample values throughout the range to divelope the exponential decay plot
plt.scatter(xaxisNotFitted, dollar_per_kg_iron[0:-3], color = 'r', marker = 'X', label = 'Not Fitted Points')
plt.scatter(xaxisFitted, fitted_dollar_per_kg_iron, color = 'blue', marker = "D", label = 'Fitted Points')
plt.axhline(dollar_per_kg_iron[-2], color = 'r', linestyle = 'dashed', linewidth = 2, label = f'Schreiner HS ({dollar_per_kg_iron[-2]:.2f} $/kg)')
plt.axhline(dollar_per_kg_iron[-1], color = 'black', linestyle = 'dashed', linewidth = 2, label = f'Schreiner High-Ti Mare ({dollar_per_kg_iron[-1]:.2f} $/kg)')
plt.axhline(100000, color = 'g', linestyle = 'dashed', linewidth = 2, label = 'SpaceX Lunar Transport Rate (100,000 $/kg)')

######### exponential decay curve fit #########
#function
def decay(x, a, b, c):
     return a*np.exp(b*x)+c

#fit curve
params, _ = curve_fit(decay, xaxisFitted, fitted_dollar_per_kg_iron, p0=[max(fitted_dollar_per_kg_iron), -0.1, min(fitted_dollar_per_kg_iron)],
                       maxfev=5000)

#generate smooth curve
x_smooth = np.linspace(0, 100, 500)
y_smooth = decay(x_smooth, *params)

#find R^2 term
y_pred = decay(np.array(xaxisFitted), *params)
ss_res = np.sum((np.array(fitted_dollar_per_kg_iron) - y_pred) ** 2)
ss_tot = np.sum((np.array(fitted_dollar_per_kg_iron) - np.mean(fitted_dollar_per_kg_iron)) ** 2)

r_squared = 1 - (ss_res/ss_tot)

#plot fitted curve
a, b, c = params
plt.plot(x_smooth, y_smooth, color = 'blue', label = f'Best Fit Curve: y = {a:.2f}*e^({b:.4f}*x) + {c:.2f}\nR^2 = {r_squared:0.4f}')

######### Break Even Pounts (found by plotting fitted curve and transport & scrheinter costs in desmos -> found intercepts) #########
plt.plot(53.88567, 100000, 'go', label = 'Transport Break Even Point: 53.89% ilm')
plt.plot(13.92381, 255138.01, 'ro', label = 'Schreiner HS Break Even Point: 13.92% ilm')



plt.title('Cost to Make 1 kg Iron From Regolith of Varying %Weight Ilmenite')
plt.xlabel('Regolith Composition')
plt.ylabel('Cost ($/Kg)')
plt.legend()
plt.show()
