READ ME FILE for X-Ray Diagnostics Triggering system ofr DLS Diagnostics Team
Created by Summer Student 2021, Codrutza Dragu, University of Oxford

''' This software package is made to communicate with TetrAMM and MantaCam software via the EPICS pvs '''

Pre-Requisites:
    Virtual Environment witht the fillowing pipinstalls:
    - [packages]
        h5py = "*"
        cothread = "*"
        matplotlib = "*"
        pyqt5 = "*"
        scipy = "*"
        mpld3 = "*"

    - [python version]
        #python_version = "3.7"

    Access to EPICS gui and IOcs for the MantaCam and the TetrAMM

Files in this package:
    Main files to be run from Terminal:
        - Main_Experiment_Set_Up.py
            This file runs the secquence of set up GUIs in order. 
            It calls Set_Up_Main, Set_Up_TetrAMM,Set_Up_Camera, Set_Up_Diagnostics_Hybrid, Set_Up_Beamline, Set_Up_Beamline_Schematic GUI packages#
            This file also imports the TertAMM and MantaCam object classes

        - Main_Data_Converter_Set_Up.py
            This file runs the script to convert the hdf5 files into .mat files for future anlaysis
            It calls Set_Up_DataConverter

        - Main_Analysis_Set_Up.py
            This file runs the script to produce the analysis gui and perform the different kinds of anlaysis required
            It calls Set_Up_Analysis_GUI

    Set_Up_GUI files:
        - Set_Up_Main.py
            This script generates a GUI to allow the users to select the harware that they want to use on the beamaline
        
        - Set_Up_TetrAMM.py 
            This script sets up the TetrAMM objects and the HDF5 portion of the GUI

        - Set_Up_MantaCam.py
            This script sets up the MantaCam objects and the HDF5 portion of the GUI

        - Set_Up_Beamline.py
            This script allows you to choose the beamline that you want to use. The pv of the topup for any beamline is already displayed on the GUI#

        - Set_Up_Beamline_Schematic.py
            This script allows you to drag and drop hardware along the beamline positions available

        - Set_Up_Diagnostics_Hybrid.py
            This script manages the experiment part of the triggering. It is an updating interface that displays any errors with the hardware and file saving, 
            and also allows you to start the hardware's HDF acquire feature, stop it, reset the hardware and interface, and produce a metadata mat file
            which is needed for upload in the anlaysis GUIs

        - Set_Up_DataConverter.py
            This script converts the hdf5 files into .mat files for easier data access after the experimetn is done. 
            It already performs stitching and 2D gaussian fitting, but does not perform the anlaysis yet

        - Set_Up_Analysis_Gui.py
            This script uses the Info.mat file produced during the experiment and the .mat files created from the Data Converter to produce any graph that the user wants
    


