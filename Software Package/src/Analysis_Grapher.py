# IMPORTS #
import Fourier_Analysis as fa
import matplotlib.pyplot as plt
import scipy.io as sio
import mpld3
import numpy as np
import time
import os
import datetime
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D

# VARIABLES #
hw_names = ['Tetty', 'Cammy'] # Names of the hardware you want to analyze 
capture_file = 19 # The number of the file you want to analyze
cap_range_min = 0   # Min and max range for a range of flies - this will be inclusive, so must add one in the code
cap_range_max = 1
total_files = 3      # The total number of files there are
linee = ' '         # Lable placeholder
file_path = '/dls/science/groups/vibration/20210722_i18/mfiles_test'

# FUNCTIONS #

# Graph Type Fucntions:
# A – Single Plot, Single Position, Single Hardware. Can have multiple data files
def sp_sp_sh(hw, thisfig, thisax, iter, capture_options, graph_options, analysis_options, stacked_options):
# Function to process single position (x or y), single hardware, for one plot
# Arguments: hw (name of the single hardware), thisfig (respective figure), thisax (respective axis on the figure), capture_options, graph_options, analysis_options, stacked_options --> see help document for number codes
# Rturns for the plotting funtion: hw, thisfig, thisax, analysis_options, graph_options 
    # Global Variables:
    global capture_file
    global cap_range_min
    global cap_range_max
    global total_files
    global file_path

    # Initialise empty array to store the mean values if required:
    mean_store = []
   
    # Next, determine how many data files should be analyzed 
    capture_determine(capture_options, iter) # Automatically updates max and min global variables
   
    # Now, do a for loop to loop through the data and extract the data required:
    
    # First, extract the x_axis values for the single hardware
    xaxis_dict = {} # dict of the X axis values for the hardware
    sio.loadmat('%s/XAxis.mat'%file_path, mdict=xaxis_dict)
    # Extract the x_axis linspace value for the array that you want
    x_axis = xaxis_dict[hw][0]

    for w in range(cap_range_min, cap_range_max):

        # Load Files into dict
        matdict = {} # Dict of the matlab files with the data
        cnum = "%04d"%w
        sio.loadmat('%(c)s/%(a)s_%(b)s.mat'%{"a" : hw, "b" : cnum, 'c': file_path}, mdict=matdict)

        # Depending on which position value is wanted, choose x or y:
        pos, pos_label = graph_determine(graph_options,matdict)

        # Now, use the fourier anlaysis 'create' function to caluclate the transform that is wanted as specified by the user:
        f,y = anlaysis_determine(analysis_options,x_axis,pos)

        # Then, check whether the graph needs to display an average, and if so, plot here as the lines need to be thinner
        if((capture_options ==2) or (capture_options ==3)):
            # Plot Thin dotted lines
            thisax.semilogx(f,y,color = 'black',linewidth=0.5,linestyle=':', label='_%s'%cnum)
            mean_store.append(np.array(y))
        elif (capture_options == 4): # Plot only the average, don't plot anything else
            mean_store.append(np.array(y))
        elif (capture_options == 0): # Only 1 file
            if(stacked_options == 0): # Not stacked
                thisax.semilogx(f,y,label= '_%s'%cnum)
            else: # stacked
                thisax.semilogx(f,y,label= '%(a)s_%(b)s_%(c)s'%{"a" : hw, "b" : cnum, 'c': pos_label})
        else: # Do not make lines thin and dotted, keep them default thickness and dont label them
            if(stacked_options == 0): # Not stacked
                thisax.semilogx(f,y,label= '_%s'%cnum)
            else: # stacked
                thisax.semilogx(f,y,label= '%(a)s_%(b)s_%(c)s'%{"a" : hw, "b" : cnum, 'c' : pos_label})
        
    # At the end of the for loop, determine wheather the mean line should be added and if so, add it!
    if((capture_options ==2) or (capture_options ==3) or (capture_options == 4)):
        # Calculate the Mean
        meanned = np.mean(mean_store, axis = 0)
        thisax.semilogx(f,meanned, label='%(a)s_Average_%(b)s'%{'a':hw, 'b':pos_label}, color='purple')

    # Call plotting code outside of funciton, but return necessary values:
    return hw, thisfig, thisax, analysis_options, graph_options
            
# B -- Single Plot, Single Position, Multiple Hardware
def sp_sp_mh(hw_names, thisfig, thisax, capture_options, graph_options, analysis_options, stacked_options):
# Function to process single position (x or y), multipleS hardware, for one plot
# Arguments: hw (name of the single hardware), thisfig (respective figure), thisax (respective axis on the figure), capture_options, graph_options, analysis_options, stacked_options --> see help document for number codes
# Rturns for the plotting funtion: hw, thisfig, thisax, analysis_options, graph_options    
    # Global Variables:
    global capture_file
    global cap_range_min
    global cap_range_max
    global total_files
    global file_path

    # hw_names stores multiple hardwares. We need to assign a color to each and loop through them:
    color_list = ['black', 'blue', 'red', 'green', 'orange', 'pink', 'purple']

    # Now, loop through each processing code
    for p in range(0,len(hw_names)):
        # Get the hardware name:
        hw = hw_names[p]

        # Initialise empty array to store the mean values if required:
        mean_store = []

        # Next, determine how many data files should be analyzed 
        capture_determine(capture_options) # Automatically updates max and min global variables
    
        # Now, do a for loop to loop through the data and extract the data required:
        
        # First, extract the x_axis values for the single hardware
        xaxis_dict = {} # dict of the X axis values for the hardware
        sio.loadmat('%s/XAxis.mat'%file_path, mdict=xaxis_dict)
        # Extract the x_axis linspace value for the array that you want
        x_axis = xaxis_dict[hw][0]

        for w in range(cap_range_min, cap_range_max):
            # Load Files into dict
            matdict = {} # Dict of the matlab files with the data
            cnum = "%04d"%w
            sio.loadmat('%(c)s/%(a)s_%(b)s.mat'%{"a" : hw, "b" : cnum, 'c': file_path}, mdict=matdict)

            # Depending on which position value is wanted, choose x or y:
            pos, pos_lab = graph_determine(graph_options,matdict)

            # Now, use the fourier anlaysis 'create' function to caluclate the transform that is wanted as specified by the user:
            f,y = anlaysis_determine(analysis_options,x_axis,pos)

            # Then, check whether the graph needs to display an average, and if so, plot here as the lines need to be thinner
            if((capture_options ==2) or (capture_options ==3)):
                # Plot Thin dotted lines
                thisax.semilogx(f,y,color = color_list[p],linewidth=0.5,linestyle=':', label='_%s'%cnum)
                mean_store.append(np.array(y))
            elif(capture_options == 4): # Plot only the avaerage, don't plot the others
                mean_store.append(np.array(y))
            else: # Do not make lines thin and dotted, keep them default thickness and label them
                # Check if this is the first iteration, if so, lable this accordingly
                if (w == cap_range_min):
                    # If this is stacked graph, add whether it is X or Y
                    if(stacked_options == 0): # Not stacked
                        thisax.semilogx(f,y,color = color_list[p],label= '%s'%hw_names[p])
                    else: # stacked
                        thisax.semilogx(f,y,color = color_list[p],label= '%(a)s_%(b)s'%{'a': hw_names[p], 'b': pos_lab})
                else: # if this is not the first iteration, lable with the number
                    thisax.semilogx(f,y,color = color_list[p],label= '_%(a)s_%(b)s'%{"a" : hw_names[p], "b" : cnum})
                
        # At the end of the for loop, determine wheather the mean line should be added and if so, add it!
        if((capture_options ==2) or (capture_options ==3) or (capture_options==4)):
            # Calculate the Mean
            meanned = np.mean(mean_store, axis = 0)
            if (stacked_options == 0): # not stacked
                thisax.semilogx(f,meanned, label='%s'%hw_names[p], color = color_list[p],linewidth=2)
            else: # Stacked
                thisax.semilogx(f,meanned, label='%(a)s_%(b)s'%{'a': hw_names[p], 'b' : pos_lab}, color = color_list[p],linewidth=2)

    # Call plotting code outside of funciton, but return necessary values:
    return hw, thisfig, thisax, analysis_options, graph_options
                     
# C – Single Plot, Double Position, Single Hardware
def sp_dp_sh(hw, thisfig, thisax, capture_options, graph_options,analysis_options): # Graph options default = 2
# Function to process double position (x and y), single hardware, for one plot
# Arguments: hw (name of the single hardware), thisfig (respective figure), thisax (respective axis on the figure), capture_options, graph_options, analysis_options, stacked_options --> see help document for number codes
# Rturns for the plotting funtion: hw, thisfig, thisax, analysis_options, graph_options    
    # Global Variables:
    global capture_file
    global cap_range_min
    global cap_range_max
    global total_files
    global file_path

    # Initialise empty array to store the mean values if required:
    mean_store_x = []
    mean_store_y = []

    # Then, set the color scheme array:
    color = ['blue', 'red']
   
    # Next, determine how many data files should be analyzed 
    capture_determine(capture_options) # Automatically updates max and min global variables
   
    # Now, do a for loop to loop through the data and extract the data required:
    
    # First, extract the x_axis values for the single hardware
    xaxis_dict = {} # dict of the X axis values for the hardware
    sio.loadmat('%s/XAxis.mat'%file_path, mdict=xaxis_dict)
    # Extract the x_axis linspace value for the array that you want
    x_axis = xaxis_dict[hw][0]

    for w in range(cap_range_min, cap_range_max):
        # Load Files into dict
        matdict = {} # Dict of the matlab files with the data
        cnum = "%04d"%w
        sio.loadmat('%(c)s/%(a)s_%(b)s.mat'%{"a" : hw, "b" : cnum, "c": file_path}, mdict=matdict)

        # Both x and Y position Data is wanted, therefore:
        posx, pos_x_label = graph_determine(0,matdict) # x data
        posy, pos_y_label = graph_determine(1,matdict) # y data

        # Now, use the fourier anlaysis 'create' function to caluclate the transform that is wanted as specified by the user:
        fx,yx = anlaysis_determine(analysis_options,x_axis,posx)
        fy,yy = anlaysis_determine(analysis_options,x_axis,posy)

        # Then, check whether the graph needs to display an average, and if so, plot here as the lines need to be thinner
        if((capture_options ==2) or (capture_options ==3)):
            # Plot Thin dotted lines
            thisax.semilogx(fx,yx,color = color[0],linewidth=0.5,linestyle=':', label='_X_%s'%cnum)
            thisax.semilogx(fy,yy,color = color[1],linewidth=0.5,linestyle=':', label='_Y_%s'%cnum)
            mean_store_x.append(np.array(yx))
            mean_store_y.append(np.array(yy))
        elif (capture_options == 4): # Plot only the average, don't plot anything else
            mean_store_x.append(np.array(yx))
            mean_store_y.append(np.array(yy))
        elif (capture_options == 1):
            # Do not plot all of the labels in the legend except for the first set of lines. Make the rest insivisble with _
            if(w == cap_range_min):
                thisax.semilogx(fx,yx,color = color[0],label= 'X')
                thisax.semilogx(fy,yy,color = color[1],label= 'Y') 
            else:               
                thisax.semilogx(fx,yx,color = color[0],label= '_X_%s'%cnum)
                thisax.semilogx(fy,yy,color = color[1],label= '_Y_%s'%cnum)
        else: # Do not make lines thin and dotted, keep them default thickness and label them
            thisax.semilogx(fx,yx,color = color[0],label= 'X_%s'%cnum)
            thisax.semilogx(fy,yy,color = color[1],label= 'Y_%s'%cnum)
        
    # At the end of the for loop, determine wheather the mean line should be added and if so, add it!
    if((capture_options ==2) or (capture_options ==3) or (capture_options == 4)):
        # Calculate the Mean
        meanned_x = np.mean(mean_store_x, axis = 0)
        meanned_y = np.mean(mean_store_y, axis = 0)
        thisax.semilogx(fx,meanned_x, label='Average_X', color=color[0])
        thisax.semilogx(fy,meanned_y, label='Average_Y', color=color[1])

    # Call plotting code outside of funciton, but return necessary values:
    return hw, thisfig, thisax, analysis_options, graph_options

# Grph type D: D – Single Plot, Double Position, Multiple Hardware
def sp_dp_mh(hw_names, thisfig, thisax, capture_options, graph_options,analysis_options): # Graph options default = 2
# Function to process multiple position (x and y), multipleS hardware, for one plot
# Arguments: hw (name of the single hardware), thisfig (respective figure), thisax (respective axis on the figure), capture_options, graph_options, analysis_options, stacked_options --> see help document for number codes
# Rturns for the plotting funtion: hw, thisfig, thisax, analysis_options, graph_options   
    # Global Variables:
    global capture_file
    global cap_range_min
    global cap_range_max
    global total_files
    global file_path

    # Then, set the color scheme array:
    color = ['blue', 'red']
    # hw_names store multip;e hardwares so we need linestyle scheme:
    line_type = ['-', ':', '--', '-.']

    # Now loop through each processing code
    for p in range(0,len(hw_names)):
        # Get the hardware name:
        hw = hw_names[p]

        # Initialise empty array to store the mean values if required:
        mean_store_x = []
        mean_store_y = []
    
        # Next, determine how many data files should be analyzed 
        capture_determine(capture_options) # Automatically updates max and min global variables
    
        # Now, do a for loop to loop through the data and extract the data required:
        
        # First, extract the x_axis values for the single hardware
        xaxis_dict = {} # dict of the X axis values for the hardware
        sio.loadmat('%s/XAxis.mat'%file_path, mdict=xaxis_dict)
        # Extract the x_axis linspace value for the array that you want
        x_axis = xaxis_dict[hw][0]

        for w in range(cap_range_min, cap_range_max):
            # Load Files into dict
            matdict = {} # Dict of the matlab files with the data
            cnum = "%04d"%w
            sio.loadmat('%(c)s/%(a)s_%(b)s.mat'%{"a" : hw, "b" : cnum, 'c': file_path}, mdict=matdict)

            # Both x and Y position Data is wanted, therefore:
            posx, x_lab = graph_determine(0,matdict) # x data
            posy, y_lab = graph_determine(1,matdict) # y data

            # Now, use the fourier anlaysis 'create' function to caluclate the transform that is wanted as specified by the user:
            fx,yx = anlaysis_determine(analysis_options,x_axis,posx)
            fy,yy = anlaysis_determine(analysis_options,x_axis,posy)

            # Then, check whether the graph needs to display an average, and if so, plot here as the lines need to be thinner
            if((capture_options ==2) or (capture_options ==3)):
                # Plot Thin dotted lines
                thisax.semilogx(fx,yx,color = color[0],linewidth=0.3,linestyle=line_type[p], label='_%(a)s_X_%(b)s'%{'a': hw, 'b': cnum})
                thisax.semilogx(fy,yy,color = color[1],linewidth=0.3,linestyle=line_type[p], label='_%(a)s_Y_%(b)s'%{'a': hw, 'b': cnum})
                mean_store_x.append(np.array(yx))
                mean_store_y.append(np.array(yy))
            elif (capture_options == 4): # Plot only the average, don't plot anything else
                mean_store_x.append(np.array(yx))
                mean_store_y.append(np.array(yy))
            elif (capture_options == 1):
                # Do not plot all of the labels in the legend except for the first set of lines. Make the rest insivisble with _
                if(w == cap_range_min):
                    thisax.semilogx(fx,yx,color = color[0],label= '%s_X'%hw,linestyle= line_type[p])
                    thisax.semilogx(fy,yy,color = color[1],label= '%s_Y'%hw,linestyle=line_type[p]) 
                else:               
                    thisax.semilogx(fx,yx,color = color[0],label='_%(a)s_X_%(b)s'%{'a': hw, 'b': cnum},linestyle=line_type[p])
                    thisax.semilogx(fy,yy,color = color[1],label='_%(a)s_Y_%(b)s'%{'a': hw, 'b': cnum},linestyle=line_type[p])
            else: # Do not make lines thin and dotted, keep them default thickness and label them
                thisax.semilogx(fx,yx,color = color[0],label='%(a)s_X_%(b)s'%{'a': hw, 'b': cnum},linestyle=line_type[p])
                thisax.semilogx(fy,yy,color = color[1],label='%(a)s_Y_%(b)s'%{'a': hw, 'b': cnum},linestyle=line_type[p])
            
        # At the end of the for loop, determine wheather the mean line should be added and if so, add it!
        if((capture_options ==2) or (capture_options ==3) or (capture_options == 4)):
            # Calculate the Mean
            meanned_x = np.mean(mean_store_x, axis = 0)
            meanned_y = np.mean(mean_store_y, axis = 0)
            thisax.semilogx(fx,meanned_x, label='Average_X_%s'%hw, color=color[0],linestyle = line_type[p])
            thisax.semilogx(fy,meanned_y, label='Average_Y_%s'%hw, color=color[1], linestyle = line_type[p])

    # Call plotting code outside of funciton, but return necessary values:
    return hw, thisfig, thisax, analysis_options, graph_options


# Plotting Fucntions:
def single_graph_plotter(title_type,hw, figure, axis, analysis_options, graph_options):
# Plotting function for graphs A - D (single plots, aka no subplots)
# Arguments: title_type (0 for single hardware, 1 for multiple hardware, determines whether the name of the hardware is shown in the title), figure (respective figure), axis (respective axis), analysis_options, graph_options --> see help document
# Returns: No returns, graph is plotted  
    # Based on the type of analysis required, make the title, axis, and legend:

    if (graph_options == 0): # pos x
        pos_string = 'Horizontal Motion'
    elif (graph_options == 1): # pos y
        pos_string = 'Vertical Motion'
    else: # graph options is both (2)
        pos_string = 'Horizontal and Vertical Motion'

    if (analysis_options == 0): # Dft
        axis.set_xlabel("Frequency [Hz]")
        axis.set_ylabel("DFT,[\u03bcm√Hz]")

        if(title_type == 0): # only 1 hardware
            axis.set_title('Discrete Fourier Transform of %(a)s, %(b)s'%{"a" : pos_string, "b" : hw})
        else: # multiple harwares
            axis.set_title('Discrete Fourier Transform of %s'%pos_string)

        axis.grid()
        axis.legend(frameon=False)
        figure.canvas.mpl_connect('motion_notify_event', line_hover)  

    elif (analysis_options == 1): # Csp
        axis.set_xlabel("Frequency [Hz]")
        axis.set_ylabel("CSP, [\u03bcm^2]")

        if(title_type == 0): # only 1 hardware
            axis.set_title('Cumulative Spectral Power of %(a)s, %(b)s'%{"a" : pos_string, "b" : hw})
        else: # multiple harwares
            axis.set_title('Cumulative Spectral Power of %s'%pos_string)

        axis.grid()
        axis.legend(frameon=False)
        figure.canvas.mpl_connect('motion_notify_event', line_hover)

    elif (analysis_options == 2): # CSP_N
        axis.set_xlabel("Frequency [Hz]")
        axis.set_ylabel("Normalised CSP")

        if(title_type == 0): # only 1 hardware
            axis.set_title('Realtive Cumulative Spectral Power of %(a)s, %(b)s'%{"a" : pos_string, "b" : hw})
        else: # multiple harwares
            axis.set_title('Relative Cumulative Spectral Power of %s'%pos_string)

        axis.grid()
        axis.legend(frameon=False)
        figure.canvas.mpl_connect('motion_notify_event', line_hover)

def stacked_graph_plotter(iteration_plotter,hw, figure, axis, analysis_options, graph_options):
# Plotting function for graphs G-H (multiple subplots on the same figure)
# Arguments: itheration_plotter (0 for the first subplot iter, 1 for the rest, sets title here and is the axis which the rest follow the scale for), figure (respective figure), axis (respective axis), analysis_options, graph_options --> see help document
# Returns: No returns, graph is plotted 
    # Based on the type of analysis required, make the title, axis, and legend:

    if (graph_options == 0): # pos x
        pos_string = 'Horizontal Motion'
    elif (graph_options == 1): # pos y
        pos_string = 'Vertical Motion'
    else: # graph options is both (2)
        pos_string = 'Horizontal and Vertical Motion'

    if (analysis_options == 0): # Dft
        axis.set_xlabel("Frequency [Hz]")
        axis.set_ylabel("DFT,[\u03bcm√Hz]")

        if(iteration_plotter == 0): # the first iteration - set the title here and the axis to follow the scale for 
            figure.suptitle('Discrete Fourier Transform of %s'%pos_string)
 
        axis.grid()
        axis.legend(frameon=False)
        figure.canvas.mpl_connect('motion_notify_event', line_hover)  

    elif (analysis_options == 1): # Csp
        axis.set_xlabel("Frequency [Hz]")
        axis.set_ylabel("CSP, [\u03bcm^2]")

        if(iteration_plotter == 0): # the first iteration - set the title here and the axis to follow the scale for 
            figure.suptitle('Cumulative Spectral Power of %s'%pos_string)

        axis.grid()
        axis.legend(frameon=False)
        figure.canvas.mpl_connect('motion_notify_event', line_hover)

    elif (analysis_options == 2): # CSP_N
        axis.set_xlabel("Frequency [Hz]")
        axis.set_ylabel("Normalised CSP")

        if(iteration_plotter == 0): # the first iteration - set the title here and the axis to follow the scale for 
            figure.suptitle('Relative Cumulative Spectral Power of %s'%pos_string)

        axis.grid()
        axis.legend(frameon=False)
        figure.canvas.mpl_connect('motion_notify_event', line_hover)

# Caluclation Functions: 
def capture_determine(capture_options, iter=0):
# Function to determine the type of capture option required and to set the range as specified
# Arguments: capture_options numerical value - see document
# Returns: None, but will alter the global cap_range_min and max values accordingly
    global cap_range_max
    global cap_range_min
    global capture_file

    if(capture_options == 0): # Only 1 file 
        # Set the file to be the cap_range_min:
        cap_range_min = capture_file
        cap_range_max = capture_file+1
    # If capture option is a range of files (averaged or unaveraged) or all the files:
    elif(capture_options == 3) or (capture_options == 4): # All the files, so make the range span all the available files
        cap_range_min = 0
        cap_range_max = total_files
    # if capture_options == 1 or 2 (averaged or unaveraged range), the cap_range_min and cap_range_max will be set by the user
    else:
        if iter == 0:
            cap_range_max = cap_range_max+1 # Make the final value inclusive

def graph_determine(graph_options,matdict):
# Function to retun the position data specified and the title of the data if applicable
# Arguments: the graph option value (see help document), the dict in which all the values are stored
# Returns: the called position data and the title of that data
        if(graph_options == 0): # X data
            return matdict['PosX'][0], 'X'
        elif(graph_options == 1): # graph_options == 1, Y data. 
            return matdict['PosY'][0], 'Y'
        else: # graph_options = 2, both data
            return matdict['PosX'][0], matdict['PosY'][0]
        
def anlaysis_determine(analysis_options, x_axis, pos):
# Fucntion to determine the type of fourier analysis to be performed
# Arguments: the anlaysis option value (see help doc), the x_axis data, the position data
# Returns: After calculating the frequency set and the y value set, it return these two lists for further processing / plotting
    if(analysis_options == 0): #DFT
        f,y = fa.create(x_axis, pos, 1, 0)
    elif(analysis_options == 1): # CSP
        f,y = fa.create(x_axis, pos, 1, 1)
    else: # if anlaysis_options == 2, CSP Normalised 
        f,y = fa.create(x_axis,pos,1, 2) 
    
    return f,y

# Line Hover Fucntions
def line_hover(event):
# Function to get the lable of the line which is hovered over in a plot (works best for single plots)
# Arguments: the event
# Returns: None, but stores the label in the linee palceholder
    global linee
    ax = plt.gca()
    ax.format_coord = format_coord_special
    for line in ax.get_lines():
        if line.contains(event)[0]:
            linee = line.get_label()
       
def format_coord_special(x, y):
# Fucntion to display the label of the selected line in the coordinate bar
# Arguments: the coordinates of the mouse (this is automatically inputted)
# Returns: the coordinates + selected label to be displayed on the graph

    global linee
    return 'x=%1.4f, y=%1.4f, Selected: %s' % (x, y,linee)

# Figure and Axis making functions:
def makefig(fignum):
# Function to make figures and axis for the single plots
# Arguments: the fignum - actually the plotnumber (which should be 1)
# Returns: the current fig and axis
    thisfig, thisax = plt.subplots(fignum)
    return thisfig, thisax

def makefigandaxis(axisnum):
# Fucntion to make the figures and axis with subplot and scale sharing for the stacked plots
# Arguments: the number of subpltos required
# Returns: the figure, the array of axis suplotsS
    fig, axs = plt.subplots(axisnum, sharex= True, sharey= False)
    return fig, axs

def makefigwaterfall():
# Fucntion to make the figures and axis for the 3d waterfall plot
# Arguments: none
# Returns: the figure, the axis    
    fig = plt.figure(figsize = (20,10))
    #fig.subplots_adjust(bottom=-0.3,top=1.9)
    ax = fig.add_subplot(111, projection='3d')
    return fig, ax


# Functions to produce the graphs
def graphA(capture_options, graph_options, analysis_options, stacked_options):
# Function to create the graph for one singe hardware, one signle plot, x or y
# Arguments: array of only 1 hardware name
# Returns: None, but the graph is simply produced
    global hw_names
    # Before anything, initialise the figure of this graph:
    thisfig, thisax = makefig(1)
    hardware_name, figure_name, ax_name, a_option, g_option = sp_sp_sh(hw_names[0],thisfig,thisax,0,capture_options,graph_options,analysis_options,stacked_options)
    # Now, call the function to plot the graph:
    single_graph_plotter(0,hardware_name, figure_name, ax_name, a_option,g_option)
    plt.show()

def graphC(capture_options, graph_options,analysis_options):
# Function to create the graph for one singe hardware, one signle plot, x and y
# Arguments: Array of only 1 hardware name
# Returns: None, but the graph is simply produced    
    global hw_names
    # Before anything, initialise the figure of this graph:
    thisfig, thisax = makefig(1)
    hardware_name, figure_name, ax_name, a_option, g_option = sp_dp_sh(hw_names[0],thisfig,thisax,capture_options, graph_options,analysis_options)
    # Now, call the function to plot the graph:
    single_graph_plotter(0,hardware_name, figure_name, ax_name, a_option,g_option)
    plt.show()

def graphB(capture_options, graph_options, analysis_options, stacked_options):
# Function to create the graph for multiple hardware, one signle plot, x or y
# Arguments: Array of hardware names
# Returns: None, but the graph is simply produced    
    global hw_names
    # Before anything, initialise the figure of this graph:
    thisfig, thisax = makefig(1)
    hardware_name, figure_name, ax_name, a_option, g_option = sp_sp_mh(hw_names,thisfig,thisax,capture_options, graph_options, analysis_options, stacked_options)
    # Now, call the function to plot the graph:
    single_graph_plotter(1,hardware_name, figure_name, ax_name, a_option,g_option)
    plt.show()

def graphD(capture_options, graph_options,analysis_options):
# Function to create the graph for multiple hardware, one signle plot, x andS y
# Arguments: Array of hardware names
# Returns: None, but the graph is simply produced    
    global hw_names
    # Before anything, initialise the figure of this graph:
    thisfig, thisax = makefig(1)
    hardware_name, figure_name, ax_name, a_option, g_option = sp_dp_mh(hw_names,thisfig,thisax,capture_options, graph_options,analysis_options)
    # Now, call the function to plot the graph:
    single_graph_plotter(1,hardware_name, figure_name, ax_name, a_option,g_option)
    plt.show()

def graphF(capture_options, graph_options, analysis_options, stacked_options):
# Function to create the graph for multiple hardware, multiple plot, x or y. This uses the graph A base function 
# Arguments: Array of hardware names
# Returns: None, but the graph is simply produced
    global hw_names
    global cap_range_max
    global cap_range_min
    # Create figure with subplots corresponding to how many hardwares are present
    thisfig, thisax = makefigandaxis(len(hw_names))
    # Then, for each of the hardwares, generate the data and plots
    # Assume that multiple plot, single position, multiple harware
    for r in range(0,len(hw_names)):
        hardware_name, figure_name, ax_name, a_option, g_option = sp_sp_sh(hw_names[r], thisfig, thisax[r],r,capture_options, graph_options, analysis_options, stacked_options)
        stacked_graph_plotter(0,hardware_name, figure_name, ax_name, a_option,g_option)
    plt.tight_layout()
    plt.show()

def graphG(capture_options, graph_options, analysis_options, stacked_options):
# Function to create the graph for single hardware, multiple plot, x and y. This uses the graph A base function 
# Arguments: Array of hardware names
# Returns: None, but the graph is simply produced
    global hw_names
    # Create a figure with 2 subpltos for each position data
    thisfig, thisax = makefigandaxis(2) # an axis for each position data
    # This is only for 1 harware so extract it
    hw = hw_names[0]
    # Then for each of the position data generate the data and the plots
    # Assume mUltiple Plot, double position, single hardware
    for r in range(0,2):
        hardware_name, figure_name, ax_name, a_option, g_option = sp_sp_sh(hw, thisfig, thisax[r], r, capture_options, r, analysis_options, stacked_options)
        stacked_graph_plotter(r,hardware_name, figure_name, ax_name, a_option,2)
    plt.tight_layout()
    plt.show()

def graphH(capture_options, graph_options, analysis_options, stacked_options):
# Function to create the graph for multiple hardware, multiple plot, x and y. This uses the graph A base function 
# Arguments: Array of hardware names
# Returns: None, but the graph is simply produced
    global hw_names
    # Create a figure with 2 subpltos for each position data
    thisfig, thisax = makefigandaxis(2)
    # For each of the positions, make the figure:
    for r in range(0,2):
        hardware_name, figure_name, ax_name, a_option, g_option = sp_sp_mh(hw_names,thisfig,thisax[r],capture_options, r, analysis_options, stacked_options)
        stacked_graph_plotter(r,hardware_name, figure_name, ax_name, a_option,2)
    plt.tight_layout()
    plt.show()
   
def graphWaterfall(graph_options, capture_options, K, interval):
    global hw_names

    # NOTE FOR k: This is the cutoff frequency. If K = 0: that is no cutoff frequency

    # Create the figure and the axis
    thisfig, thisax = makefigwaterfall()

    # Plot everything and retreive tick array
    tstamp_array, X, Y, Z, nonformatted_time =  waterfall_plot(hw_names[0],thisfig,thisax,graph_options, capture_options, K, interval) 
    # X = Frequency, Y = Time , Z = CSP

    # Set Axis requirements
    thisax.auto_scale_xyz(X,Y,Z) # set axis limits to auto
    thisax.set_xlabel("Frequency [Hz]", fontsize =10, labelpad=10) 
    thisax.set_ylabel("Timestamp", fontsize =10, labelpad=60)
    thisax.set_zlabel("CSP, [\u03bcm^2]", fontsize =10, labelpad=35) 

    # Set Ticks:
    thisax.set_yticks(nonformatted_time)
    thisax.set_yticklabels(tstamp_array, rotation = 60)
    thisax.tick_params(axis='z', which='major', pad=15)

    # Rotate
    thisax.view_init(30,40)
    thisax.invert_xaxis()

    # Scale
    scale_x = 0.5
    scale_y = 1
    scale_z = 0.5
    #thisax.get_proj = lambda: np.dot(Axes3D.get_proj(thisax), np.diag([scale_x, scale_y, scale_z, 1]))

    # Set title:
    thisax.set_title('CSP')

    plt.show()


def waterfall_plot(hw, thisfig, thisax, graph_options, capture_options, K, interval):
# Function to process single position (x or y), single hardware, for one plot
# Arguments: hw (name of the single hardware), thisfig (respective figure), thisax (respective axis on the figure), capture_options, graph_options, analysis_options, stacked_options --> see help document for number codes
# Rturns for the plotting funtion: hw, thisfig, thisax, analysis_options, graph_options 
    # Global Variables:
    global capture_file
    global cap_range_min
    global cap_range_max
    global total_files
    global file_path

    # Set option values:
    analysis_options = 1 # CSP
    stacked_options = 0 # Not stacked
   
    # Next, determine how many data files should be analyzed 
    capture_determine(capture_options) # Automatically updates max and min global variables
   
    # Now, do a for loop to loop through the data and extract the data required:
    
    # First, extract the x_axis values for the single hardware
    xaxis_dict = {} # dict of the X axis values for the hardware
    sio.loadmat('%s/XAxis.mat'%file_path, mdict=xaxis_dict)
    # Extract the x_axis linspace value for the array that you want
    x_axis = xaxis_dict[hw][0]

    # Create three arrays for the function to process
    x_arr = [] # frequency
    y_arr = [] # csp
    z = [] # time array
    tstamp_array = [] # Time Stamp Array (for future use)

    for w in range(cap_range_min, cap_range_max):
        # Load Files fromdict
        matdict = {} # Dict of the matlab files with the data
        cnum = "%04d"%w
        sio.loadmat('%(c)s/%(a)s_%(b)s.mat'%{"a" : hw, "b" : cnum, 'c': file_path}, mdict=matdict)

        # Depending on which position value is wanted, choose x or y:
        pos, pos_label = graph_determine(graph_options,matdict)

        # Now, use the fourier anlaysis 'create' function to caluclate the transform that is wanted as specified by the user:
        f,y = anlaysis_determine(analysis_options,x_axis,pos)
        
        # If you dont want processing to take too long, reduce the array to every intervalth point:
        if interval != 0:
            if (interval<(len(f)-1)): # Interval does not go over
                f = f[0::interval]
                y = y[0::interval]

        # NOTE: Get the timestamp:
        # If it has been already appended to the dict:
        tstamp_format = matdict['TSFormat'][0]
        tstamp = matdict['TS'][0][0]

        # K is cutoff frequency, so if there is a cutoff specified:
        if (w == cap_range_min): # if first iteration, append f
            if (K != 0):
                f = [x for x in f if x<= K]
            x_arr.append(f)
        else: # if k = 0
            f = [x for x in f if x<= K]

        if(K != 0):
            y= y[0: len(f)] 

        y_arr.append(y)
        z.append(tstamp)
        tstamp_array.append(tstamp_format)

    # Create MeshGrid 
    X,Y = np.meshgrid(x_arr,z) # time and f

    # Check sizes to loop always over the smallest dimension
    Z = np.array(y_arr) #csp

    # Normalise
    norm = plt.Normalize(Z.min().min(), Z.max().max())

    n,m = Z.shape
    if n>m:
        X=X.T; Y=Y.T; Z=Z.T
        m,n = n,m

    for j in range(n):
        # reshape the X,Z into pairs 
        points = np.array([X[j,:], Z[j,:]]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)        
        lc = LineCollection(segments, cmap='jet', norm = norm)
        # Set the values used for colormapping
        lc.set_array((Z[j,1:]+Z[j,:-1])/2)
        lc.set_linewidth(2) # set linewidth a little larger to see properly the colormap variation
        line = thisax.add_collection3d(lc,zs=(Y[j,1:]+Y[j,:-1])/2, zdir='y') # add line to axes

    
    return tstamp_array, X, Y, Z, z
