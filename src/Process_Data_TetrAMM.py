# Process Data reads the HDF file for the TetrAMM, configures the 3D array, and returns an analysable dataset

# IMPORTS #

# Public
import cothread
from cothread.catools import *
import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import os
import datetime

# Private (self-created)
import Fourier_Analysis as fa

# VARIABLES #
raw_data = []   # The initial unprocessed dataset
capture_num = 0 # Current capture number
data_points = 0 # Number of points collected per capture
data_types = 0  # Number of different types of data extracted per frame
data  = []      # Processed dataset with total no. samples as rows and the data_types as columns
                # Default data types in order from prep_data() (11): Current1, Current2, Current3, Current4, X, Y, All, ????, ????, Position X, Position Y

# FUNCTIONS #

def read_file(path):
# Function to read the file and extract the dataset.
# Arguments: path name in string, Returns: raw dataset (unstitiched)

    # Reference the global variables outside the function    
    global raw_data
    global capture_num
    global data_points
    global data_types

    # Use h5py to read the file path and get the data 
    f = h5py.File(path,'r')
    f_data = f.get('/entry/instrument/detector/data')[:]
    
    # Set to global variables for easy access later
    raw_data = np.array(f_data)
    capture_num = f_data.shape[0]
    data_points = f_data.shape[1]
    data_types = f_data.shape[2]
    
    return f_data

def prep_data():
# Function to decompose the 3D array into a stiched 2D array
# Arguments: none, Returns: 2D stitched dataset of capture_number rows and data_type columns of data  
    # Reference global variable outside function to access the pulled data, and to place the stiched set
    global raw_data
    global data

    # Initial set of values: first capture, 2000 rows/samples taken x 11 columns of data_types
    base_stitch = raw_data[0,:,:] # array format --> (capture_num, data_points, data_types)

    # Stitch remaining capture data (data_points, data_types) to the end of the initial 2D array
    for x in range(1,capture_num):
        new_stitch = raw_data[x,:,:]
        base_stitch =np.append(base_stitch,new_stitch,axis=0)
    
    #print(base_stitch.shape) to check. Format should be (capture_num * data_points , data_types), where on the TetrAMM GUI data types = 11
    
    data = base_stitch
    return base_stitch

def getdata():
    return data

def runner(): 
    #bob = read_file('/dls/science/groups/vibration/20210722_i18/frametest/T1_0000.h5')
    bob = read_file('/home/dqi23796/fastdigiwrite/T1_0018.h5')
    #print('prepping')
    prep_data()
    #print(data[6,:])
    #prep_data()
    #print('prepping done')
    #print(data.shape)
    #print(capture_num)
   # print(data_points)
    #print(data_types)
    #data[:,graph_of_interest]
    hi =  data[:,6]
    him = np.mean(hi)
    hello = hi-him
    return (hello)
    #cplot.plot_data(data,6)

def overnight_file_creator(hw, fpath_get, fpath_set, counter):
# Function to turn the acquired data into processed .mat files for easier and further analysis 
# Arguments: hw (the name of the hardware), fpath_get (file path from where to get the hdf5 files), fpath_set (file_path to set where the .mat files should be saved), counter (file number increment)
# Returns: None    
    # Read the incrementing file
    file_read = read_file('%(a)s/%(b)s_%(c)s.h5'%{'a': fpath_get, 'b': hw, 'c': counter})
    
    # Prep the data for this file  
    prep_data()

    # To get posiiton x (9) and position y(10), extract that data set from the data processed
    posx = data[:,9]
    posy = data[:,10]

    # Next, Prepare x (time) dataset
    sec = capture_num / 10 # No. seconds = capture number / 10
    total_data_points = (capture_num * data_points) + 1 # Total number of data points (of rows) is the number or data points per capture * the number of captures
    x = np.linspace(0,sec,total_data_points) # create the linspace 

    # Get the timestamp of the file for the waterfall plot:
    tstamp = os.path.getmtime('%(a)s/%(b)s_%(c)s.h5'%{'a': fpath_get, 'b': hw, 'c': counter})
    tstamp_format = datetime.datetime.fromtimestamp(tstamp).strftime('%H:%M:%S')

    # Create a dict called savedict and save all the data, as well as the position x and y data for easy access
    savedict = {
    hw : data,
    'PosX' : posx,
    'PosY' : posy,
    'TSFormat' : tstamp_format,
    'TS' : tstamp
    }

    # Save the dict
    sio.savemat('%(a)s/%(b)s_%(c)s.mat'%{'a': fpath_set, 'b': hw, 'c': counter}, savedict)

    # Return the x linspace
    return x


def bingbong():
    q = 4
    oo = "%04d"%q
    overnight_file_creator('T1', '/dls/science/groups/vibration/20210722_i18/overnight', '/home/dqi23796/mpl_files', oo)

#bingbong()
#runner()
