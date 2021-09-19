# Script to perform fourier analysis on the data obtained from the beamline

# IMPORTS #
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import scipy.io as sio

# VARIABLES #
hw_names = ['T1', 'T2', 'C1'] 
cap_file = 0
cap_range_min = 0
cap_range_max = 0
num_hdf5_files = 2

# FUNCTIONS #

# Generating Functions: 
def frequency_base_gen(x,y,dc):
# Function to find the frequency base and prepare frequency list
# Arguments: x (indicies) and y (position data), dc = dc drift removal value
# Returns: length of dataset (nx), frequency dataset, frequency indicies

    # Set the dc value
    # dc = 2
    # Find the frequency base:

    # Find the sampling frequency:
    diff_x = np.diff(x, n=1, axis=0)
    f_sample = 1 / (diff_x.mean(axis=0))
    # Length of the X dataset
    nx = len(x)
    # Frequency Axis based on the X dataset
    normf = np.linspace(0,nx,nx+1)
    normf = normf / nx
    f = normf * f_sample
    # Midpoint of X dataset
    nfx = np.floor(nx / 2)

    # Remove the dc component including dc drift if specified
    # Need to remove f() above Nyquist, as we fold this back.
    nfx = nfx.astype(int)
    fft_indicies = list(range(dc,nfx)) # start on the dc value. Default is 1 to remove the dc component unless drift removal is specified
    frequency = f[fft_indicies] # cut the frequency base

    return frequency, fft_indicies, nx

def fft_gen(fft_indicies,y,nx):
# Function to generate the fast fourier transforms
# Arguments: fft_indicies (indicies for the fast fourier transform) and y (position data), nx = length of dataset
# Returns: the fast fourier transform of the dataset

    fft_y_fourier = np.fft.fft(y) # calc fft
    fft_y = abs(fft_y_fourier) / nx # Calculate fourier transform, remembering to divide by nx
    fft_y = fft_y[fft_indicies]

    return fft_y

def dft_gen(fft_y):
# Function to generate the discrete fourier transforms
# Arguments: fft of y
# Returns: dft of y

    dft_y = 2 * fft_y # double the amplitude as we are only using half the transform
    return dft_y

def csp_gen(y_fft):
# Function to generate the cumulative specrtal power
# Arguments: the fast fourier transfrom of y
# Returns: the csp of the data

    y_psd = 2*(y_fft ** 2) # find the psd
    y_csp = y_psd.cumsum(axis=0) # find the csp

    return y_csp, y_psd

def ibm_gen(y_psd):
# Function to generate the integrated beam motion
# Arguments: the psd of y
# Returns: the ibm of y

    y_ibm = (y_psd.cumsum(axis=0))**(0.5)
    return y_ibm

def hann_gen(y):
# Function to generate the Hann Windowed data
# Arguments:  y (position data)
# Returns: the windowed y data

    # Apply the Hann Window:
    y_hann = y * np.hanning(len(y))
    y_hann_power_scale = np.sqrt((np.sum(y ** 2)) / np.sum(y_hann ** 2))
    yy_hann = y_hann * y_hann_power_scale

    return yy_hann


# Plotting Functions (these are only used here for testing, Analysis Grpaher has its own complex plotting and processing fucntions):
def plot_generate_DFT(f,y_dft):
# Function to plot the discrete fourier transform on a semilog scale
# Arguments frequency base, the discrete fourier transform of the data set
    plt.semilogx(f,y_dft)
    #plt.semilogx(f,y_dft, '--b', marker = mpath.Path.unit_circle(), markersize = 2)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Discrete Fourier transform of beam position, y[\u03bcm, /Hz]")
    plt.title('Discrete Fourier Transform')
    plt.show()

def plot_generate_CSP(title):
# Function to plot the cumulative spectral power on a semilog scale
# Arguments frequency base, the cumulative spectral power of the data set
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Cumulative Spectral Power %s, [\u03bcm^2]"%title)
    plt.title('CSP')
    plt.grid()
    plt.legend()
    plt.show()

def plot_generate_IBM(f,y_ibm):
# Function to plot the integrated beam motion on a semilog scale
# Arguments frequency base, the integrated beam motion of the data set
    plt.semilogx(f,y_ibm)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Integrated Beam Motion, [\u03bcm]")
    plt.title('Integrated Beam Motion')
    plt.grid()
    plt.show()


def create(x,y, win, return_type):
# Function to create the fft, dft, csp, ibm values for future plotting
# Arguments: any x and y from a capture, win = toggle if you want the Hann window or not return_type: Based on the graph you want to display, what calculation do you want returned
# Returns: the values of what you want to create:
#       0: DFT
#       1: CSP
#       2: CSP Proportional (wrt noise level)
#       3: IBM
    
    # Generate the frequency base first of all
    frequency, fft_indicies, nx = frequency_base_gen(x,y,5) # 5 is the default for removal of DC drift as determiend experimetnally. This can be edited here if needed
    
    # Apply the window if the toggle is enabled
    if (win == 1):
        yy_hann = hann_gen(y)
        y = yy_hann

    # Generate fft:
    y_fft = fft_gen(fft_indicies,y,nx)
    # Generate dft: 
    y_dft= dft_gen(y_fft)

    # Generate CSP:
    y_csp, y_psd = csp_gen(y_fft)

    # Generate normalised CSP:
    variance = y_csp[-1] # last point in the csp
    y_csp_norm = y_csp / variance

    # Generate IBM:
    y_ibm = ibm_gen(y_psd)

    # Check what you want returned:
    if (return_type == 0):
        return frequency, y_dft
    elif (return_type == 1):
        return frequency, y_csp
    elif (return_type == 2):
        return frequency, y_csp_norm
    else:
        return frequency, y_ibm


