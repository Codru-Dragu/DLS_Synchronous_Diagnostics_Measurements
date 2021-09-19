# Plotting contains funcitons which are used for further processing of cleaned-up data
# This script will plot the data in helful graphs #

# IMPORTS

# Public
import numpy as np
import h5py
import matplotlib.pyplot as plt

# Private (self-created)

# VARIABLES

# FUNCTIONS

def plot_data(data, graph_of_interest):
# Funciton to plot specific data in a graph - WILL BE EDITED FOR THE GUI
# Agrguments: data set and value of the data_type that you want to plot (eg. ch1, x pos, etc.) Returns: none, will auto plot
    a_list = list(range(0, 600000))  
    plt.scatter(a_list, data[:,graph_of_interest])
    #plt.plot(data[:,graph_of_interest])
    #print(a_list, data[:,graph_of_interest])
    #plt.ylabel('some numbers')
    plt.show()
