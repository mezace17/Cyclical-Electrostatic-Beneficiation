# Main

###################################################
################ Importing Packages ############### 
###################################################
from single_analysis import single_analysis 
from dictionary_maker import dictionary_maker_recycle
from graphing_function import quantity
from graphing_function import percent_weight
from graphing_function import recycle_bin_concentrations
from graphing_function import final_quantity
from graphing_function import bin_analysis
from graphing_function import mass_change
from graphing_function import mass_abstraction

###################################################
################## Reporting Data ################# 
###################################################
number_of_trials = 5
number_of_cycles = 4 # Currently has
cycle_stats = dictionary_maker_recycle()
mode = 'else' # Change as necessary
element = 'Fe' # Change as necessary
element_name = 'Iron' # Change as necessary
show = False # Change as necessary

for n in range(0,number_of_cycles):
    bin_stats = single_analysis(str(n), mode, element)
    cycle_stats[f'Cycle {n}'] = bin_stats
    if show:
        if mode == 'weight':
            percent_weight(bin_stats, n, element_name)
        else:
            quantity(bin_stats, n, element_name)
if mode != 'weight':
    final_quantity(cycle_stats, number_of_cycles, element_name)
    bin_analysis(cycle_stats, number_of_cycles, element_name, 2, 'Quantity')
    mass_change()
    mass_abstraction()
else:
    recycle_bin_concentrations(cycle_stats, number_of_cycles, element_name) 
    bin_analysis(cycle_stats, number_of_cycles, element_name, 2, 'Percent Weight')