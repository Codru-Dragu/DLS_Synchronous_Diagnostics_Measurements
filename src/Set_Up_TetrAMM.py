''' FILE TO ALLOW USERS TO INPUT THE VALUES THEY WANT FOR THE HDF SET UP OF THE HARDWARE '''

# IMPORTS #
import sys

from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase

import cothread
from cothread.catools import *
import h5py
import time

# VARIABLES #

# FUNCTIONS # 

# Set up the application and stylesheet
def create_app():
# Function to create the application object
# Arguments: None
# Returns: None
    app = QApplication(sys.argv)
    return app

class Tetramm_Setup(QDialog):
# Main Window to create the TetrAMM set up modal window
    def __init__(self, tetnum, totaltet, parent=None):
    # Class initialiser for the modal
        super().__init__(parent)
        # Set the style sheet depending on how you want the GUI to look
        self.setStyleSheet('''
            QLabel {
                font-size: 20px;
                color: #191970;

            }
            
            #LabelTitle {
                font-size: 47px;
                color: #191970;
                font-weight: bold;
            }

            #PVLabel {
                font-size: 20px;
                font-weight: bold;
            
            }

            QLineEdit{
                font-size: 15px;
                border: 2px solid white;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                min-width: 4em;
            
            }

            QDialog {
                background: #B6D0E2;
            }

            #PVFrame {
                border-top: 2px solid white;
                border-bottom:  2px solid white;
                border-radius: 10px;
                
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
                width: 25px;

                border-left-width: 1px;
                border-left-color: lightblue;
                border-left-style: solid; /* just a single line */
                border-top-right-radius: 3px; /* same radius as the QComboBox */
                border-bottom-right-radius: 3px;
            }

            QComboBox::down-arrow {
                image: url("downArrow.png");
                width: 100px;
            }
            
            QComboBox QAbstractItemView {
                border: 2px solid darkgray;
                selection-background-color: lightgray;
                background-color: transparent;
                max-width: 130px;
                min-width: 30px;
                
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

            #NextBtn {
                font: bold 20px;
                max-width: 100px;
                
            }

            #AcquireBtn {
                font: bold 20px;
                border-width: 2px;
                border-radius: 15px;
                padding: 3px;
                max-width: 235;
            }
            
            ''')

        self.setWindowTitle(' ') # No title
        self.initUI(tetnum,totaltet) # Initialise the GUI
    
    def get_output(self):
    # Function to return the values needed
    # Called externally  
    # Arguments: self
    # Returns: the pv of the TetrAMM, and arrays containing the qe1 and hdf set up values respectively    
        return self.pv_text, self.qe1, self.hdf

    def calcseconds(self):
    # Fucntion to calculate the number of captures required
    # Called when seconds is edited
    # Arguments: None
    # Returns: None
        try:
            number_captures = int(self.seconds_edit.text())*10
            self.captures_read.setText(str(number_captures))
        except ValueError as e:
            self.captures_read.setText('Invalid') # If the number of captures cannot be calcualted due to bad input in the seconds field, display invalid error

    def gonext(self):
    # Function to get the values for Tetramm object set up
    # Called by the next button
    # Arguments: None
    # Returns: the QE1 and HDF5 Set up values   

        # Get the values for HDF5 from the GUI
        fp = self.filepath_edit.text()
        fn = self.filename_edit.text()
        ff = self.fileformat_edit.text()
        sec = self.seconds_edit.text()
        cap = self.captures_read.text()
        pvv = self.pv.text()

        # Getting the QE1 Values to return from the EPICS GUI:
        values_per_reading = caget ('%s:DRV:ValuesPerRead'%pvv) 
        averaging_time = caget('%s:DRV:AveragingTime'%pvv)

        # Create the Arrays
        self.pv_text = pvv
        self.qe1 = [values_per_reading,averaging_time]
        self.hdf = [fp,fn,ff,sec,cap]

        # Close the GUI
        self.close()

    def initUI(self, tetnum, totaltet):
    # Initialiser code
        # Layouts
        dlgLayout = QVBoxLayout() # Vertical box layout
        formLayout = QVBoxLayout() # Form format (lables and fields)
        formLayout_sec_labels = QHBoxLayout() # Form layout for the last two fields
        formLayout_sec= QHBoxLayout() # Form layout for the last two fields
        btnLayout = QHBoxLayout() # Bottom buttons layout
        titleLayout = QVBoxLayout() # Layout for the title

        # Frame for the pv section
        pv_frame = QFrame()
        pv_frame.setObjectName("PVFrame")
        pv_formLayout = QFormLayout()
        pv_btnLayout = QHBoxLayout()

        # Add fonts:
        QFontDatabase.addApplicationFont("Landasans_Light.otf")
        QFontDatabase.addApplicationFont("Landasans_Medium.otf")

        font_medium = QFont("Landasans Medium")
        font_light = QFont("Landasans Ultra Light")

        # Title Setup 
        self.labelTitle = QLabel(self)
        self.labelTitle.setObjectName('LabelTitle')
        self.labelTitle.setText('TetrAMM    (%(a)s/%(b)s)'%{'a': tetnum , 'b': totaltet})
        self.labelTitle.setFont(font_light)
        self.labelTitle.setAlignment(Qt.AlignHCenter)
        self.labelTitle.setWordWrap(True)
        
        # Form set up

        # Input fields
        self.filepath_edit = QLineEdit()
        self.filename_edit = QLineEdit()
        self.fileformat_edit = QLineEdit()
        self.fileformat_edit.setText('%s%s_%04d.h5')
        self.seconds_edit = QLineEdit()
        self.seconds_edit.textChanged.connect(self.calcseconds)
        self.captures_read = QLineEdit()
        self.captures_read.setReadOnly(True)

        # Lables
        fp_label = QLabel(self)
        fp_label.setText('FilePath:')
        fp_label.setFont(font_light)
        fp_label.setAlignment(Qt.AlignLeft)

        fn_label = QLabel(self)
        fn_label.setText('FileName:')
        fn_label.setFont(font_light)
        fn_label.setAlignment(Qt.AlignLeft)

        ff_label = QLabel(self)
        ff_label.setText('FileFormat:')
        ff_label.setFont(font_light)
        ff_label.setAlignment(Qt.AlignLeft)

        sec_label = QLabel(self)
        sec_label.setText('Seconds:')
        sec_label.setFont(font_light)
        sec_label.setAlignment(Qt.AlignLeft)

        cap_label = QLabel(self)
        cap_label.setText('Capture Num:')
        cap_label.setFont(font_light)
        cap_label.setAlignment(Qt.AlignLeft)

        # PV form section
        self.pv = QLineEdit(self)
        self.pv.setObjectName("PV")

        pv_label = QLabel(self)
        pv_label.setText('PV:')
        pv_label.setFont(font_light)
        pv_label.setObjectName("PVLabel")
        pv_label.setAlignment(Qt.AlignHCenter)

        pv_formLayout.insertRow(1, pv_label, self.pv) # Insert the labels in the appropriate position

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
        self.next_btn.setFont(font_medium)
        self.next_btn.clicked.connect(self.gonext)
        
        btnLayout.addWidget(self.next_btn)

        
        # Add the widgets and layouts in the vertical dialogue box

        # Add diamond Logo
        dlgLayout.addWidget(self.diamond)
        
        # Add Modal Title
        titleLayout.addWidget(self.labelTitle)
        titleLayout.setContentsMargins(0,0,0,0)
        dlgLayout.addLayout(titleLayout)

        # Add PV section 
        pv_formLayout.setContentsMargins(0,14,0,-6)
        pv_frame.setLayout(pv_formLayout)
        dlgLayout.addWidget(pv_frame)

        # Add the form section - note that when adding wdigets or layout to other layouts, the order in which they are added are the order in which they will show up on the GUI
        formLayout.addWidget(fp_label)
        formLayout.addWidget(self.filepath_edit)
        formLayout.addWidget(fn_label)
        formLayout.addWidget(self.filename_edit)
        formLayout.addWidget(ff_label)
        formLayout.addWidget(self.fileformat_edit)
        dlgLayout.addLayout(formLayout)

        formLayout_sec_labels.addWidget(sec_label)
        formLayout_sec_labels.addWidget(cap_label)
        dlgLayout.addLayout(formLayout_sec_labels)

        formLayout_sec.addWidget(self.seconds_edit)
        formLayout_sec.addWidget(self.captures_read)
        dlgLayout.addLayout(formLayout_sec)

        dlgLayout.addLayout(btnLayout)
        
        # Set the main layout and height and width of the modal window
        self.setLayout(dlgLayout)
        self.setFixedWidth(300)
        self.setFixedHeight(480)

# In case you want to run this app from this script
if __name__ == '__main__':
    app = create_app()
    dlg = Tetramm_Setup(1,2)
    dlg.show()
    sys.exit(app.exec_())