import Equation_3_7 as op
import Equation_3_2_File_Input as sp
'''
Implementing equation 4.8 from section 4
'''

def productValue(mreFile, Schreiner = False):

    C_sp_MRE = 1.7*(sp.runCalculation_3_2(mreFile)/1000)*8760 # cost to provide energy to MRE reactor -> 1.7 $/kWHr * power draw of MRE reactor * hours active (1 full year)
    C_op_MRE = op.calcAMCM(2, 2280, 2.39, 2030, 1, 1) # cost to opperate MRE reactor
    C_sp_CEB = 1.7*(50.94/1000)*8760 # cost to provide energy to CEB -> 1.7 $/kWHr * 50.94 W * hours active (1 full year)
    C_op_CEB = op.calcAMCM(2, 59.55, 2.39, 2030, 1, 0)
    MassCEB = 59.55

    if Schreiner:
        C_sp_CEB = 0
        C_op_CEB = 0
        MassCEB = 0

    value = C_sp_MRE + C_op_MRE + C_sp_CEB + C_op_CEB + 100000*(2280 + MassCEB) # add all costs together + cost to transport CEB and MRE to the moon ($100,000/kg)
    print(f'{mreFile} costs: ${value:.2f}')
    return value
