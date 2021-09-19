''' FILE TO ALLOW USERS TO MONITOR THE STATE OF THE HARDWARE AND CONTROL IT SEPARATELY FROM THE EPICS GUI'''

# IMPORTS #
# PyQt imports 
import sys
import time
import scipy.io as sio
import webbrowser

from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QFrame, QMainWindow, QAction, QHeaderView
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QScrollArea, QWidget, QTextBrowser, QPlainTextEdit
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase, QPainter, QIcon, QStandardItemModel

# Looping
import Loop_Code as Looper

# FUNCTIONS #

''' GUI FUNCTIONS '''

# Set up the application and stylesheet
def create_app():
# Function to create the application object
# Arguments: None
# Returns: None
    app = QApplication(sys.argv)
    return app

class Hardware_Device(QFrame):
# Class for each individual hardware device frame / modal
    def __init__(self,device_name,device_type, parent = None):
    # Main Class initialiser code
        super().__init__(parent)
        # Set styulesheet to configure the GUI look
        self.setStyleSheet('''
            QWidget {
                background: #B6D0E2;
            }

            QPlainTextEdit {
                background: #B6D0E2;
                border: 6px solid;
                border-color: #191970;
                border-radius: 10px;
            }
            
            #file_display_scroll {
                background: white;
                border-color: #B6D0E2;
            }

            QLabel {
                font-size: 20px;
                color: #191970;

            }

            #DLabel {
                font-size: 60px;
                color: #191970;
                font-weight: bold;
                padding-top: 0px;
                padding-left: 12px;
            }

            #device_name_label {
                font-size: 40px;
                color: #191970;
                background-color: white;
                font-weight: bold;
            }

            #device_type_label {
                font-size: 30px;
                color: red;
                background-color: white;
            }

            #DiamondLogo {

                border-right :3px solid blue;
                border-color: #191970;
                padding-right: 16px;
                padding-bottom: 5px;
                padding-top: 1px;
            }

            #MLabel {
                font-size: 30px;
                padding-left: 5px;
            
            }

            #BeamLabel {
                font-size: 80px;
                padding-top: 20px;
            
            }

            #TimeoutLabel {
                padding-top: 2px;
                padding-right:-6px;
            
            }

            QLineEdit {
                font-size: 15px;
                background-color: white;
                border: 2px solid white;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                max-width: 6em;
            
            }

            QPushButton {
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

            #TimeoutHelpBtn {
                image: url("help.png");
                font: bold 15px;
                width: 15;
                border-width: 3px;
                border-radius: 10px;
                padding: 3px;
            }

            #HelpBtn {
                image: url("help.png");
                font: bold 20px;
                width: 30px;
            }

            #ErrorLogLabel {
                font-size: 30px;
                border-top :3px solid;
                border-color: #191970;

            }

            QPlainTextEdit {
                background: white;
                border: 6px solid;
                border-color: #191970;
                border-radius: 10px;

            }

            Hardware_Device {
                background-color: white;
                border: 6px solid;
                border-color: #191970;
                border-radius: 10px;

            }

            ''')

        self.setWindowTitle(' ') # No title
        self.initUI(device_name,device_type) # Call the Initialisation code

    def initUI(self,device_name,device_type):
    # Actual initialisation code to set up the GUI

        # Layouts
        hardware_frame = QVBoxLayout(self)

        # Add fonts:
        QFontDatabase.addApplicationFont("Landasans_Light.otf")
        QFontDatabase.addApplicationFont("Landasans_Medium.otf")

        font_medium = QFont("Landasans Medium")
        font_light = QFont("Landasans Ultra Light")

        # Widgets
        # Name label and Device type:
        device_name_label = QLabel(self)
        device_name_label.setText('%s'%device_name)
        device_name_label.setFont(font_medium)
        device_name_label.setObjectName("device_name_label")
        device_name_label.setAlignment(Qt.AlignHCenter)
        device_name_label.setWordWrap(True)

        device_type_label = QLabel(self)
        device_type_label.setFont(font_medium)
        device_type_label.setObjectName("device_type_label")
        device_type_label.setAlignment(Qt.AlignHCenter)
        
        ## Determine the device type:
        if(device_type == 0): # If the device is a TetrAMM
            device_type_label.setText('TETRAMM')
        else: # Camera
            device_type_label.setText('MANTACAM')

        # NOTE: To add more hardware, add more elif statements and number identifiers > 1 (as 0 = Tet, 1 = MCam)

        #QScroll - make the text fields scrollable:
        self.device_scroll = QPlainTextEdit(self)
        self.device_scroll.setReadOnly(True)
        self.device_scroll.setObjectName('file_display_scroll')

        # Add widgets to frame
        hardware_frame.addWidget(device_name_label)
        hardware_frame.addWidget(device_type_label)
        hardware_frame.addWidget(self.device_scroll)

        # Configure Frame Size
        self.setLayout(hardware_frame)
        self.setFixedSize(194,520)

class MainLayout(QWidget):
# Class for the main Diagnostics page

    def __init__(self,hd_t,hd_c,tet_dict,cam_dict,total_seconds,beamline_name,beamline_topup):
    # Main Initialiser
    # Arguments: hd_t: an array of TetrAMM device widgets (the frames from the above class), hd_c: an array of Camera device widgets (the frames from the above class), tet_dict: tetramm object array, cam_dict: cam era object array
    # total_seconds: time data was acquired for, beamline name, beamline_topup: topup pv 
        super().__init__()
        # Configure GUI look
        self.setStyleSheet('''
                QWidget {
                    background: #B6D0E2;
                }

                QScrollArea {
                    background: #B6D0E2;
                    border: 6px solid;
                    border-color: #191970;
                    border-radius: 10px;
                }
                
                #file_display_scroll {
                    background: white;
                    border-color: #B6D0E2;
                }

                QLabel {
                    font-size: 20px;
                    color: #191970;

                }

                #DLabel {
                    font-size: 60px;
                    color: #191970;
                    font-weight: bold;
                    padding-top: 0px;
                    padding-left: 12px;
                }

                #device_name_label {
                    font-size: 40px;
                    color: #191970;
                    background-color: white;
                    font-weight: bold;
                }

                #device_type_label {
                    font-size: 30px;
                    color: red;
                    background-color: white;
                }

                #DiamondLogo {

                    border-right :3px solid blue;
                    border-color: #191970;
                    padding-right: 16px;
                    padding-bottom: 5px;
                    padding-top: 1px;
                }

                #MLabel {
                    font-size: 30px;
                    padding-left: 5px;
                
                }

                #BeamLabel {
                    font-size: 80px;
                    padding-top: 20px;
                
                }

                #TimeoutLabel {
                    padding-top: 4px;
                    padding-right:-6px;
                
                }

                #GateLabel {
                    padding-top: 4px;
                    padding-right:-6px;                

                }

                QLineEdit {
                    font-size: 15px;
                    background-color: white;
                    border: 2px solid white;
                    border-radius: 5px;
                    padding: 1px 18px 1px 3px;
                    max-width: 6em;
                
                }

                QPushButton {
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
                    background-color:gray;
                }

                #SetBtn {
                    font: bold 15px;
                    width: 40px;
                    height: 20px;
                    border-width: 5px;
                    border-radius: 10px;
                    padding: 3px;

                }

                #StartBtn {
                    background-color: #DAF7A6;
                
                }
                #StartBtn::disabled {
                    background-color:gray;
                }

                #StopBtn {
                    background-color: #FF5733;
                
                } 
                #StopBtn::disabled {
                    background-color:gray;
                }                   

                #ResetBtn {
                    background-color: #FFE07B;
                }            
                #ResetBtn::disabled {
                    background-color:gray;
                } 
                #ChangedBtn {
                    background-color: #FFE07B;
                }
                #ChangedBtn::disabled {
                    background-color:gray;
                } 
                #TimeoutHelpBtn {
                    image: url("help.png");
                    font: bold 15px;
                    width: 15px;
                    height: 20px;
                    border-width: 5px;
                    border-radius: 10px;
                    padding: 3px;
                }

                #HelpBtn {
                    image: url("help.png");
                    font: bold 20px;
                    width: 30px;
                }

                #ErrorLogLabel {
                    font-size: 30px;
                    border-top :3px solid;
                    border-color: #191970;

                }

                QPlainTextEdit {
                    background: white;
                    border: 6px solid;
                    border-color: #191970;
                    border-radius: 10px;

                }

                Hardware_Device {
                    background-color: white;
                    border: 6px solid;
                    border-color: #191970;
                    border-radius: 10px;

                }

                ''')    
        
        # INITIALISE THE LOOP CLASS to run the backend code #
        Looper.set_up(tet_dict,cam_dict,beamline_topup) 
        Looper.set_camera_fps_range() # Initialise the set fps range marker

        # Initialise click to determine whether the stop button was pressed or not and exit the Looper code loop
        self.click = 0

        # Initialise InfoFIle saved button click and close button click (to determine how many times the upper close has been pressed)
        self.infosaved = 0
        self.closeclick = 0

        # Set the UI
        self.initUI(hd_t,hd_c,tet_dict,cam_dict,total_seconds,beamline_name,beamline_topup)

    def get_timeout_help(self):
    # Function to open the webbroswer to the help file on confluence
    # Called by help button
    # Arguments: self
        webbrowser.open('https://confluence.diamond.ac.uk/pages/viewpage.action?spaceKey=DIAGTECH&title=Synchronous+X-Ray+Diagnostics+Measurements+Help+Guide#SynchronousX-RayDiagnosticsMeasurementsHelpGuide-Set_Up_Diagnostics.py')
        pass

    def set_start(self):
    # Function to arm the hardware: start the loop data acquisition function
    # Arguments: self
    # Returns: None

        # First disable the reset, export file, and changed epics buttons, as well as the timeout set btn
        self.reset_btn.setEnabled(False)
        self.getfile_btn.setEnabled(False)
        self.changed_btn.setEnabled(False)
        self.set_both_btn.setEnabled(False)
        self.export_error_btn.setEnabled(False)

        # First start the hdf files
        Looper.set_hdf_toggles()
        # Now run the loop code as needed
        self.click = 0 
        while (self.click != 1): # while the stop button has not been clicked
            QApplication.processEvents() # process the events - this is needed for any button press on the GUI to be registered once the Loop funciton is called
            # Do a loop, and extract any error messages from the end of the loop
            error_store, files_tetramm, files_camera, increm_store = Looper.main_loop()
            # Now, process the messages recieved
            # The indicies of the objects match the indicies of their error messages and the indicies of the hardware widgets
            
            # Process error messages (if exists, append)
            if error_store:
                self.append_error_message(error_store)
            # Process hardware messages (if exists, append)
            if any(files_tetramm):
                self.append_to_hw_modals_tet(files_tetramm)
            if any(files_camera):
                self.append_to_hw_modals_cam(files_camera)
            if increm_store:
                self.append_to_incrementer(increm_store)
    
        # After loop done, Stop the acquisition
        for tet_obj in self.tet_dict:
            tet_obj.put_HDF_start(0)

        for cam_obj in self.cam_dict:
            cam_obj.put_HDF_start(0) 
            
    def set_stop(self):
    # Function to stop the hdf from acquiring for the hardware
    # Arguments; self
    # Returns: None

        # Stop the loop from running
        self.click = 1    

        # Enable all the buttons
        self.reset_btn.setEnabled(True)
        self.getfile_btn.setEnabled(True)
        self.export_error_btn.setEnabled(True)
        self.changed_btn.setEnabled(True)
        self.set_both_btn.setEnabled(True)

    def set_reset(self):
    # Reset the hardware and GUI (clear all error messages and reset the increment to 0)
    # Arguments; self
    # Returns: None
    #     
        # First clear everything (error messages)
        self.clear_error_message()
        self.clear_modal_message()

        # Then change the saved files to 0
        self.fc_read.setText('0')

        # Then reset the hardware objects
        for tet_obj in self.tet_dict:
            tet_obj.reset_from_diagnostics_gui()

        # Then reset the hardware objects 
        for cam_obj in self.cam_dict:
            cam_obj.reset_from_diagnostics_gui()
       
    def save_export_error(self):
    # Save the error log as a txt file in the same folder as all the other hdf5 files are located
    # Arguments; self
    # Returns: None

        # Get the file path of the hardware that exists
        if self.tet_dict:
            path_saved = self.tet_dict[0].file_path

        elif self.cam_dict:
            path_saved = self.cam_dict[0].file_path

        # Make a txt file, write the error messages to it
        f = open("%s/error_log.txt"%path_saved, "w+")
        f.write(self.errorlog.toPlainText())
        f.close()
        print ('error_log.txt saved at %s'%path_saved)

    def save_file(self):
    # Function to save a .mat file with the required information for the further analysis GUIs
    # Arguments; self
    # Returns: None

        # First, update infosaved incrementor (this is to check if the file has been created before closing the GUI)
        self.infosaved = self.infosaved + 1

        # in the .mat file, save the tetramm and camera objects
        file_save = {'Tet_Hw': self.tet_dict , 'Cam_Hw': self.cam_dict}

        # And save the path of where the hdf files are located
        if self.tet_dict:
            path_saved = self.tet_dict[0].file_path
            file_save['Path'] = path_saved
        elif self.cam_dict:
            path_saved = self.cam_dict[0].file_path
            file_save['Path'] = path_saved

        # Save the totsal number of files sqaved in the session
        file_save['Total_Files'] = int(self.fc_read.text())

        # Save the mat file in the same location
        sio.savemat('%s/Info.mat'%path_saved, file_save)

        print('Info.mat File Saved at %s'%path_saved)

    def set_changed_value(self):
    # If a value was changed, in EPICS run this script to update the global variables of the hardware objcts.
    # Arguments; self
    # Returns: None

        for tet_obj in self.tet_dict:
            tet_obj.update_all_values_from_epics() # Call external script
            # Update the number capture
            tet_num = tet_obj.number_capture
            self.tet_cap_read.setText(str(tet_num))
            # Update the nuber of files
            self.fc_read.setText(str(tet_obj.next_file))

        for cam_obj in self.cam_dict:
            cam_obj.update_all_values_from_epics()
            # Update the FPS:
            cap_num = cam_obj.number_capture
            fps = int(cap_num / int(self.gate_edit.text())) # Call external script
            self.cam_cap_read.setText(str(cap_num))
            self.cam_fps_read.setText(str(fps))
            # Update the number of files
            self.fc_read.setText(str(cam_obj.next_file))


    def append_error_message(self,error_store):
    # Append the available error messages ot the error log
    # Arguments; self
    # Returns: None
        for message in error_store:
            self.errorlog.appendPlainText(message)

    def append_to_hw_modals_tet(self,files_tetramm):
    # Append the available error messages to the Tetramm frame
    # Arguments; self
    # Returns: None
        # Extract the messages and match the indiies to the hd_t modal
        for i in range(0,len(self.hd_t)):
            if (files_tetramm[i]): # If there is something besides an empty array there (aka there is a message)
                self.hd_t[i].device_scroll.appendPlainText(files_tetramm[i][0])

    def append_to_hw_modals_cam(self,files_camera):
    # Append the available error messages to the Camera Frame
    # Arguments; self
    # Returns: None
        # Extract the messages and match the indiies to the hd_t and hd_c modals
        for i in range(0,len(self.hd_c)):
            if (files_camera[i]): # If there is something besides an empty array there
                self.hd_c[i].device_scroll.appendPlainText(files_camera[i][0])

    def append_to_incrementer(self,increm_store):
    # Increment the file count display
    # Arguments; self
    # Returns: None
        self.fc_read.setText(str(increm_store[0]))


    def clear_error_message(self):
    # Funciton to clear the error log box
    # Arguments; self
    # Returns: None
        self.errorlog.clear()

    def clear_modal_message(self):
    # Function to clear the modal messages box for all the hardware
    # Arguments; self
    # Returns: None
        for i in range(0,len(self.hd_t)):
            self.hd_t[i].device_scroll.clear()

        for i in range(0,len(self.hd_c)):
            self.hd_c[i].device_scroll.clear()
    
    def set_timeout_gate(self):
    # Fucntion to set the timoute tinme (for cothread) and gate signal time (for topup)
    # Arguments; self
    # Returns: None

        # Set the Looper values
        Looper.set_up_gate_timeout(self.timeout_edit.text(), self.gate_edit.text()) # This will update the cothread caget / put wait=True with how long they need to wait for, and the topup check with the length of the data being taken (s)

        # Enable the start stop buttons
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        self.getfile_btn.setEnabled(True)
        self.export_error_btn.setEnabled(True)
        self.changed_btn.setEnabled(True)

    def calc_timeout(self,total_seconds):
    # Calculate what default timeout value needs to be displayed based on how long the data is being taken for:
    # Arguments; self
    # Returns: the timout required

        if (total_seconds < 30):
            timeout_text = 5
        elif (30 <= total_seconds < 60):
            timeout_text = 6
        elif (60 <= total_seconds < 90):
            timeout_text = 7
        elif (90 <= total_seconds < 120):
            timeout_text = 8
        else: 
            timeout_text = 10

        return timeout_text


    def initUI(self,hd_t,hd_c,tet_dict,cam_dict,total_seconds,beamline_name, beamline_topup):
    # Main intialiser function
        
        # add the objects to self so that they can be accessible to every function
        self.hd_t = hd_t # arrays of the side frames for the tetramm (Hardware class)
        self.hd_c = hd_c # arrays of the side frames for the camera (Hardware class)
        self.tet_dict = tet_dict
        self.cam_dict = cam_dict
        
        # Set the layout:
        main_layout = QHBoxLayout()

        # Add fonts:
        QFontDatabase.addApplicationFont("Landasans_Light.otf")
        QFontDatabase.addApplicationFont("Landasans_Medium.otf")

        font_medium = QFont("Landasans Medium")
        font_light = QFont("Landasans Ultra Light")

        # Consider the left hand side
        # Add appropriate layouts:
        left_main_layout = QVBoxLayout()
        logo_layout = QHBoxLayout()
        hardware_display_layout = QHBoxLayout()

        # Create the required widgets and add them to the layout
        # Diamond Logo set up
        self.diamond = QLabel(self)
        pixmap = QPixmap('Diamond.png')
        pixmap = pixmap.scaledToHeight(70)
        self.diamond.setPixmap(pixmap)
        self.diamond.setAlignment(Qt.AlignLeft)
        self.diamond.setObjectName('DiamondLogo')
        # Diagnostics Team Label
        d_label = QLabel(self)
        d_label.setText('Diagnostics Monitor:')
        d_label.setFont(font_medium)
        d_label.setObjectName("DLabel")
        d_label.setAlignment(Qt.AlignLeft)

        # Add the widgets to the layouts
        logo_layout.addWidget(self.diamond, stretch = 0.99)
        logo_layout.addWidget(d_label, stretch = 1.1)

        # Hardware devices:
        m_label = QLabel(self)
        m_label.setText('Monitor Hardware')
        m_label.setFont(font_light)
        m_label.setObjectName("MLabel")
        m_label.setAlignment(Qt.AlignLeft)

        # Add the scrollarea
        scroll_hardware = QScrollArea(self)
        scroll_widget = QWidget(self)

        # For each of the devices in hd_t and c, add it to the layout
        for i in range(0,len(self.hd_t)):
            hardware_display_layout.addWidget(self.hd_t[i])

        for i in range(0,len(self.hd_c)):
            hardware_display_layout.addWidget(self.hd_c[i])            
        
        scroll_widget.setLayout(hardware_display_layout)

        # Scroll Settings
        scroll_hardware.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_hardware.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_hardware.setWidgetResizable(False)
        scroll_hardware.setWidget(scroll_widget)

        # Add all the left hand layouts
        left_main_layout.addLayout(logo_layout)
        left_main_layout.addWidget(m_label)
        left_main_layout.addWidget(scroll_hardware)

        main_layout.addLayout(left_main_layout, stretch = 1)

        # Right hand side widgets and layouts
        right_main_layout = QVBoxLayout()
        beamline_layout = QHBoxLayout()
        data_h_layout = QHBoxLayout()
        data_v_layout_left = QVBoxLayout()
        data_v_layout_right = QVBoxLayout()
        data_v_layout_center = QVBoxLayout()
        timeout_h_layout = QHBoxLayout()
        buttons_layout = QHBoxLayout()

        # Beamline Label:
        beam_label = QLabel(self)
        beam_label.setText('%s:   '%beamline_name)
        beam_label.setFont(font_medium)
        beam_label.setObjectName("BeamLabel")
        beam_label.setAlignment(Qt.AlignRight)

        # Beamline Img:
        self.beamline= QLabel(self)
        bpixmap = QPixmap('BeamSchemAnno.png')
        bpixmap = bpixmap.scaledToHeight(130)
        self.beamline.setPixmap(bpixmap)
        self.beamline.setAlignment(Qt.AlignLeft)
        self.beamline.setObjectName('BeamlineSchematic')

        beamline_layout.addWidget(beam_label)
        beamline_layout.addWidget(self.beamline)

        # Data Displayer:
        # Labels and Text Displays:
        filecount_label = QLabel(self)
        filecount_label.setText('Saved Files:')
        filecount_label.setFont(font_light)
        filecount_label.setAlignment(Qt.AlignLeft)

        # File coutn read
        self.fc_read = QLineEdit()
        self.fc_read.setReadOnly(True)
        self.fc_read.setText("0") # Starts at no files saved

        # Number of Seconds
        sec_label = QLabel(self)
        sec_label.setText('Seconds:')
        sec_label.setFont(font_light)
        sec_label.setAlignment(Qt.AlignLeft)

        self.sec_read = QLineEdit()
        self.sec_read.setReadOnly(True)
        self.sec_read.setText(str(total_seconds))
        
        # Capture number
        tet_cap_label = QLabel(self)
        tet_cap_label.setText('TetrAMM Capture Num:')
        tet_cap_label.setFont(font_light)
        tet_cap_label.setAlignment(Qt.AlignLeft)

        self.tet_cap_read = QLineEdit()
        self.tet_cap_read.setReadOnly(True)
        self.tet_cap_read.setObjectName('tet_cap_read')

        # Show the Tetramm Capture Number if there are any tetramms:
        if self.tet_dict: # if there are values
            cap_num = self.tet_dict[0].number_capture
            self.tet_cap_read.setText(str(cap_num))
        else: # if ther are no tetramms disable the field
            self.tet_cap_read.setEnabled(False)
            self.tet_cap_read.setStyleSheet('''
                #tet_cap_read {
                font-size: 15px;
                background-color: gray;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                max-width: 6em;
            }''') 

        cam_cap_label = QLabel(self)
        cam_cap_label.setText('Camera Capture Num:')
        cam_cap_label.setFont(font_light)
        cam_cap_label.setAlignment(Qt.AlignLeft)

        self.cam_cap_read = QLineEdit()
        self.cam_cap_read.setReadOnly(True)
        self.cam_cap_read.setObjectName('cam_cap_read')

        cam_fps_label = QLabel(self)
        cam_fps_label.setText('Camera FPS:')
        cam_fps_label.setFont(font_light)
        cam_fps_label.setAlignment(Qt.AlignLeft)

        self.cam_fps_read = QLineEdit()
        self.cam_fps_read.setReadOnly(True)
        self.cam_fps_read.setObjectName('cam_fps_read')

        # Show the Camera Capture Number and fps if there are any cameras:
        if self.cam_dict: # if there are values 
            cap_num = self.cam_dict[0].number_capture
            fps = int(cap_num / total_seconds)
            self.cam_cap_read.setText(str(cap_num))
            self.cam_fps_read.setText(str(fps))
        else: # if there are no cams disable the field
            self.cam_cap_read.setEnabled(False)
            self.cam_fps_read.setEnabled(False)
            self.cam_cap_read.setStyleSheet('''
                #cam_cap_read {
                font-size: 15px;
                background-color: gray;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                max-width: 6em;
            }''') 
            self.cam_fps_read.setStyleSheet('''
                #cam_fps_read {
                font-size: 15px;
                background-color: gray;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                max-width: 6em;
            }''')             

        # Add the data to the layouts
        data_v_layout_left.addWidget(filecount_label)
        data_v_layout_left.addWidget(self.fc_read)
        data_v_layout_left.addWidget(tet_cap_label)
        data_v_layout_left.addWidget(self.tet_cap_read)

        data_v_layout_center.addWidget(sec_label)
        data_v_layout_center.addWidget(self.sec_read)
        data_v_layout_center.addWidget(cam_cap_label)
        data_v_layout_center.addWidget(self.cam_cap_read)

        # Create empty labels to preserve shape
        el_1 = QLabel(self)
        el_1.setText(' ')
        el_2 = QLabel(self)
        el_2.setText(' ')

        data_v_layout_right.addWidget(el_1)
        data_v_layout_right.addWidget(el_2)
        data_v_layout_right.addWidget(cam_fps_label)
        data_v_layout_right.addWidget(self.cam_fps_read)

        data_h_layout.addLayout(data_v_layout_left)
        data_h_layout.addLayout(data_v_layout_center)
        data_h_layout.addLayout(data_v_layout_right)

        # Timeout section: lable, editor, button
        timeout_label = QLabel(self)
        timeout_label.setText('Timeout:')
        timeout_label.setFont(font_medium)
        timeout_label.setObjectName("TimeoutLabel")
        timeout_label.setAlignment(Qt.AlignLeft)

        self.timeout_edit = QLineEdit()
        self.timeout_edit.setAlignment(Qt.AlignLeft)
        self.timeout_edit.setObjectName('TimeoutEditor')
        # Set the timeout as calculated
        self.timeout_edit.setText(str(self.calc_timeout(total_seconds)))

        self.timeout_help_btn = QPushButton(self)
        self.timeout_help_btn.setText('')
        self.timeout_help_btn.setObjectName('TimeoutHelpBtn')
        self.timeout_help_btn.setFixedWidth(50)
        self.timeout_help_btn.clicked.connect(self.get_timeout_help)

        gate_label = QLabel(self)
        gate_label.setText('Gate Signal:')
        gate_label.setFont(font_medium)
        gate_label.setObjectName("GateLabel")
        gate_label.setAlignment(Qt.AlignLeft)

        self.gate_edit = QLineEdit()
        self.gate_edit.setAlignment(Qt.AlignLeft)
        self.gate_edit.setObjectName('GateEditor')
        self.gate_edit.setText(str(total_seconds)) # Set as the total number of seocnds data is being acquired for
 
        self.set_both_btn = QPushButton(self) # Set button
        self.set_both_btn.setText('S E T')
        self.set_both_btn.setFont(font_medium)
        self.set_both_btn.setObjectName('SetBtn')
        self.set_both_btn.clicked.connect(self.set_timeout_gate)
        
        timeout_h_layout.addStretch(1)
        timeout_h_layout.addWidget(timeout_label)
        timeout_h_layout.addWidget(self.timeout_edit)
        timeout_h_layout.addWidget(gate_label)
        timeout_h_layout.addWidget(self.gate_edit)
        timeout_h_layout.addWidget(self.set_both_btn)

        timeout_h_layout.addWidget(self.timeout_help_btn)
        timeout_h_layout.addStretch(1)

        # Error log: label, log
        errorlog_label = QLabel(self)
        errorlog_label.setText('ERROR LOG')
        errorlog_label.setFont(font_medium)
        errorlog_label.setObjectName("ErrorLogLabel")
        errorlog_label.setAlignment(Qt.AlignHCenter)
        
        self.errorlog = QPlainTextEdit(self)
        self.errorlog.setReadOnly(True)


        # Bottom Buttons, and the functions they conncet to 9clicked.connect(self.function))
        self.start_btn = QPushButton(self)
        self.start_btn.setText('ARM')
        self.start_btn.setObjectName('StartBtn')
        self.start_btn.setFont(font_medium)
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.set_start)

        self.stop_btn = QPushButton(self)
        self.stop_btn.setText('STOP')
        self.stop_btn.setObjectName('StopBtn')
        self.stop_btn.setFont(font_medium)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.set_stop)

        self.reset_btn = QPushButton(self)
        self.reset_btn.setText('RESET')
        self.reset_btn.setObjectName('ResetBtn')
        self.reset_btn.setFont(font_medium)
        self.reset_btn.setEnabled(False)
        self.reset_btn.clicked.connect(self.set_reset)

        self.getfile_btn = QPushButton(self)
        self.getfile_btn.setText('EXPORT FILE')
        self.getfile_btn.setObjectName('ExportBtn')
        self.getfile_btn.setFont(font_medium)
        self.getfile_btn.setEnabled(False)
        self.getfile_btn.clicked.connect(self.save_file)
        
        self.changed_btn = QPushButton(self)
        self.changed_btn.setText('CHANGED EPICS')
        self.changed_btn.setObjectName('ChangedBtn')
        self.changed_btn.setFont(font_medium)
        self.changed_btn.setEnabled(False)
        self.changed_btn.clicked.connect(self.set_changed_value)

        self.export_error_btn = QPushButton(self)
        self.export_error_btn.setText('EXPORT LOG')
        self.export_error_btn.setObjectName('ExportLogBtn')
        self.export_error_btn.setFont(font_medium)
        self.export_error_btn.setEnabled(False)
        self.export_error_btn.clicked.connect(self.save_export_error)

        self.help_btn = QPushButton(self)
        self.help_btn.setText('')
        self.help_btn.setObjectName('HelpBtn')
        self.help_btn.setFixedWidth(50)

        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.stop_btn)
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addWidget(self.changed_btn)
        buttons_layout.addWidget(self.getfile_btn)
        buttons_layout.addWidget(self.export_error_btn)
        buttons_layout.addWidget(self.help_btn)

        # Add all the layouts to the main vertical layout
        right_main_layout.addLayout(beamline_layout)
        right_main_layout.addLayout(data_h_layout)
        right_main_layout.addLayout(timeout_h_layout)
        right_main_layout.addWidget(errorlog_label)
        right_main_layout.addWidget(self.errorlog)
        right_main_layout.addLayout(buttons_layout)

        main_layout.addLayout(right_main_layout, stretch = 1)

        self.setLayout(main_layout)
       

class MainWindow(QMainWindow):
# Main application window
    def __init__(self,ml):
        super().__init__()
        self.setStyleSheet('''
            QWidget {
                    background: #B6D0E2;
                }

                QScrollArea {
                    background: #B6D0E2;
                    border: 6px solid;
                    border-color: #191970;
                    border-radius: 10px;
                }
                
                #file_display_scroll {
                    background: white;
                    border-color: #B6D0E2;
                }

                QLabel {
                    font-size: 20px;
                    color: #191970;

                }

                #DLabel {
                    font-size: 60px;
                    color: #191970;
                    font-weight: bold;
                    padding-top: 0px;
                    padding-left: 12px;
                }

                #device_name_label {
                    font-size: 40px;
                    color: #191970;
                    background-color: white;
                    font-weight: bold;
                }

                #device_type_label {
                    font-size: 30px;
                    color: red;
                    background-color: white;
                }

                #DiamondLogo {

                    border-right :3px solid blue;
                    border-color: #191970;
                    padding-right: 16px;
                    padding-bottom: 5px;
                    padding-top: 1px;
                }

                #MLabel {
                    font-size: 30px;
                    padding-left: 5px;
                
                }

                #BeamLabel {
                    font-size: 80px;
                    padding-top: 20px;
                
                }

                #TimeoutLabel {
                    padding-top: 4px;
                    padding-right:-6px;
                
                }

                #GateLabel {
                    padding-top: 4px;
                    padding-right:-6px;                

                }

                QLineEdit {
                    font-size: 15px;
                    background-color: white;
                    border: 2px solid white;
                    border-radius: 5px;
                    padding: 1px 18px 1px 3px;
                    max-width: 6em;
                
                }

                QPushButton {
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

                #SetBtn {
                    font: bold 15px;
                    width: 40px;
                    height: 20px;
                    border-width: 5px;
                    border-radius: 10px;
                    padding: 3px;

                }

                #TimeoutHelpBtn {
                    image: url("help.png");
                    font: bold 15px;
                    width: 15px;
                    height: 20px;
                    border-width: 5px;
                    border-radius: 10px;
                    padding: 3px;
                }

                #HelpBtn {
                    image: url("help.png");
                    font: bold 20px;
                    width: 30px;
                }

                #ErrorLogLabel {
                    font-size: 30px;
                    border-top :3px solid;
                    border-color: #191970;

                }

                QTextPlainTextEdit {
                    background: white;
                    border: 6px solid;
                    border-color: #191970;
                    border-radius: 10px;

                }

                Hardware_Device {
                    background-color: white;
                    border: 6px solid;
                    border-color: #191970;
                    border-radius: 10px;

                }

            ''')
        self.ml = ml
        self.setWindowTitle(' ')
        self.initUI(ml) # Use the preinitialised layout class to add to the app

    def closeEvent(self, event):
    # Function to determine whether the Info file has been saved before closing
    # Arguments; self
    # Returns: None

        # if the info file has been saved and the x button is pressed, close the gui (accept the close event)
        if (self.ml.infosaved > 0) or (self.ml.closeclick > 0): # If the x button is pressed twice, then closeclick will fulfil this condition regardless of whether the file was saved or not, and the GUI will close
            event.accept()
        else: # If it hasnt been saves, increment the closeclick variable and make the button red to draw attention to it
            self.ml.closeclick = self.ml.closeclick + 1
            self.ml.getfile_btn.setStyleSheet('''QPushButton {background-color: red;}''')
            event.ignore()

    def initUI(self,ml):
    # Main initialiser
        self.setCentralWidget(ml)
        self.resize(1200,700)

''' '''

# In case you want to run this without the main script
''' Exectue Main '''
if __name__ == '__main__':
    app = create_app()
    hd_t = [Hardware_Device('bob',0)]
    hd_c = [Hardware_Device('bobv',0)]
    ml = MainLayout(hd_t,hd_c,[],[],20,'BLI19', 'LOL')
    demo = MainWindow(ml)
    demo.show()
    sys.exit(app.exec_())

''' '''