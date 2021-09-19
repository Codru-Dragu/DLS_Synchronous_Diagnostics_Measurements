''' FILE TO ALLOW USERS TO CONVER THE HDF5 FILES TO MAT FILES FOR FASTER ANLAYSIS '''
# IMPORTS # 
import sys 

from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QCheckBox, QFileDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
import webbrowser

import scipy.io as sio
import Analysis_Grapher as an

# VARIABLES # 

# FUNCTIONS # 

# Set up the application and stylesheet
def create_app():
# Function to create the application object
# Arguments: None
# Returns: None
    app = QApplication(sys.argv)
    return app

# NOTE: This class is first called to etract the needed information and call the Analysis set up class directly
class Chooser_Setup(QDialog):
# Main Window to upload the info file and the write the file path of the mat files
    def __init__(self, parent=None):
    # Class initialiser for the modal
        super().__init__(parent)
        self.setStyleSheet('''
            QLabel {
                font-size: 27px;
                color: #191970;

            }
            
            #LabelTitle {
                font-size: 50px;
                color: #191970;
                font-weight: bold;
            }

            QDialog {
                background: #B6D0E2;
            }
        
            QComboBox {
                border: 5px solid white;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }

            QComboBox:editable {
                background: white;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;

                border-left-width: 1px;
                border-left-color: lightblue;
                border-left-style: solid; /* just a single line */
                border-top-right-radius: 3px; /* same radius as the QComboBox */
                border-bottom-right-radius: 3px;
            }

            QComboBox::down-arrow {
                image: url("downArrow.png");
                width: 100px;
                padding-left: 3px;
            }
            
            QComboBox QAbstractItemView {
                border: 2px solid darkgray;
                selection-background-color: lightgray;
                background-color: transparent;
                
            }

            QPushButton{
                background-color: #B6D0E2;
                border-style: outset;
                border-width: 5px;
                border-radius: 15px;
                border-color: white;
                font: 20px;
                color: #191970;
                padding: 6px;
            }

            QPushButton::pressed {
                background-color: #A7C7E7;
                border-style: inset;
            }

            QPushButton::disabled {
                background-color: gray;
            }

            #HelpBtn {
                image: url("help.png");
                font: bold 20px;
                width: 30px;
                
            }
            #ChooseBtn {
                background-color: white;
                border-radius: 0px;
                border-color: #191970;
            
            }
            ''')

        self.setWindowTitle(' ') # No title
        self.initUI() # Initialise

    def grab_files(self):
    # Function to open the Info file that is selected
    # Called by the next button, will close the gui and open the next one after the required filepaths are specified
    # Arguments: None
    # Returns: None
        # Open the file first
        self.open_matfile()
        self.hide()
        self.anaysis_gui = Analysis_Setup(self.tet_arr,self.cam_arr,self.total_files,self.location.text()) # Open the analysis tool bar GUI
        self.anaysis_gui.show()
        
    def open_file(self):
    # Function to get the file path of the Info.Mat file
    # Called by the upload file button, will close the gui and open the next one after the required filepaths are specified
    # Arguments: None
    # Returns: None
        self.path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)')
        if self.path != ('', ''): # If the person has input a path
            self.path_chosen = self.path[0] # save this as a self variabel to universal access
            self.chosen_path.setText(self.path_chosen) # update the text field with the file path
        

    def open_matfile(self):
    # Function to open the .mat file and extrat the useful information
    # Called byt he grab_fiels function
    # Arguments: None
    # Returns: None
        self.info_file = {}
        sio.loadmat('%s'%self.path_chosen, mdict=self.info_file) # open the file path
        self.tet_arr = self.info_file['Tet_Hw'][0][0][0][0][2] # The [][][][] is neccessary to access the variables directly, as everything is saved within arrays of arrays
        self.cam_arr = self.info_file['Cam_Hw'][0][0][0][0][2] # NOTE: The actual 'object' isnt really saved, but a list of the self variables of that oject which can be accessed using the fifth []
        self.total_files = self.info_file['Total_Files'][0][0] # The numbers on the fifth [] correspond to the order it was initilaised in the object class (eg. in TetrAMM the first thing initialised was self.pv (accessed by [0]) followed by self.filepath (accessed by [1]) and then self.name (accessed by [2] as shown. See respective class for more details))

    def initUI(self):
    # Main initialiser
        # Layouts
        self.dlgLayout = QVBoxLayout() # Vertical box layout
        # FOrm Layout
        self.formLayout = QFormLayout() # Form format (lables and fields)
        self.btnLayout = QHBoxLayout() # Bottom buttons layout

        self.titleLayout = QVBoxLayout()

        # Add fonts:
        QFontDatabase.addApplicationFont("Landasans_Light.otf")
        QFontDatabase.addApplicationFont("Landasans_Medium.otf")

        self.font_medium = QFont("Landasans Medium")
        self.font_light = QFont("Landasans Ultra Light")

        # Choose File Button Set up
        self.choose_btn = QPushButton()
        self.choose_btn.setText('UPLOAD FILE')
        self.choose_btn.setFont(self.font_light)
        self.choose_btn.setObjectName('ChooseBtn')
        self.choose_btn.clicked.connect(self.open_file)

        # QLineEdit SetUp - location of the saved mat files
        self.location = QLineEdit()

        self.t_label = QLabel(self)
        self.t_label.setText('SELECT INFOFILE: ')
        self.t_label.setFont(self.font_light)
        self.t_label.setAlignment(Qt.AlignCenter)

        self.line_label = QLabel(self)
        self.line_label.setText('FOLDER PATH: ')
        self.line_label.setFont(self.font_light)
        self.line_label.setAlignment(Qt.AlignCenter)

        path_label = QLabel(self)
        path_label.setText('SELECTED FILE: ')
        path_label.setFont(self.font_light)
        path_label.setAlignment(Qt.AlignCenter)

        # QLineEdit SetUp - display path of chosen file
        self.chosen_path = QLineEdit()      
        self.chosen_path.setReadOnly(False) 

        self.formLayout.insertRow(1, self.t_label, self.choose_btn)
        self.formLayout.insertRow(2, path_label, self.chosen_path)
        self.formLayout.insertRow(2, self.line_label, self.location)

        # Initialise button set up
        self.init_btn = QPushButton(self)
        self.init_btn.setText('Grab Files')
        self.init_btn.setFont(self.font_medium)
        self.init_btn.clicked.connect(self.grab_files)

        # Title Setup 
        self.labelTitle = QLabel(self)
        self.labelTitle.setObjectName('LabelTitle')
        self.labelTitle.setText('ANALYSIS')
        self.labelTitle.setFont(self.font_medium)
        self.labelTitle.setAlignment(Qt.AlignHCenter)
        self.labelTitle.setWordWrap(True)

        # Diamond Logo set up
        self.diamond = QLabel(self)
        pixmap = QPixmap('Diamond.png')
        pixmap = pixmap.scaledToHeight(40)
        self.diamond.setPixmap(pixmap)
        self.diamond.setAlignment(Qt.AlignHCenter)
        self.diamond.setObjectName('DiamondLogo')

        # Add the widgets and layouts in the vertical dialogue box

        self.dlgLayout.addWidget(self.diamond)
        self.titleLayout.addWidget(self.labelTitle)
        self.dlgLayout.addLayout(self.titleLayout)

        self.dlgLayout.addLayout(self.formLayout)
        self.dlgLayout.addWidget(self.init_btn)

        # Configure the main window        
        self.setLayout(self.dlgLayout)
        self.setFixedWidth(400)
        self.setFixedHeight(350)
    

class Analysis_Setup(QDialog):
# Main Window for the analysis tool box
    def __init__(self, tet_arr, cam_arr, total_files, folder_location, parent=None):
    # Class initialiser for the modal
    # Argumetns: self, tet_arr: array of tetramm objects, cam_arr: array of camera objects, total_files: the total numbner of mat files, folder location: where there matfiles are located
        super().__init__(parent)

        # Set up the self variables with the acquired arguments (that way they can be accessed by any of the class functions)
        self.tet_arr = tet_arr
        self.cam_arr = cam_arr
        self.total_files = total_files
        self.folder_location = folder_location

        self.setStyleSheet('''
            QLabel {
                font-size: 27px;
                color: #191970;

            }
            
            #LabelTitle {
                font-size: 50px;
                color: #191970;
                font-weight: bold;
            }

            QDialog {
                background: #B6D0E2;
            }
        
            QComboBox {
                border: 5px solid white;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }

            QComboBox:editable {
                background: white;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;

                border-left-width: 1px;
                border-left-color: lightblue;
                border-left-style: solid; /* just a single line */
                border-top-right-radius: 3px; /* same radius as the QComboBox */
                border-bottom-right-radius: 3px;
            }

            QComboBox::down-arrow {
                image: url("downArrow.png");
                width: 100px;
                padding-left: 3px;
            }
            
            QComboBox QAbstractItemView {
                border: 2px solid darkgray;
                selection-background-color: lightgray;
                background-color: transparent;
                
            }

            QPushButton{
                background-color: #B6D0E2;
                border-style: outset;
                border-width: 5px;
                border-radius: 15px;
                border-color: white;
                font: 20px;
                color: #191970;
                padding: 6px;
            }

            QPushButton::pressed {
                background-color: #A7C7E7;
                border-style: inset;
            }

            QPushButton::disabled {
                background-color: gray;
            }

            #HelpBtn {
                image: url("help.png");
                font: bold 20px;
                width: 30px;
                
            }
            #ChooseBtn {
                background-color: white;
                border-radius: 0px;
                border-color: #191970;
            
            }
            QLineEdit[readOnly=\"true\"] {
                background-color: gray;
            }
            ''')

        self.setWindowTitle(' ') # No title
        self.initUI() # Initialise

    # Make the checkboxes be such that only one can be selected for each section
    def uncheck_a(self, state):
    # Analysis Options checkbox code to make only one checkbox at a time selectable and to enable/disable lower options as necessary 
    # Arguments: self, state of the check box (NOTE: this 'state' variable is automatically inputted by pyqt, you do not need to input it)
    # Returns: None 
        # checking if state is checked
        if state == Qt.Checked:
            # if first check box is selected
            if self.sender() == self.a_0: # DFT
                self.analysis_options = 0
                # making other check box to uncheck
                self.a_1.setChecked(False)
                self.a_2.setChecked(False)
                self.a_3.setChecked(False)
                # Renable the boxes disabled by the waterfall plot box the following:
                self.g_2.setEnabled(True) # X and Y
                self.c_0.setEnabled(True) # Single Capture
                self.c_2.setEnabled(True) # Range Avereaged
                self.c_4.setEnabled(True) # Only Avg
                self.s_0.setEnabled(True) # Enable the stacked options
                self.s_1.setEnabled(True)
                # Disable the K value and interval by making them grey and uneditable
                self.k_value.setEnabled(False)
                self.k_value.setStyleSheet(''' QLineEdit{background-color:grey;}''')
                self.k_value.setText(' ')
                self.k_value.setReadOnly(True)
                self.interval.setEnabled(False)
                self.interval.setStyleSheet(''' QLineEdit{background-color:grey;}''')
                self.interval.setText(' ')
                self.interval.setReadOnly(True)
                # Connect the hardware options to it's default function
                for i in range(0,len(self.hw_checkboxes)):
                    self.hw_checkboxes[i].stateChanged.connect(self.check_stacked_h)

            # if second check box is selected
            elif self.sender() == self.a_1: # CSP
                self.analysis_options = 1
                # making other check box to uncheck
                self.a_0.setChecked(False)
                self.a_2.setChecked(False)
                self.a_3.setChecked(False)
                # Renable the boxes disabled by the waterfall plot box the following:
                self.g_2.setEnabled(True) # X and Y
                self.c_0.setEnabled(True) # Single Capture
                self.c_2.setEnabled(True) # Range Avereaged
                self.c_4.setEnabled(True) # Only Avg
                self.s_0.setEnabled(True) # Enable the stacked options
                self.s_1.setEnabled(True)
                # Disable the K value:
                self.k_value.setEnabled(False)
                self.k_value.setStyleSheet(''' QLineEdit{background-color:grey;}''')
                self.k_value.setText(' ')
                self.k_value.setReadOnly(True)
                self.interval.setEnabled(False)
                self.interval.setStyleSheet(''' QLineEdit{background-color:grey;}''')
                self.interval.setText(' ')
                self.interval.setReadOnly(True)
                # Connect the hardware options to it's default function
                for i in range(0,len(self.hw_checkboxes)):
                    self.hw_checkboxes[i].stateChanged.connect(self.check_stacked_h)
  
            # if third check box is selected
            elif self.sender() == self.a_2: # CSP Normalised
                self.analysis_options = 2
                # making other check box to uncheck
                self.a_0.setChecked(False)
                self.a_1.setChecked(False)
                self.a_3.setChecked(False)
                # Renable the boxes disabled by the waterfall plot box the following:
                self.g_2.setEnabled(True) # X and Y
                self.c_0.setEnabled(True) # Single Capture
                self.c_2.setEnabled(True) # Range Avereaged
                self.c_4.setEnabled(True) # Only Avg
                self.s_0.setEnabled(True) # Enable the stacked options
                self.s_1.setEnabled(True)
                # Disable the K value:
                self.k_value.setEnabled(False)
                self.k_value.setStyleSheet(''' QLineEdit{background-color:grey;}''')
                self.k_value.setText(' ')
                self.k_value.setReadOnly(True)
                self.interval.setEnabled(False)
                self.interval.setStyleSheet(''' QLineEdit{background-color:grey;}''')
                self.interval.setText(' ')
                self.interval.setReadOnly(True)
                # Connect the hardware options to it's default function
                for i in range(0,len(self.hw_checkboxes)):
                    self.hw_checkboxes[i].stateChanged.connect(self.check_stacked_h)

            elif self.sender() == self.a_3: # Waterfall
                self.analysis_options = 3
                # making other check box to uncheck
                self.a_0.setChecked(False)
                self.a_1.setChecked(False)
                self.a_2.setChecked(False) 
                # Disable the following:
                self.g_2.setEnabled(False) # X and Y
                self.c_0.setEnabled(False) # Single Capture
                self.c_2.setEnabled(False) # Range Avereaged
                self.c_4.setEnabled(False) # Only Avg
                self.s_0.setEnabled(False) # Disable the stacked options
                self.s_1.setEnabled(False)
                # Enable the K value:
                self.k_value.setEnabled(True)
                self.k_value.setStyleSheet(''' QLineEdit{background-color:white;}''')
                self.k_value.setText('0')
                self.k_value.setReadOnly(False)
                self.interval.setEnabled(True)
                self.interval.setStyleSheet(''' QLineEdit{background-color:white;}''')
                self.interval.setText('0')
                self.interval.setReadOnly(False)
                # Make only 1 hardware selectable
                for i in range(0,len(self.hw_checkboxes)):
                    self.hw_checkboxes[i].stateChanged.connect(self.uncheck_h)

    def uncheck_g(self, state):
    # Graph Options checkbox code to make only one checkbox at a time selectable and to enable/disable lower options as necessary 
    # Arguments: self, state of the check box (NOTE: this 'state' variable is automatically inputted by pyqt, you do not need to input it)
    # Returns: None
            # checking if state is checked
            if state == Qt.Checked:
                # if first check box is selected
                if self.sender() == self.g_0:
                    self.graph_options = 0
                    # making other check box in the section to uncheck
                    self.g_1.setChecked(False)
                    self.g_2.setChecked(False)
    
                # if second check box is selected
                elif self.sender() == self.g_1:
                    self.graph_options = 1
                    # making other check box to uncheck
                    self.g_0.setChecked(False)
                    self.g_2.setChecked(False)
    
                # if third check box is selected
                elif self.sender() == self.g_2:
                    self.graph_options = 2
                    # making other check box to uncheck
                    self.g_0.setChecked(False)
                    self.g_1.setChecked(False)
              
    def uncheck_c(self, state):
    # Capture Options checkbox code to make only one checkbox at a time selectable and to enable/disable lower options as necessary 
    # Arguments: self, state of the check box (NOTE: this 'state' variable is automatically inputted by pyqt, you do not need to input it)
    # Returns: None
        # checking if state is checked
        if state == Qt.Checked:
            # if first check box is selected
            if self.sender() == self.c_0:
                self.capture_options = 0
                # making other check box to uncheck
                self.c_1.setChecked(False)
                self.c_2.setChecked(False)
                self.c_3.setChecked(False)
                self.c_4.setChecked(False)
                # Enable / Disable the min max files input
                self.range_min.setReadOnly(False)
                self.range_max.setText(' ')
                self.range_max.setReadOnly(True)
                self.range_min.setStyleSheet(''' QLineEdit{background-color:white;}''')
                self.range_max.setStyleSheet(''' QLineEdit{background-color:grey;}''')

            # if second check box is selected
            elif self.sender() == self.c_1:
                self.capture_options = 1
                # making other check box to uncheck
                self.c_0.setChecked(False)
                self.c_2.setChecked(False)
                self.c_3.setChecked(False)
                self.c_4.setChecked(False)
                # Enable / Disable the min max files input
                self.range_min.setReadOnly(False)
                self.range_max.setReadOnly(False)
                self.range_min.setStyleSheet(''' QLineEdit{background-color:white;}''')
                self.range_max.setStyleSheet(''' QLineEdit{background-color:white;}''')
  
            # if third check box is selected
            elif self.sender() == self.c_2:
                self.capture_options = 2
                # making other check box to uncheck
                self.c_0.setChecked(False)
                self.c_1.setChecked(False)
                self.c_3.setChecked(False)
                self.c_4.setChecked(False)
                # Enable / Disable the min max files input
                self.range_min.setReadOnly(False)
                self.range_max.setReadOnly(False)
                self.range_min.setStyleSheet(''' QLineEdit{background-color:white;}''')
                self.range_max.setStyleSheet(''' QLineEdit{background-color:white;}''')

            elif self.sender() == self.c_3:
                self.capture_options = 3
                # making other check box to uncheck
                self.c_0.setChecked(False)
                self.c_1.setChecked(False)
                self.c_2.setChecked(False)
                self.c_4.setChecked(False)   
                # Enable / Disable the min max files input
                self.range_min.setText(' ')
                self.range_min.setReadOnly(True)
                self.range_max.setText(' ')
                self.range_max.setReadOnly(True)
                self.range_min.setStyleSheet(''' QLineEdit{background-color:gray;}''')
                self.range_max.setStyleSheet(''' QLineEdit{background-color:gray;}''')

            elif self.sender() == self.c_4:
                self.capture_options = 4
                # making other check box to uncheck
                self.c_0.setChecked(False)
                self.c_1.setChecked(False)
                self.c_2.setChecked(False)
                self.c_3.setChecked(False)  
                # Enable / Disable the min max files input
                self.range_min.setText(' ')
                self.range_min.setReadOnly(True)
                self.range_max.setText(' ')
                self.range_max.setReadOnly(True)   
                self.range_min.setStyleSheet(''' QLineEdit{background-color:gray;}''')
                self.range_max.setStyleSheet(''' QLineEdit{background-color:gray;}''')         

    def uncheck_s(self, state):
    # Stacked Options checkbox code to make only one checkbox at a time selectable and to enable/disable lower options as necessary 
    # Arguments: self, state of the check box (NOTE: this 'state' variable is automatically inputted by pyqt, you do not need to input it)
    # Returns: None
        # checking if state is checked
        if state == Qt.Checked:
            # if first check box is selected
            if self.sender() == self.s_0:
                self.stacked_options = 0
                # making other check box to uncheck
                self.s_1.setChecked(False)
  
            # if second check box is selected
            elif self.sender() == self.s_1:
                self.stacked_options = 1
                # making other check box to uncheck
                self.s_0.setChecked(False)

    def uncheck_h(self, state):
    # Hardware Options checkbox code to make only one checkbox at a time selectable and to enable/disable lower options as necessary 
    # Arguments: self, state of the check box (NOTE: this 'state' variable is automatically inputted by pyqt, you do not need to input it)
    # Returns: None
        # As the hardware is dynamically added, acces them via a list
        num_hw = len(self.hw_checkboxes) # find length of hardware list
        # checking if state is checked
        if state == Qt.Checked:
            for i in range(0,num_hw):
                # if any check box is selected
                if self.sender() == self.hw_checkboxes[i]: # if the checkbox that has been checked is the same as that in the current list index
                    for k in range(0,num_hw):
                        if (i == k): # do nothing
                            pass
                        else:
                            # if it is another checkbox in the list, then uncheck it
                            self.hw_checkboxes[k].setChecked(False)

    def check_stacked_h(self, state):
    # There a graph with subplots cannot be produced for only one pice of data, so this checks if that 
    # Arguments: self, state of the check box (NOTE: this 'state' variable is automatically inputted by pyqt, you do not need to input it)
    # Returns: None
        num_hw = len(self.hw_checkboxes)
        # checking if state is checked
        if state == Qt.Checked:
            count = 0
            for i in range(0,num_hw):
                if self.hw_checkboxes[i].isChecked():
                    count = count + 1
            if ((count > 1) or (self.g_2.isChecked())):
                self.s_1.setEnabled(True)
            else:
                self.s_1.setEnabled(False)
 
    def produce_graph(self):
        # First populate the class with the appropriate values
        an.file_path = self.folder_location
        an.total_files = self.total_files

        if self.c_0.isChecked(): # one single capture
            an.capture_file = int(self.range_min.text())
        elif ((self.c_1.isChecked()) or (self.c_2.isChecked())):
            an.cap_range_min = int(self.range_min.text())
            an.cap_range_max = int(self.range_max.text())

        # Get the hw devices selected:
        hw_names = []
        for name in self.hw_checkboxes:
            if name.isChecked():
                hw_names.append(name.text())
        
        an.hw_names = hw_names

        # Check which functions are needed:
        if self.a_3.isChecked(): # Waterfall: 
            an.graphWaterfall(self.graph_options, self.capture_options, int(self.k_value.text()), int(self.interval.text()))
        else: # Normal Graphs
            if self.stacked_options == 0: # if this is an unstacked graph:
                if self.graph_options != 2: # Not both x and y
                    if len(hw_names) == 1: # single hardware
                        an.graphA(self.capture_options, self.graph_options, self.analysis_options, 0)
                    else: # More hardware
                        an.graphB(self.capture_options, self.graph_options, self.analysis_options, 0)
                else: # if for both x and y, single plot
                    if len(hw_names) == 1: # single hardware
                        an.graphC(self.capture_options, self.graph_options,self.analysis_options)
                    else: # More hardware
                        an.graphD(self.capture_options, self.graph_options,self.analysis_options)        
            else: # if this is a stacked graph
                if self.graph_options != 2: # Not both x and y, but must have multiple hardwares
                    if len(hw_names) != 1:
                        an.graphF(self.capture_options, self.graph_options, self.analysis_options, 1)
                else: # if both x and y
                    if len(hw_names) == 1: # single hardware
                        an.graphG(self.capture_options, self.graph_options, self.analysis_options, 1)
                    else: # More hardware
                        an.graphH(self.capture_options, self.graph_options,self.analysis_options, 1)   
        
        # Now clear all the checkboxes
        for i in range(0,len(self.all_check_buttons)):
            if self.all_check_buttons[i].isChecked():
                self.all_check_buttons[i].setChecked(False)
            if not self.all_check_buttons[i].isEnabled():
                self.all_check_buttons[i].setEnabled(True)

        # And Clear + DIsable the text boxes
        self.range_min.setText(' ')
        self.range_min.setReadOnly(True)
        self.range_max.setText(' ')
        self.range_max.setReadOnly(True)
        self.range_min.setStyleSheet(''' QLineEdit{background-color:gray;}''')
        self.range_max.setStyleSheet(''' QLineEdit{background-color:gray;}''')
        self.k_value.setText('0')
        self.k_value.setReadOnly(False)
        self.k_value.setStyleSheet(''' QLineEdit{background-color:gray;}''')
        self.interval.setText('0')
        self.interval.setReadOnly(False)
        self.interval.setStyleSheet(''' QLineEdit{background-color:grey;}''')


    def initUI(self):

        # Layouts
        self.dlgLayout = QVBoxLayout() # Vertical box layout
        # FOrm Layout
        self.btnLayout = QHBoxLayout() # Bottom buttons layout
        self.titleLayout = QVBoxLayout()

        # Horizontal Layouts:
        self.analysis_options_layout = QHBoxLayout()
        self.graph_options_layout = QHBoxLayout()
        self.hardware_options_layout = QHBoxLayout()
        self.capture_options_layout_1 = QHBoxLayout()
        self.capture_options_layout_2 = QHBoxLayout()
        self.range_layout_min = QHBoxLayout()
        self.range_layout_max = QHBoxLayout()
        self.stacked_options_layout = QHBoxLayout()

        # Add fonts:
        QFontDatabase.addApplicationFont("Landasans_Light.otf")
        QFontDatabase.addApplicationFont("Landasans_Medium.otf")

        self.font_medium = QFont("Landasans Medium")
        self.font_light = QFont("Landasans Ultra Light")

        # Title Setup 
        self.labelTitle = QLabel(self)
        self.labelTitle.setObjectName('LabelTitle')
        self.labelTitle.setText('ANALYSIS')
        self.labelTitle.setFont(self.font_medium)
        self.labelTitle.setAlignment(Qt.AlignHCenter)
        self.labelTitle.setWordWrap(True)

        # Diamond Logo set up
        self.diamond = QLabel(self)
        pixmap = QPixmap('Diamond.png')
        pixmap = pixmap.scaledToHeight(40)
        self.diamond.setPixmap(pixmap)
        self.diamond.setAlignment(Qt.AlignHCenter)
        self.diamond.setObjectName('DiamondLogo')

        # QCheckButtons Set up
        self.all_check_buttons = []

        # Analysis Options

        self.a_label = QLabel(self)
        self.a_label.setText('Analysis Options:')
        self.a_label.setFont(self.font_light)

        self.a_0 = QCheckBox("DFT")
        self.a_1 = QCheckBox("CSP")
        self.a_2 = QCheckBox("Normalised CSP")
        self.a_3 = QCheckBox("Waterfall")

        self.all_check_buttons.append(self.a_0)
        self.all_check_buttons.append(self.a_1)
        self.all_check_buttons.append(self.a_2)
        self.all_check_buttons.append(self.a_3)

        self.a_0.stateChanged.connect(self.uncheck_a)
        self.a_1.stateChanged.connect(self.uncheck_a)
        self.a_2.stateChanged.connect(self.uncheck_a)
        self.a_3.stateChanged.connect(self.uncheck_a)

        self.analysis_options_layout.addWidget(self.a_0)
        self.analysis_options_layout.addWidget(self.a_1)
        self.analysis_options_layout.addWidget(self.a_2)
        self.analysis_options_layout.addWidget(self.a_3)
        self.analysis_options_layout.addStretch(1)

        # Graph Options

        self.g_label = QLabel(self)
        self.g_label.setText('Graph Options:')
        self.g_label.setFont(self.font_light)

        self.g_0 = QCheckBox("X")
        self.g_1 = QCheckBox("Y")
        self.g_2 = QCheckBox("X and Y")

        self.all_check_buttons.append(self.g_0)
        self.all_check_buttons.append(self.g_1)
        self.all_check_buttons.append(self.g_2)

        self.g_0.stateChanged.connect(self.uncheck_g)
        self.g_1.stateChanged.connect(self.uncheck_g)
        self.g_2.stateChanged.connect(self.uncheck_g)

        self.graph_options_layout.addWidget(self.g_0)
        self.graph_options_layout.addWidget(self.g_1)
        self.graph_options_layout.addWidget(self.g_2)
        self.graph_options_layout.addStretch(1)

        # Hardware Options - All the hardwares

        self.h_label = QLabel(self)
        self.h_label.setText('Hardware Options:')
        self.h_label.setFont(self.font_light)        

        self.hw_names = []
        self.hw_checkboxes = [] # array to append the QCheckBox references to

        if self.tet_arr: # If tetramms exist
            for tet_name in self.tet_arr:
                self.hw_names.append(tet_name)

        if self.cam_arr: # If tetramms exist
            for cam_name in self.cam_arr:
                self.hw_names.append(cam_name)

        for i in range(0,len(self.hw_names)):
            self.hw_checkboxes.append(QCheckBox(self.hw_names[i]))
            self.hw_checkboxes[i].stateChanged.connect(self.check_stacked_h)
            self.all_check_buttons.append(self.hw_checkboxes[i])
            self.hardware_options_layout.addWidget(self.hw_checkboxes[i])

        self.hardware_options_layout.addStretch(1)

        # Capture Options:
        
        self.c_label = QLabel(self)
        self.c_label.setText('Capture Options:')
        self.c_label.setFont(self.font_light)  
         
        self.c_0 = QCheckBox("Specific Capture")
        self.c_1 = QCheckBox("Range, Unaveraged")
        self.c_2 = QCheckBox("Range, Averaged") 
        self.c_3 = QCheckBox("All Files, Averaged")
        self.c_4 = QCheckBox("All Files, Only Average")

        self.all_check_buttons.append(self.c_0)
        self.all_check_buttons.append(self.c_1)
        self.all_check_buttons.append(self.c_2)
        self.all_check_buttons.append(self.c_3)
        self.all_check_buttons.append(self.c_4)

        self.c_0.stateChanged.connect(self.uncheck_c)
        self.c_1.stateChanged.connect(self.uncheck_c)
        self.c_2.stateChanged.connect(self.uncheck_c)   
        self.c_3.stateChanged.connect(self.uncheck_c)
        self.c_4.stateChanged.connect(self.uncheck_c)

        self.capture_options_layout_1.addWidget(self.c_0)
        self.capture_options_layout_1.addWidget(self.c_1)
        self.capture_options_layout_1.addWidget(self.c_2)
        self.capture_options_layout_1.addStretch(1)

        self.capture_options_layout_2.addWidget(self.c_3)
        self.capture_options_layout_2.addWidget(self.c_4)
        self.capture_options_layout_2.addStretch(1)

        # Capture Options Range:
        min_label = QLabel(self)
        min_label.setText('Min File:')
        min_label.setFont(self.font_light)
        min_label.setAlignment(Qt.AlignHCenter)

        max_label = QLabel(self)
        max_label.setText('Max File:')
        max_label.setFont(self.font_light)
        max_label.setAlignment(Qt.AlignHCenter)        

        self.range_min = QLineEdit(self)
        self.range_min.setReadOnly(True)
        self.range_max = QLineEdit(self)
        self.range_max.setReadOnly(True)
        
        self.total_max = QLineEdit(self)
        self.total_max.setReadOnly(True)
        self.total_max.setText(str(self.total_files-1))
        self.total_max.setStyleSheet('''QLineEdit {background-color: white}''')
        total_label = QLabel(self)
        total_label.setText('Last File Num:')
        total_label.setFont(self.font_light)
        total_label.setAlignment(Qt.AlignHCenter) 

        self.k_value = QLineEdit(self)
        self.k_value.setReadOnly(True)
        self.k_value.setText('0')
        k_label = QLabel(self)
        k_label.setText('Cutoff Frequency:')
        k_label.setFont(self.font_light)
        k_label.setAlignment(Qt.AlignHCenter) 

        self.interval = QLineEdit(self)
        self.interval.setReadOnly(True)
        self.interval.setText('0')
        interval_label = QLabel(self)
        interval_label.setText('Interval Point:')
        interval_label.setFont(self.font_light)
        interval_label.setAlignment(Qt.AlignHCenter) 
        
        self.range_layout_min.addWidget(min_label)
        self.range_layout_min.addWidget(self.range_min)
        self.range_layout_min.addWidget(total_label)
        self.range_layout_min.addWidget(self.total_max)
        self.range_layout_min.addStretch(1)

        self.range_layout_max.addWidget(max_label)
        self.range_layout_max.addWidget(self.range_max)
        self.range_layout_max.addWidget(k_label)
        self.range_layout_max.addWidget(self.k_value)
        self.range_layout_max.addWidget(interval_label)
        self.range_layout_max.addWidget(self.interval)
        self.range_layout_max.addStretch(1)


        # Stacked Options:
        
        self.s_label = QLabel(self)
        self.s_label.setText('Stacked Options:')
        self.s_label.setFont(self.font_light)  

        self.s_0 = QCheckBox("Non Stacked")
        self.s_1 = QCheckBox("Stacked")

        self.all_check_buttons.append(self.s_0)
        self.all_check_buttons.append(self.s_1)

        self.s_0.stateChanged.connect(self.uncheck_s)
        self.s_1.stateChanged.connect(self.uncheck_s)

        self.stacked_options_layout.addWidget(self.s_0)
        self.stacked_options_layout.addWidget(self.s_1)
        self.stacked_options_layout.addStretch(1)

        # Clear Btn and Next Btn
        self.create_graph = QPushButton(self)
        self.create_graph.setText('Generate Graph')
        self.create_graph.setFont(self.font_medium)
        self.create_graph.clicked.connect(self.produce_graph)

        # Add the widgets and layouts in the vertical dialogue box

        self.dlgLayout.addWidget(self.diamond)
        self.titleLayout.addWidget(self.labelTitle)
        self.dlgLayout.addLayout(self.titleLayout)

        self.dlgLayout.addWidget(self.a_label)
        self.dlgLayout.addLayout(self.analysis_options_layout)
        self.dlgLayout.addWidget(self.g_label)
        self.dlgLayout.addLayout(self.graph_options_layout)
        self.dlgLayout.addWidget(self.h_label)
        self.dlgLayout.addLayout(self.hardware_options_layout)
        self.dlgLayout.addWidget(self.c_label)
        self.dlgLayout.addLayout(self.capture_options_layout_1)
        self.dlgLayout.addLayout(self.capture_options_layout_2)
        self.dlgLayout.addLayout(self.range_layout_min)
        self.dlgLayout.addLayout(self.range_layout_max)
        self.dlgLayout.addWidget(self.s_label)
        self.dlgLayout.addLayout(self.stacked_options_layout)
        self.dlgLayout.addWidget(self.create_graph)

    
        self.setLayout(self.dlgLayout)
        self.setFixedWidth(470)
        self.setFixedHeight(700)
    


if __name__ == '__main__':
    app = create_app()
    dlg = Chooser_Setup()
    dlg.show()
    sys.exit(app.exec_())