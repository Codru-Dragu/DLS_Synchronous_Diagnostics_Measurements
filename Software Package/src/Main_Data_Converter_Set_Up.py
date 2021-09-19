''' FILE TO RUN FROM PYTHON TERMINAL, RUNS THE DATA CONVERTING GUI '''

# IMPORTS #
import Set_Up_DataConversion as sudc
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


# FUNCTIONS + WINDOWS CALLED #

''' Set up the Main Application Object '''
app = QApplication(sys.argv) # must execute after each window

''' Main Set Up window of the data converter ''' 
# Call the UI
process_data = sudc.Data_Convertor()
process_data.show()
# Execute the UI
app.exec_()