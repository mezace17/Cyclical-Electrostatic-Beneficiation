# Dictionary maker
''' 
Documentation
    Inputs:
        Mone
    Outputs:
        data_dictionary (dictionary) = dictionary with bins labeled

'''
def dictionary_maker_bins():
    data_dictionary = {}
    for index in range(5):
        name = 'Bin ' + str(index + 1)
        data_dictionary[name] = [] 
    return data_dictionary

def dictionary_maker_recycle():
    data_dictionary = {}
    for index in range(2):
        name = 'Cycle ' + str(index)
        data_dictionary[name] = [] 
    return data_dictionary

