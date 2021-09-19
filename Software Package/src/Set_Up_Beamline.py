''' FILE TO ALLOW USERS TO PICK THE BEAMLINE THEY WANT IN PREPARATION FOR THE NEXT GUI '''

# IMPORTS #

import sys 

from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
import webbrowser

# VARIABLES #

# FUNTIONS #

# Set up the application and stylesheet
def create_app():
# Function to create the application object
# Arguments: None
# Returns: None
    app = QApplication(sys.argv)
    return app

class Beamline_Setup(QDialog):
# Main Window to set up beamline configuration GUI
    def __init__(self, parent=None):
    # Class initialiser for the modal
        super().__init__(parent)
        # Set stylesheet ot configure GUI however you want
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

            #HelpBtn {
                image: url("help.png");
                font: bold 20px;
                width: 30px;
                
            
            }
            ''')

        self.setWindowTitle(' ') # No title
        self.initUI() # Initialiser function 

    def gonext(self):
    # Function to acquire the number of the beamline
    # Function called by the next button
    # Arguments: self
    # Returns: None, but stores the beamline name and Topup PV in the output variable

        # First, get the beamline name
        beamline_name = self.beam_combo.currentText()
        topup_pv = self.topup.text()
        # Store the harware values in the output variable
        self._output = beamline_name, topup_pv
        # Close the GUI
        self.close()
        
    def get_output(self):
    # Function to return the values needed
    # Called externally  
    # Arguments: self
    # Returns: the _output variable containing the beamline name and topup pv
        return self._output

    def initUI(self):
    # Initialiser code
        # Layouts
        dlgLayout = QVBoxLayout() # Vertical box layout
        formLayout = QFormLayout() # Form format (lables and fields)
        btnLayout = QHBoxLayout() # Bottom buttons layout
        titleLayout = QVBoxLayout() # Layout for the titles

        # Add fonts:
        QFontDatabase.addApplicationFont("Landasans_Light.otf")
        QFontDatabase.addApplicationFont("Landasans_Medium.otf")

        font_medium = QFont("Landasans Medium")
        font_light = QFont("Landasans Ultra Light")

        # Combobox Setup - choosing the beamline name
        self.beam_combo = QComboBox()
        self.beam_combo.addItems(['BL02I', 'BLO2J', 'BL03I', 'BL04I', 'BL04J', 'BL05I', 'BL06I', 'BL06K', 'BL07B', 'BL07C', 'BL07I', 'BL08I', 'BL08J', 'BL09I', 'BL10I', 'BL11I', 'BL11J', 'BL11K', 'BL12I', 'BL12I', 'BL13I', 'BL13J', 'BL14I', 'BL15I', 'BL15J', 'BL16B', 'BL16I', 'BL18B', 'BL18I', 'BL19I', 'BL20I', 'BL20J', 'BL21I', 'BL21B', 'BL22B', 'BL22I', 'BL23B', 'BL23I', 'BL24B', 'BL24I'])
        self.beam_combo.setObjectName('BeamCombo')

        # QLineEdit SetUp - text edit for the topup pv
        self.topup = QLineEdit()
        self.topup.setText('SR-CS-FILL-01:COUNTDOWN')
        self.topup.setReadOnly(True) # This makes it uneditable, to make editable replace True with False

        # Title Setup  and labels
        self.labelTitle = QLabel(self)
        self.labelTitle.setObjectName('LabelTitle')
        self.labelTitle.setText('SELECT BEAMLINE')
        self.labelTitle.setFont(font_medium)
        self.labelTitle.setAlignment(Qt.AlignHCenter)
        self.labelTitle.setWordWrap(True)
        
        t_label = QLabel(self)
        t_label.setText('BEAMLINE')
        t_label.setFont(font_light)
        t_label.setAlignment(Qt.AlignCenter)

        line_label = QLabel(self)
        line_label.setText('TOPUP PV')
        line_label.setFont(font_light)
        line_label.setAlignment(Qt.AlignCenter)

        formLayout.insertRow(1, t_label, self.beam_combo)
        formLayout.insertRow(2, line_label, self.topup )


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

        # Diamond logo
        dlgLayout.addWidget(self.diamond)
        
        # Title Layout
        titleLayout.addWidget(self.labelTitle)
        titleLayout.setContentsMargins(0,0,0,0)
        dlgLayout.addLayout(titleLayout)

        # Add comboboxes and labels
        formLayout.setVerticalSpacing(10)
        dlgLayout.addLayout(formLayout)
        dlgLayout.addLayout(btnLayout)
        
        # Configure the main layout and the sise of the GUI
        self.setLayout(dlgLayout)
        self.setFixedWidth(250)
        self.setFixedHeight(250)
    
# In case you want to run the script from this file 
if __name__ == '__main__':
    app = create_app()
    dlg = Beamline_Setup()
    dlg.show()
    sys.exit(app.exec_())