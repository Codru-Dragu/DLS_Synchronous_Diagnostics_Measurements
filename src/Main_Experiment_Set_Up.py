''' FILE TO RUN FROM PYTHON TERMINAL, RUNS THE MAIN SEQUENCE OF GUIS IN ORDER TO SET UP AND CONDUCT EXPERIMENT '''

# IMPORTS #
import Set_Up_Main as sumain
import Set_Up_TetrAMM as sutet
import Set_Up_Camera as sucam
import Set_Up_Diagnostics_Hybrid as sudiag
import Set_Up_Beamline as subeam
import Set_Up_Beamline_Schematic as suschem

import TetrAMM as T
import MantaCam as MC

import cothread
from cothread.catools import *
import h5py
import time

import sys 

from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase

# VARIABLES #

# Set Default values to be updated
number_tet = 0
number_cam = 0
filepath = ' '

# FUNCTIONS + WINDOWS CALLED #

''' Set up the Main Application Object '''
app = QApplication(sys.argv) # must execute after each window

''' Main Set Up window where the number of hardware is specified ''' 
# Call the UI
choose_hardware = sumain.Hardware_Setup()
choose_hardware.show()
# Execute the UI
app.exec_()

# At the end of execution Get the number of tetramm and camera values
n_tet, n_cam = choose_hardware.get_output()
number_tet = int(n_tet)
number_cam = int(n_cam)

''' ''' ''' '''

''' TetrAMM Set Up window(s) '''
# First creat an empty seconds variable that will be changed later
seconds = 0
# First, create an empty array for the tetramms
tet_dict = []

# Function to create tetramms:
def create_tet_GUI(current_tet, total_tet):
    global seconds
    # Call the UI
    set_tet = sutet.Tetramm_Setup(current_tet+1, total_tet)
    set_tet.show()
    # Execute the UI
    app.exec_()
    # At the end of the execution, Get the QLine Edit values to populate the tetramm object
    pv_text, qe1, hdf = set_tet.get_output()

    # If this is the first TetrAMM, alter the default values of the whole class:
    if(current_tet == 0):
        T.TetrAMM.values_per_reading = int(qe1[0])
        T.TetrAMM.averaging_time = float(qe1[1])

        T.TetrAMM.number_capture = int(hdf[4])
        T.TetrAMM.file_format = hdf[2]

        # Set the seconds:
        seconds = int(hdf[3])

    # Next, create a TetrAMM Object, which will be automatically initialised
    tet_dict.append(T.TetrAMM(pv_text,hdf[0],hdf[1])) # filepath = hdf[0], filename = hdf[1]
        
# Based on the number of tetramms, loop this:
for i in range(0,number_tet):
    # Create the Tetramm
    create_tet_GUI(i,number_tet)

''' ''' ''' '''

''' Camera Set Up window(s) '''
# First, create an empty array for the cameras
cam_dict = []

# Function to create camera:
def create_cam_GUI(current_cam, total_cam):
    global seconds
    # Call the UI
    set_cam = sucam.Camera_Setup(current_cam+1, total_cam)
    set_cam.show()
    # Execute the UI
    app.exec_()

    # Once execution is done, Get the QLine Edit values to populate the camera object
    pv_text, qe1, hdf = set_cam.get_output()

    # If this is the first Camera, alter the default values of the whole class:
    if(current_cam == 0):
        MC.MantaCam.gain = float(qe1[0])
        MC.MantaCam.binning_x = int(qe1[1])
        MC.MantaCam.binning_y = int(qe1[2])
        MC.MantaCam.reg_start_x = int(qe1[5])
        MC.MantaCam.reg_start_y = int(qe1[6])
        MC.MantaCam.reg_size_x = int(qe1[3])
        MC.MantaCam.reg_size_y = int(qe1[4])
        MC.MantaCam.acq_period = qe1[7]
        MC.MantaCam.exposure =  qe1[8]
        MC.MantaCam.number_capture = int(hdf[4])
        MC.MantaCam.file_format = hdf[2]
        MC.MantaCam.frames_per_second = int(hdf[5])
        seconds = int(hdf[3])

    # Next, create a TetrAMM Object, which will be automatically initialised
    cam_dict.append(MC.MantaCam(pv_text,hdf[0],hdf[1])) # filepath = hdf[0], filename = hdf[1]
        
# Based on the number of cameras, loop this, creating cam objects and the modals for the diagnostics gui:
for i in range(0,number_cam):
    # Create the Tetramm
    create_cam_GUI(i,number_cam)

''' ''' ''' '''

''' Beamline Set up Windows '''
# Call the UI
set_beam = subeam.Beamline_Setup()
set_beam.show()
# Execute the UI
app.exec_()

# At the end of execution get the beamline number and the topup_pv
b_num, topup_pv = set_beam.get_output()

# Next, call the schematic creator UI
set_schem = suschem.MainWindow(tet_dict,cam_dict)
set_schem.show()
# Execute the UI
app.exec_()

# There is no output, but the png imagbe BeamSchemAnno will be called by the diagnostics file

''' ''' ''' '''

''' Main Diagnostics Page '''
# First, create an array of widget display objects which will be passed to the scroll area:
# Set up empty arrays to hold the widgets 
t_widgets= []
c_widgets= []

# TetrAmms:
for i in range(0,number_tet):
    # Get the TetrAMM object values
    device_name = tet_dict[i].file_name
    device_type = 0 # 0 is for TetrAMMS
    # Create a widget object of that Tetramm:
    widg_obj = sudiag.Hardware_Device(device_name,device_type)
    # Append it to the tet_object array
    t_widgets.append(widg_obj)

# Cameras:
for i in range(0,number_cam):
    # Get the TetrAMM object values
    device_name = cam_dict[i].file_name
    device_type = 1 # 0 is for Cameras
    # Create a widget object of that Camera:
    widg_obj = sudiag.Hardware_Device(device_name,device_type)
    # Append it to the tet_object array
    c_widgets.append(widg_obj)


# Now that you have all the widget objects, create the diagnostics with the required objects
main_layout= sudiag.MainLayout(t_widgets, c_widgets, tet_dict, cam_dict,seconds,b_num,topup_pv)
diagnostics = sudiag.MainWindow(main_layout)
diagnostics.show()
# Execute the UI
sys.exit(app.exec_())


# End of experimental set up sequence