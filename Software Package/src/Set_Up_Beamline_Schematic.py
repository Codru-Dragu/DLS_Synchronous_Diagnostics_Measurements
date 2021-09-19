''' FILE TO ALLOW USERS TO PLACE THE AVAILABLE HARDWARE IN ORDER ON THE BEAMLINE SCHEMATIC '''
# IMPORTS #
import sys
import time

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton 
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor, QFontDatabase, QFont, QScreen
from PyQt5.QtCore import QMimeData, Qt, QTimer

import TetrAMM as T
import MantaCam as MC

# VARIABLES #

# FUNCTIONS # 

class DraggableLabel(QLabel):
# Class for the draggable labels containing the hardware devices availabele

    def mousePressEvent(self, event):
        # Upon mouse click, set the drag start position of the label
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        # Upon mouse move, use the mimedata class to drag the lable and paint where you are dragging it to across the GUI
        if not (event.buttons() & Qt.LeftButton):
            return # If the label is no being dragged anymore, return nothing
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return # if the label is dragged out of range, return nothing

        # Set up a drag object using QDrag and mimedata  
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text())
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab()) # Draw the pixmap of the moving label
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction) # Copy and mocve the label

class DropLabel(QLabel):
# Class for the lables on which other labels can be dropped, to be placed along the beamline

    def __init__(self, *args, **kwargs):
        # Main modal initialiser code, accpeting label drops
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
    # If the label being dragged on top has text, then accept the drop (to refrain from dropping empty labels)
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
    # When the label has been dropped, acquire the text of the dropped image
        text = event.mimeData().text()
        
        # Check the kind of hardware it is to know which icon to set, because you cannot inherit the hardware image from the dropped label
        # if it is a TetrAMM, (AKA, the label has TET in it), then add the TetrAMM image to the label
        if ('TET:' in text):
            # Set style sheet of the labe which is being dropped on to display the appropriate image
            self.setStyleSheet('''
                    QLabel {
                        image: url("TetIMG.png");
                        width: 10px;
                        padding-left: 3px;
                        padding-bottom: 60px;
                    }
                ''')
            self.setFixedHeight(100)
            self.setFixedWidth(210)

            display = text.replace('TET: ','') # Remove the TET indicator that was not placed by the user
            self.setText(display)

         # if it is a Camera, (AKA, the label has CAM in it), then add the Camera image to the label  
        elif ('CAM:' in text):
            # Set style sheet of the labe which is being dropped on to display the appropriate image
            self.setStyleSheet('''
                    QLabel {
                        image: url("CamIMG.png");
                        width: 10px;
                        padding-left: 3px;
                        padding-bottom: 60px;
                    }
                ''')
            self.setFixedHeight(100)
            self.setFixedWidth(210) 

            display = text.replace('CAM: ','') # Remove the CAM indicator that was not placed by the user
            self.setText(display)   

        # NOTE: if you want to add more kinds of hardware, you must makes sure to update the if statement with more options to display the appropriate hardware image         

        event.acceptProposedAction() # Accept the Drop

class MainWindow(QMainWindow):
# Main drag and drop GUI class

    def __init__(self, tet_dict, cam_dict):
    # Main initialiser
        super().__init__()
        # Set the stylesheet to customise the look and feel of the GUI. The background image is sete here under the MainWindow {} section - BeamSchem.png
        self.setStyleSheet('''
            MainWindow {
                background-image: url("BeamSchem"); 
                background-repeat: no-repeat; 
                background-position: center;
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
        ''')
        self.setWindowTitle(' ') # No title
        self.initUI(tet_dict,cam_dict) # Initialise the GUI

    def save(self):
    # Function to save the updated schematic 
    # Takes a screenshot of the current screen after all the labes have been put into their approppriate place
    # Arguments: None
    # Returns: None
        filename = 'BeamSchemAnno.png'
        screen = QApplication.primaryScreen() # Get the main screen of the window
        p = screen.grabWindow(self.centralwidget.winId()) # Grab the image
        p.save(filename, 'png') # Save as a png file

    def gonext(self):
    # Function to remove the hardware choices from the top, grab thr screen, and close the GUI upon button press
    # Arguments: None
    # Returns: None

        # Remove the Button
        self.next_btn.setText(' ')
        self.next_btn.setEnabled(False)
        self.next_btn.setStyleSheet('''
            QPushButton{
                background-color: white;
                border-style: outset;
                border-width: 5px;
                border-radius: 15px;
                border-color: white;
                font: 20px;
                color: #191970;
                padding: 6px;
            }
        ''')
        # Hide all the Drag Labels
        for lab in self.drag_label:
            # For each draggable label along the top, remove it's text and image
            lab.setText(' ')
            lab.setStyleSheet(''' 
                Qlabel{
                    image: None;
                }
                ''')

        # Add a qtimer so that the widgets can hide properly first before capturing. Call the save functon
        QTimer.singleShot(700, self.save)

        # Then close it, but after allowing enough time for the shot to be taken and saved using a Qtimer
        QTimer.singleShot(700, self.close)

    def initUI(self,tet_dict,cam_dict):
    # Main initialiser code

        # Make vertical and horizontal box layouts:
        self.centralwidget = QWidget() # Central widget schematic photo
        self.setCentralWidget(self.centralwidget)

        self.selector_layout = QHBoxLayout() # Layout for draggable labels displaying available hardware along the top
        self.drop_layout = QHBoxLayout() # Layout for labels which should be dropped on
        self.button_layout = QHBoxLayout() #Layout for bottom button
        overall_layout = QVBoxLayout(self.centralwidget) # The overall layout

        # Add fonts:
        QFontDatabase.addApplicationFont("Landasans_Light.otf")
        QFontDatabase.addApplicationFont("Landasans_Medium.otf")

        font_medium = QFont("Landasans Medium")
        font_light = QFont("Landasans Ultra Light")

        # Based on the number of hardwares, dynamically create the kind of lables needed to add to the GUI

        # First, create the DRAGGABLE LABELS:
        self.drag_label = [] # initialise array to store the instances

        # To create the TetrAMMs:
        if tet_dict: # if they exist
            for tet_obj in tet_dict:
                # Create selector labels and set the image you want
                tet_label = DraggableLabel('TET: %s'%tet_obj.file_name, self) 
                tet_label.setStyleSheet('''
                    QLabel {
                        image: url("TetIMG.png");
                        width: 10px;
                        padding-left: 3px;
                        padding-bottom: 20px;
                    }
                ''')
                tet_label.setFixedHeight(70)
                tet_label.setFixedWidth(250)   
                self.drag_label.append(tet_label)  # Append the list      
                self.selector_layout.addWidget(tet_label)

        # To create the Cameras:
        if cam_dict: # If there are cameras
            for cam_obj in cam_dict:
                # Create selector labels and set the image you want
                cam_label = DraggableLabel('CAM: %s'%cam_obj.file_name, self) 
                cam_label.setStyleSheet('''
                    QLabel {
                        image: url("CamIMG.png");
                        width: 10px;
                        padding-left: 3px;
                        padding-bottom: 20px;
                    }
                ''')
                
                cam_label.setFixedHeight(70)
                cam_label.setFixedWidth(250) 
                self.drag_label.append(cam_label)   # Append to the list        
                self.selector_layout.addWidget(cam_label)


        # Now, create the LABELS ON WHICH TO DROP THE DRAGGABLES LABELS ON

        self.drop_layout.addStretch(1) # Add stretches to span the whole screen with even spacing

        for i in range(0,(len(tet_dict)+len(cam_dict))): # Create the total number of labels based on the total number of hardware (both) available
            slot_label = DropLabel('Place Hardware', self)
            self.drop_layout.addWidget(slot_label)
            self.drop_layout.addStretch(1)

        # NOTE: To add more draggable labels eg for beam components, follow the same process above to make the draggable labels
        # and the corresponding number of labels to drop upon in a different layout (make a new layout) and appenmd this new layout 
        # just below the one for the hardware. Or, put them all on the smae layout, so add more dropLabels than the number of hardeware

        # Creates the button
        self.next_btn = QPushButton(self)
        self.next_btn.setText('N E X T')
        self.next_btn.setObjectName('NextBtn')
        self.next_btn.setFont(font_medium)
        self.next_btn.clicked.connect(self.gonext)
        self.next_btn.setFixedWidth(200)
        self.button_layout.addWidget(self.next_btn)

        # Append everything to the layouts
        overall_layout.addLayout(self.selector_layout)
        overall_layout.addLayout(self.drop_layout)
        overall_layout.addLayout(self.button_layout)
        
        # Configure the GUI style
        self.setFixedWidth(1100)
        self.setFixedHeight(300)
        
# In case you want to try running this from this script directly
if __name__ == '__main__':
    tetr = T.TetrAMM('TS-DI-QEM-02','/home','bbb1')
    camer = MC.MantaCam('TS-DI-DCAM-01', '/home', 'Cccc1')
    app = QApplication(sys.argv) # app is created here, but this whole script will actually be called externally 
    w = MainWindow([tetr],[camer])
    w.show()
    sys.exit(app.exec_())