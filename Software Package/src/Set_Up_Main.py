''' FILE TO ALLOW USERS TO SELECT THE HARDWARE THAT THEY WANT TO ACQUIRE DATA FROM '''

# IMPORTS #
import sys 

from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
import webbrowser

# VARIABLES #

# FUNCTIONS #

# Set up the application and stylesheet
def create_app():
# Function to create the application object
# Arguments: None
# Returns: None

    app = QApplication(sys.argv)
    return app

class Hardware_Setup(QDialog):
# Main Window for Hardware set up modals
    def __init__(self, parent=None):
    # Class initialiser for the modal
        super().__init__(parent)
        # Set they StyleSheet to design the GUI as required
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
            ''')

        self.setWindowTitle(' ') # No title
        self.initUI() # Initialsie the GUI

    def gonext(self):
    # Function to acquire the number of each harware and open the next GUIS to finish the set up
    # Function called by the next button
    # Arguments: self
    # Returns: None

        # First, get how many of each harware is required
        howmany_tetramms = self.tet_combo.currentText()
        howmany_cameras = self.cam_combo.currentText()

        # Store the harware values in _output to be returned, close the window
        self._output = howmany_tetramms, howmany_cameras
        self.close()
        
    def get_output(self):
    # Function to return the number of tetramms and cameras present
    # Called externally 
    # Arguments: self
    # Returns: the _output variable that stores hardware number information for the next GUI
        return self._output

    def gethelp(self):
    # Function to open the webbroswer to the help file on confluence
    # Called by help button
    # Arguments: self
    # Returns: None
        webbrowser.open('https://confluence.diamond.ac.uk/pages/viewpage.action?spaceKey=DIAGTECH&title=Synchronous+X-Ray+Diagnostics+Measurements+Help+Guide#SynchronousX-RayDiagnosticsMeasurementsHelpGuide-Set_Up_Main.py')
        pass

    def enablenext(self):
    # Function to enable the next button iff there is at least one hardware of any kind
    # Arguments: None
    # Returns: None

        # Check if any hardwares have been selected and if so, enable the next button
        if ((int(self.tet_combo.currentText()) != 0) or (int(self.cam_combo.currentText()) != 0)):
            self.next_btn.setEnabled(True)
        else:
            self.next_btn.setEnabled(False)
            

    def initUI(self):
    # Initialisation code

        # Layouts
        dlgLayout = QVBoxLayout() # Vertical box layout
        formLayout = QFormLayout() # Form format (lables and fields)
        btnLayout = QHBoxLayout() # Bottom buttons layout

        titleLayout = QVBoxLayout()

        # Add fonts:
        QFontDatabase.addApplicationFont("Landasans_Light.otf")
        QFontDatabase.addApplicationFont("Landasans_Medium.otf")

        font_medium = QFont("Landasans Medium")
        font_light = QFont("Landasans Ultra Light")

        # Combobox Setup
        self.tet_combo = QComboBox()
        self.tet_combo.addItems(['0','1', '2', '3'])
        self.tet_combo.setObjectName('TetCombo')
        self.tet_combo.currentIndexChanged.connect(self.enablenext)

        self.cam_combo = QComboBox()
        self.cam_combo.addItems(['0','1', '2', '3'])
        self.cam_combo.setObjectName('CamCombo')
        self.cam_combo.currentIndexChanged.connect(self.enablenext)


        # Title Setup 
        self.labelTitle = QLabel(self)
        self.labelTitle.setObjectName('LabelTitle')
        self.labelTitle.setText('DIAGNOSTICS HARDWARE')
        self.labelTitle.setFont(font_medium)
        self.labelTitle.setAlignment(Qt.AlignHCenter)
        self.labelTitle.setWordWrap(True)
        
        # TetrAMM and Camera label set ups
        t_label = QLabel(self)
        t_label.setText('TETRAMM')
        t_label.setFont(font_light)
        t_label.setAlignment(Qt.AlignCenter)

        c_label = QLabel(self)
        c_label.setText('CAMERA')
        c_label.setFont(font_light)
        c_label.setAlignment(Qt.AlignCenter)

        # Add the hardware comboboxes and the labels in rows on the GUI
        formLayout.insertRow(1, t_label, self.tet_combo) 
        formLayout.insertRow(2, c_label, self.cam_combo)
        # NOTE: Add another row for another object 
    
        # Diamond Logo set up
        self.diamond = QLabel(self)
        pixmap = QPixmap('Diamond.png')
        pixmap = pixmap.scaledToHeight(40)
        self.diamond.setPixmap(pixmap)
        self.diamond.setAlignment(Qt.AlignHCenter)
        self.diamond.setObjectName('DiamondLogo')

        # Buttons Set Up:
        # Next Button
        self.next_btn = QPushButton(self)
        self.next_btn.setText('N E X T')
        self.next_btn.setObjectName('NextBtn')
        self.next_btn.setFont(font_medium)
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.gonext)

        # Help Button
        self.help_btn = QPushButton(self)
        self.help_btn.setText('')
        self.help_btn.setObjectName('HelpBtn')
        self.help_btn.setFixedWidth(50)
        self.help_btn.clicked.connect(self.gethelp)

        # Add the buttons to the btnlayout
        btnLayout.addWidget(self.next_btn)
        btnLayout.addWidget(self.help_btn)
    
        # Add the widgets and layouts in the vertical dialogue box
        dlgLayout.addWidget(self.diamond)
        
        titleLayout.addWidget(self.labelTitle)
        titleLayout.setContentsMargins(0,0,0,0)
        dlgLayout.addLayout(titleLayout)

        formLayout.setContentsMargins(0,20,0,25)
        formLayout.setVerticalSpacing(10)
        dlgLayout.addLayout(formLayout)
        dlgLayout.addLayout(btnLayout)
        
        # Set the main layout and the height/width
        self.setLayout(dlgLayout)
        self.setFixedWidth(250)
        self.setFixedHeight(360)
    
# In case you run the GUI on this script directly
if __name__ == '__main__':
    app = create_app()
    dlg = Hardware_Setup()
    dlg.show()
    sys.exit(app.exec_())