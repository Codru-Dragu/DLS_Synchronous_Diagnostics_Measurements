''' FILE TO ALLOW USERS TO CONVER THE HDF5 FILES TO MAT FILES FOR FASTER ANLAYSIS '''

# IMPORTS #
import sys 
import time

from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton,  QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
import webbrowser

import scipy.io as sio
import mpld3
import File_Creator as fc
import numpy as np

# VARIBALES #

# FUNCTIONS # 

# Set up the application and stylesheet
def create_app():
# Function to create the application object
# Arguments: None
# Returns: None
    app = QApplication(sys.argv)
    return app

class Data_Convertor(QDialog):
# Main Window for Data convertor GUI
    def __init__(self, parent=None):
    # Class initialiser for the gui
        super().__init__(parent)
        self.setStyleSheet('''
            QLabel {
                font-size: 27px;
                color: #191970;

            }
            QLineEdit{
                font-size: 15px;
                border: 2px solid white;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
            }
            
            #LabelTitle {
                font-size: 50px;
                color: #191970;
                font-weight: bold;
            }

            QDialog {
                background: #B6D0E2;
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

            #ChooseBtn {
                background-color: white;
                border-radius: 0px;
                border-color: #191970;
            
            }

            #HelpBtn {
                image: url("help.png");
                font: bold 20px;
                width: 30px;
                
            
            }
            ''')

        self.setWindowTitle(' ') # No title
        self.initUI() # initialise the GUI

    def gonext(self):
    # Function to acquire the number of the beamline
    # Function called by the next button
    # Arguments: None
    # Returns: None

        # First, extract the info file that was sent and read the appropriate values:
        info_file = {}
        sio.loadmat('%s'%self.chosen_path.text(), mdict=info_file) # open the file path

        # Next update the GUI to show whcih file is being processed
        create_Label = QLabel(self)
        create_Label.setText('Creating Files')
        create_Label.setFont(self.font_medium)
        create_Label.setAlignment(Qt.AlignHCenter)

        self.counter_label = QLabel(self)
        self.counter_label.setText('Processing File: %(a)s/%(b)s'%{'a': 0, 'b': info_file['Total_Files'][0][0] })
        self.counter_label.setFont(self.font_medium)
        self.counter_label.setAlignment(Qt.AlignHCenter)

        self.dlgLayout.addWidget(create_Label)
        self.dlgLayout.addWidget(self.counter_label)
        self.setFixedHeight(400)
        time.sleep(0.5)

        # Create the files
        for q in range(0,info_file['Total_Files'][0][0]-1): # Get the range to stop in the file before the last: eg, if there are 156 files total, the range should go to 155 (meaning it will stop at 154)
            QApplication.processEvents()
            fc.makefiles(info_file['Tet_Hw'][0][0][0][0],info_file['Cam_Hw'][0][0][0][0], self.new_file_path.text(), info_file['Total_Files'][0][0],q)
            self.counter_label.setText('Processing File: %(a)s/%(b)s'%{'a': q+1, 'b': info_file['Total_Files'][0][0]})
        
        # Create the last file and get the X_Dict - the last file is made at the same time as the xdicrt file, which stores the common time data for each object in only one file for easy access. 
        fc.makexfile(info_file['Tet_Hw'][0][0][0][0],info_file['Cam_Hw'][0][0][0][0], self.new_file_path.text(), info_file['Total_Files'][0][0])
        self.counter_label.setText('Processing Files (including XFile): Done!')

    def open_file(self):
    # Function to opn the selected file when the upload file button is pressed
    # Arguments: None
    # Returns: None
        self.path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)')
        if self.path != ('', ''): # If the person has input a path
            self.chosen_path.setText(self.path[0])

    def initUI(self):
    # Main initialiser

        # Layouts
        self.dlgLayout = QVBoxLayout() # Vertical box layout
        formLayout = QFormLayout() # Form format (lables and fields)
        btnLayout = QHBoxLayout() # Bottom buttons layout
        titleLayout = QVBoxLayout()

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

        # QLineEdit SetUp - new file path to save the mat files to
        self.new_file_path = QLineEdit()

        # QLineEdit SetUp - display path of chosen file
        self.chosen_path = QLineEdit()      
        self.chosen_path.setReadOnly(False)  

        # Title Setup 
        self.labelTitle = QLabel(self)
        self.labelTitle.setObjectName('LabelTitle')
        self.labelTitle.setText('ANALYSIS SETUP')
        self.labelTitle.setFont(self.font_medium)
        self.labelTitle.setAlignment(Qt.AlignHCenter)
        self.labelTitle.setWordWrap(True)
        
        t_label = QLabel(self)
        t_label.setText('SELECT INFOFILE: ')
        t_label.setFont(self.font_light)
        t_label.setAlignment(Qt.AlignCenter)

        line_label = QLabel(self)
        line_label.setText('NEW FILEPATH: ')
        line_label.setFont(self.font_light)
        line_label.setAlignment(Qt.AlignCenter)

        path_label = QLabel(self)
        path_label.setText('SELECTED FILE: ')
        path_label.setFont(self.font_light)
        path_label.setAlignment(Qt.AlignCenter)

        formLayout.insertRow(1, t_label, self.choose_btn)
        formLayout.insertRow(2, path_label, self.chosen_path)
        formLayout.insertRow(3, line_label, self.new_file_path )

        # Diamond Logo set up
        self.diamond = QLabel(self)
        pixmap = QPixmap('Diamond.png')
        pixmap = pixmap.scaledToHeight(20)
        self.diamond.setPixmap(pixmap)
        self.diamond.setAlignment(Qt.AlignLeft)
        self.diamond.setObjectName('DiamondLogo')

        # Buttons Set Up:
        self.next_btn = QPushButton(self)
        self.next_btn.setText('N E X T')
        self.next_btn.setObjectName('NextBtn')
        self.next_btn.setFont(self.font_medium)
        self.next_btn.clicked.connect(self.gonext)

        btnLayout.addWidget(self.next_btn)
        
        # Add the widgets and layouts in the vertical dialogue box

        self.dlgLayout.addWidget(self.diamond)
        
        titleLayout.addWidget(self.labelTitle)
        titleLayout.setContentsMargins(0,0,0,0)
        self.dlgLayout.addLayout(titleLayout)

        formLayout.setVerticalSpacing(10)
        self.dlgLayout.addLayout(formLayout)
        self.dlgLayout.addLayout(btnLayout)
        
        self.setLayout(self.dlgLayout)
        self.setFixedWidth(400)
        self.setFixedHeight(300)
    
# In case you wanted to run this script from here
if __name__ == '__main__':
    app = create_app()
    dlg = Data_Convertor()
    dlg.show()
    sys.exit(app.exec_())