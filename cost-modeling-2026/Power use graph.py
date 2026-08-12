import matplotlib.pyplot as plt
import numpy as np
import Equation_3_2_File_Input as eq32


powerUsage = [eq32.runCalculation_3_2('constants - Shreiner.csv')/1000, eq32.runCalculation_3_2('constants - LHS-1.csv')/1000, eq32.runCalculation_3_2('constants - 0.35 ilm.csv')/1000, eq32.runCalculation_3_2('constants - 0.97 ilm.csv')/1000, eq32.runCalculation_3_2('constants - 0.02 ilm.csv')/1000, eq32.runCalculation_3_2('constants - 100.00 ilm.csv')/1000, eq32.runCalculation_3_2('constants - Shreiner Hi Ti Mare.csv')/1000]
sources = ['Schreiner', '0.4% (LHS-1)', '0.35% (3 Passes)', '0.97% (Quinn)', '0.02% (0 Passes)', '100.00%', 'Schreiner (High-Ti Mare)']

plt.bar(sources, powerUsage)
plt.title('Power Usage to Process Regolith of Varying %Weight Ilmenite')
plt.xlabel('Regolith Composition')
plt.ylabel('Power Usage (in kW)')
plt.show()
