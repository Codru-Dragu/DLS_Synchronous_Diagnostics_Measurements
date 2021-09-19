# Process Data reads the HDF file for the MantaCam, configures the 3D array, and returns an analysable dataset

import sys
import os
import datetime

# Use Claire's path
PATHadd='/home/dqi23796/VirtPython/fit_lib'
sys.path.insert(0,PATHadd)

# IMPORTS 

# Public
import cothread
from cothread.catools import *
import CallFit
import numpy as np
import h5py
import matplotlib.pyplot as plt
import scipy.io as sio

# Private (self-created)
import Fourier_Analysis as fa

# VARIABLES
raw_data = []   # The initial unprocessed dataset
frame_num = 0   # Current frame capture number
fps_num = 708   # Fps count
pix_x = 0       # Intensity data for pixels in x` 
pix_y = 0       # Intensity data for pixels in y    
data  = []      # Processed data set with columns for each of the different porcessed data types and rows for each capture frame
                    # Default data types in order from prep_data() (8): Background, Height from fit, Centre beam position in x, Centre beam position in y, Beam sigma in x, Beam sigma in y, Angle of rotation of the beam, overal error 
magnification = 5.8 # To convert to pixels

# FUNCTIONS

def read_file(path):
# Function to read the file and extract the dataset.
# Arguments: path name in string, Returns: raw dataset (unstitiched)

    # Reference the global variables outside the function    
    global raw_data
    global frame_num
    global pix_x
    global pix_y

    # Use h5py to read the file path and get the data 
    f = h5py.File(path,'r')
    f_data = f.get('/entry/instrument/detector/data')[:]
    
    # Set to global variables for easy access later
    raw_data = np.array(f_data)
    frame_num = f_data.shape[0]
    pix_x = f_data.shape[1]
    pix_y = f_data.shape[2]
    
    return f_data

def prep_data():
# Function to decompose the 3D array into a stiched 2D array of received parameter and error values for each capture frame
# Arguments: none, Returns: 2D stitched dataset of frame_number rows and param+error columns of data
    # Reference global variable outside function to access the pulled data, and to place the stiched set
    global raw_data
    global data

    # Initial set of values: first capture, extract values using callfit funciton. Append error as another column
    base_frame = raw_data[0,:,:] # array format --> (frame_num, pix_x, pix_y)
    [param, error] = process_callfit(base_frame) # call CallFit to retrieve useful processed values

    base_stitch = np.reshape(param, (1, len(param))) # Set up the initial array 
    err = np.reshape(error, (1,1)) # Need to reshape into 1x1 numpy array to be able to append
    base_stitch = np.append(base_stitch,err,axis=1) # Append the error as another data column in the same array

    # Stitch remaining capture data to the end of the base
    for x in range(1,frame_num):
        
        new_frame = raw_data[x,:,:]
        [param, error] = process_callfit(new_frame)
        new_stitch = np.reshape(param, (1, len(param)))
        err = np.reshape(error, (1,1))
        new_stitch = np.append(new_stitch,err,axis=1)
        base_stitch = np.append(base_stitch,new_stitch,axis=0)
    
    data = base_stitch
    return base_stitch

def process_callfit(single_frame):
# Function to call the fabulous external CallFit function that Claire has written!
# Arguments: a frame's worth of data, a 2D array of pix_x by pix_y intentsity values, Returns: processed parameters (see top of page), and error
    [param, error] = CallFit.Fitting(single_frame,2) # Call the fitting code (with 2D arry), which outputs the results
    return param, error

def getraw():
    global raw_data
    return raw_data

def getfn():
    global frame_num
    return frame_num

def runner():
    bob = read_file('/home/dqi23796/fastdigiwrite/C1_0018.h5')
    #bob = read_file('/dls/science/groups/vibration/20210722_i18/overnight/C1_0000.h5')
    #print(raw_data.shape)
    #print(raw_data[0])

    sum = [] # empty sum
    a=0
    while (a<frame_num):
        summ = np.sum(raw_data[a])
        sum.append(summ)
        a=a+1
    print(len(sum))
    #print(len(sum))
        #prep_data()
    #cplot.plot_data(data, 3)
    
    resizer = 200000/(len(sum))

    a_list = list(range(0, len(sum)))
    f_list = [float(i) for i in a_list]  
    r_list = [i * resizer for i in f_list]

    him = np.mean(sum)
    hello = sum-him
    return r_list, hello
    #plt.scatter(r_list, sum)

    #plt.plot(sum)
    #plt.show()'''

def overnight_file_creator(hw, binx, fpath_get, fpss, fpath_set, counter):
# Function to turn the acquired data into processed .mat files for easier and further analysis 
# Arguments: hw (the name of the hardware), bin x (binning multiplier), fpath_get (file path from where to get the hdf5 files),fpss (frames per second), fpath_set (file_path to set where the .mat files should be saved), counter (file number increment)
# Returns: None   
    global data
    global raw_data
    global fps_num

    # First set the fps
    fps_num = int(fpss)

    # Read the incrementing file
    file_read = read_file('%(a)s/%(b)s_%(c)s.h5'%{'a': fpath_get, 'b': hw, 'c': counter})
    
    # Prep the data for this file  
    prep_data()
    
    # Create mean image
    mean_image= np.mean(raw_data, axis=0)

    # To get center x (2) and center y(3)
    posx = data[:,2]
    posy = data[:,3]

    # NOW ACCOUNT FOR THE MAGNIFICATION
    posx = [(p * int(binx) * magnification) for p in posx]
    posy = [(p * int(binx) * magnification) for p in posy]

    # Next, Prepare x (time) dataset
    sec = frame_num / fps_num # No. seconds = frame_number / fps count
    sec = int(sec)
    total_data_points = (frame_num) + 1 # Total number of data points (of rows) is the number or data points per capture * the number of captures
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
    'TS' : tstamp,
    'MeanImg': mean_image
    }

    # Save the dict
    sio.savemat('%(a)s/%(b)s_%(c)s.mat'%{'a': fpath_set, 'b': hw, 'c': counter}, savedict)

    # Return the x linspace
    return x


