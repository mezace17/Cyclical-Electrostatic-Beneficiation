from scipy.integrate import quad
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import sympy as sy


'''
I know this code probably sucks. Its crunch time. Im sorry
'''



def getRegMolarMass(data):
    totalMolarMass = 0 #units: g / mole Regolith
    for row in data:
            totalMolarMass += (float(row[1])*float(row[2]))/100 #add molar masses of constituents together in proportion to their abundances
    # print("total reg molar mass: " + str(totalMolarMass))
    return totalMolarMass

def get_regolith_composition(data):
    '''
    Take in data and fill in corresponding constants
    Returns lists: chi, a, b, c, Cp_bar
    '''
    # Loops over each row and asigns the corresponding values if the row is complete
    chi = []
    a = []
    b = []
    c = []
    Cp_bar = []

    for row in data:
        if len(row[7]) > 0:
            chi.append(float(row[3]))
            a.append(float(row[4]))
            b.append(float(row[5])/100)
            c.append(float(row[6])*(10**5))
            Cp_bar.append(float(row[7]))
    # print(chi, a, b, c, Cp_bar)

    ################ Troubleshooting ######################
    # chi, a, b, c, Cp_bar = get_regolith_composition()
    # n = len(chi)
    # print(sum(chi[i]*a[i] for i in range(n))/(getRegMolarMass(data))*1000)
    # print(sum(chi[i]*b[i] for i in range(n))/(getRegMolarMass(data))*1000)
    # print(sum(chi[i]*c[i] for i in range(n))/(getRegMolarMass(data))*1000)
    # print(sum(chi[i]*Cp_bar[i] for i in range(n))/(getRegMolarMass(data))*1000)

    return chi, a, b, c, Cp_bar


def Cp(T, chi, a, b, c, Cp_bar, data):
    '''
    Heat capacity of regolith melt.
    Calculates each summation where i is the number of elements in chi
    '''

    T_g = 1480
    n = len(chi)
    if T < T_g:
       # print(str(sum(chi[i]*a[i] for i in range(n))
               # + T * sum(chi[i]*b[i] for i in range(n))
                #+ T**-2 * sum(chi[i]*c[i] for i in range(n))) + " at Temp: " + str(T))

        return (sum(chi[i]*a[i] for i in range(n))/(getRegMolarMass(data))*1000
                + T * sum(chi[i]*b[i] for i in range(n))/(getRegMolarMass(data))*1000
                + (T**-2) * sum(chi[i]*c[i] for i in range(n))/(getRegMolarMass(data))*1000)
    else:

       #print(str(sum(chi[i]*Cp_bar[i] for i in range(n))) + " at Temp: " + str(T))
        return sum(chi[i]*Cp_bar[i] for i in range(n))/(getRegMolarMass(data))*1000



def Q (m_regolith, L, data):
    '''
    return the heat flux of regolith where the integral repeatedly calls C_p
    error estimate is a value returned by python to sanity check the integral (currently ignored in implementation)
    '''
    chi, a, b, c, Cp_bar = get_regolith_composition(data)
    integral_result, error_estimate = quad(Cp, 300, 2300, args = (chi, a, b, c, Cp_bar, data), points=[1480] if 300 < 1480 < 2300 else None)
    # print("error estimate", str(error_estimate))
    # print("integral result", str(integral_result))
    result = m_regolith*(L + integral_result)
    # print("m_dot: " + str(m_regolith))
    # print("Q_dot =", str(result))
    return result

def PG(n, G):
    '''
    return the power required to electrolyze the melt
    '''
    # print("PΔG =", str(result))
    return n*G


def getAverageCurrent(data):
    m = getMdot((10000 *1000)/(15.999*31556952), data) * 31556952 #(regolith / second) * seconds -> total regolith that needs to be processed to meet given oxygen production level  [Yeah i know this code is inefficient]
    n = 4
    F = 9.64853321233100184 * (10**4) #Faraday constant
    summation = 0
    for row in data:
        if len(row[8]) > 0:
            summation += ((float(row[1])/100)*float(row[11])*float(row[10]))/(float(row[2])*float(row[12]))

    return m*n*F*summation


def getG(data):
    '''
    returns the current average Gibbs Free Energy across all the electrolysis reactions at 2300K
    excludes P2O5 and MnO due to lack of reliable research documenting delta G at this temperature

    Gibbs free energy data at 2300K for K2O was unavailable so a plot of Gibbs free energies from 298.15K to 2000K was made (from jnaf thermochemical tables)
    and a 3rd degree polynomial was fitted to the data and evaluated at 2300K to approximate the gibbs free energy of K2O at that temp.
    '''
    gVals = []

    m = getMdot((10000 *1000)/(15.999*31556952),data) * 31556952 #(regolith / second) * seconds -> total regolith that needs to be processed to meet given oxygen production level  [Again, I know this code is inefficient]
    n = 4
    F = 9.64853321233100184 * (10**4) #Faraday constant
    for row in data:
        if len(row[8]) > 0: #excludes any values that dont have a value for Gibbs Free Energy
            voltage = m*n*F*((float(row[1])/100)*float(row[11])*float(row[10]))/(float(row[2])*float(row[12]))

            gVals.append(-1*float(row[8])*voltage) #flip sign of free energies

    return (sum(gVals))/getAverageCurrent(data) * 1000 #(J/mole) at 2300K





def getMdot(n, data):
    '''
    derive the mass flow rate from the given average oxygen molar production rate
    n_dot is derived from how much oxygen the reactor is capable of producing (currently specified as 10,000 kg/year)
    n_dot has units mole Oxygen/second
    '''
    totalMolarMass = getRegMolarMass(data) #units: g / mole Regolith
    # print("total Regolith molar mass: " + str(totalMolarMass))
    oxygenMolarMassContribution = 0 #units g / mole oxygen
    for row in data:
        oxygenMolarMassContribution += float(row[9]) #add molar mass contributions of oxygen in proportion to their abundance

    RegToOx = totalMolarMass/oxygenMolarMassContribution #gives ratio (g/mole Regolith)/(g/mole Oxygen) -> (moles Oxygen)/(moles Regolith)


    return (n*(RegToOx**(-1))*totalMolarMass)/1000 # dimensional analysis: (mole Ox)/(second) * (mole Ox / mole Regolith)^-1 * (g / Mole Regolith) * (1 kg / 1000 g) -> kg Regolith / second


def Q_endothermic(n_dot, data):

    summation = 0
    m = getMdot((10000 *1000)/(15.999*31556952), data) * 31556952 #(regolith / second) * seconds -> total regolith that needs to be processed to meet given oxygen production level
    # print("Regolith to be processed:", str(m))
    n = 4
    F = 9.64853321233100184 * (10**4) #Faraday constant
    for row in data:
        if len(row[13]) > 0:
            voltage = m*n*F*((float(row[1])/100)*float(row[11])*float(row[10]))/(float(row[2])*float(row[12]))

            summation += (float(row[12])-float(row[8])*(voltage/getAverageCurrent(data)))*1000 #multiply by 1000 to go from kJ/mole to J/mole

    return n_dot*summation



def calc3_2(n, G, m, L, data):
    '''
    Calculates and returns the power required to heat and electrolyze higher-ilmenite content regolith
    Ptotal ≈ 2*( Q_regolith,heatup + PΔG + Q_endothermic)
    '''
    # print(f'Q_heatup: {Q(m, L, data)}')
    # print(f'PG: {PG(n, G)}')
    # print(f'Q_endothermic: {Q_endothermic(n, data)}')
    return 2*(Q(m, L, data) + PG(n, G) + Q_endothermic(n, data))


def runCalculation_3_2(fileName):
    data = []

    with open(fileName, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    del data[0]
    # print(data)

    n_dot = (10000 *1000)/(15.999*31556952) #average oxygen molar production rate derived from 10,000 kg/year (kg/year -> moles/second)
    G = getG(data)
    m_dot = getMdot(n_dot, data)
    L = 1480 * 1000 #J/kg from schreiner
    # print(f'P-total + {calc3_2(n_dot, G, m_dot, L)}')
    return calc3_2(n_dot, G, m_dot, L, data)


# print(f"P_total = {(runCalculation_3_2('constants - LHS-1.csv')/1000):.2f} kW")
