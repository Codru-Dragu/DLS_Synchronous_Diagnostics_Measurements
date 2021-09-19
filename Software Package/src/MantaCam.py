# Class to set up MantaCam Objects with appropriate parameters

# IMPORTS #
import cothread
from cothread.catools import *
import h5py
import time

# CLASS MantaCam #
class MantaCam:
    # Class Variables - Default for all MantaCams - changed via MantaCam.values_pre_reading = djfkwejkf
    
    # Variables to populate the CAM PVs
    # EDITABLE #
    gain = 0
    binning_x = 1
    binning_y = 1
    reg_start_x = 450
    reg_start_y = 400
    reg_size_x = 60
    reg_size_y = 60
    exposure =  '0.00002'
    acq_period = '0.001982'
    # UNEDITABLE # 
    enable_arr = 1 # Enabled
    # Trigger settings - can be found in Features#1 and imgMode to trigg_source are found in the mian CAM tab
    img_mode = 2 # Image mode set to continuous
    trigg_mode = 1 # Trigger mode on
    trigg_source = 1 # Trigger source: Line 1 (input trigger pin 1, whcih is compatible with the trigger cable)
    trigg_selector = 0 # Frame Start
    trigg_activation = 3 # LevelHigh

    # Variables to populate HDF5 PVs - can change these as defaults
    # EDITABLE # 
    number_capture = 7080 # 30 seconds worth of data default. Calculation: capture number = fps * 30
    file_format = '%s%s_%04d.h5' # HDF5 file type 
    frames_per_second = 0
    # UNEDISTABLE # 
    capture_mode = 1 # Capture mode capture (single = 0, stream = 2)
    auto_increment = 1 # Yes
    auto_save = 0 # No
    next_file = 0 # Default first file for the name
    hdf_file_format = 0 # Selects HDF5 from dropdown menu in MantaCam GUI

    # Blank field placeholder for caput functions with text
    blank = [256,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    # Timeout time:
    timeout = 4

    def __init__(self,pv,fp,fn):
    # Initialised method to call when initialising instances
        # Set the PV, file path and the name 

        self.pv = pv # PV name, eg TS-DI-DCAM-02
        self.file_path = fp # Path of location
        self.file_name = fn # Name of this generation of files
        self.fps = MantaCam.frames_per_second
        self.bin_x = MantaCam.binning_x # FOr the magnification calculation

        # SAFETY CLAUSE #
        # This is to stop the MantaCam continuously saving files in an uncontrollable fashion
        if ((MantaCam.capture_mode == 0) and (MantaCam.auto_save ==1)):
            MantaCam.capture_mode = 1 # Make sure capture mode is never set to single whilst auto save is also 1

        MantaCam.set_up_CAM(self,self.pv)
        MantaCam.set_up_HDF(self,self.pv)
        
    def return_name(self):
        return self.file_name

    def return_path(self):
        return self.file_path

    def set_up_CAM(self,device):
    # Function to set up some QE1 PVs and stop and start acquiring data
    # Arguments: self, device: pv name, Returns: None

        caput ('%s:CAM:Acquire'%device, 0) # First, Stop aquiring data
        caput ('%s:CAM:TriggerSource'%device, 0) # MAKE 0 FIRST 
        caput ('%s:CAM:TriggerSource'%device, MantaCam.trigg_source) # Put to external trigger, LINE 1
        caput ('%s:CAM:TriggerMode'%device, MantaCam.trigg_mode) # Trigger mode on
        caput ('%s:CAM:GC_TriggerActivation'%device, MantaCam.trigg_activation) # Trigger activation level high
        caput ('%s:CAM:ImageMode'%device, MantaCam.img_mode) # Image mode continuous

        # Put the appriopriate values
        caput ('%s:CAM:Gain'%device, MantaCam.gain)
        caput ('%s:CAM:BinX'%device, MantaCam.binning_x)
        caput ('%s:CAM:BinY'%device, MantaCam.binning_y)
        caput ('%s:CAM:MinX'%device, MantaCam.reg_start_x)
        caput ('%s:CAM:MinY'%device, MantaCam.reg_start_y)
        caput ('%s:CAM:SizeX'%device, MantaCam.reg_size_x)
        caput ('%s:CAM:SizeY'%device, MantaCam.reg_size_y)
        
        caput ('%s:CAM:AcquirePeriod'%device, MantaCam.acq_period)
        caput ('%s:CAM:AcquireTime'%device, MantaCam.exposure)

        caput ('%s:ARR:EnableCallbacks'%device, MantaCam.enable_arr)

    def set_up_HDF(self, device):
    # Function to caput the user-specified or default arguments to edit the HDF5 data aquisition options
    # Arguments: self, device: the pv name

        # Convert the strings to ascii    
        fp_ascii = MantaCam.text_ascii_converter(self,self.file_path,0)
        fn_ascii = MantaCam.text_ascii_converter(self,self.file_name,0)  
        ff_ascii = MantaCam.text_ascii_converter(self,MantaCam.file_format,0)

        # BLANK the fields if not already blank - if you try to overwrite a shorter word onto a previously longer word without blanking, the short word will merge with the tail of the long word
        caput ('%s:HDF5:FilePath'%device, MantaCam.blank) # file path
        caput ('%s:HDF5:FileName'%device, MantaCam.blank) # file name
        caput ('%s:HDF5:FileTemplate'%device, MantaCam.blank) # file template

        # Put all the set up values in the appropriate PVs
        caput ('%s:HDF5:EnableCallbacks'%device, 1) # ENABLE THE HDF FILE - HARDCODED
        caput ('%s:HDF5:FilePath'%device,fp_ascii) # file path
        caput ('%s:HDF5:FileName'%device,fn_ascii) # file name
        caput ('%s:HDF5:FileTemplate'%device,ff_ascii) # file format
        caput ('%s:HDF5:NumCapture'%device,MantaCam.number_capture) # num captures
        caput ('%s:HDF5:FileWriteMode'%device, MantaCam.capture_mode) # capture mode
        caput ('%s:HDF5:AutoIncrement'%device, MantaCam.auto_increment) # auto increment
        caput ('%s:HDF5:AutoSave'%device, MantaCam.auto_save) # auto save
        caput ('%s:HDF5:FileNumber'%device, MantaCam.next_file) # next file
        caput ('%s:HDF5:FileFormat'%device, MantaCam.hdf_file_format) # set file format to hdf5
        caput ('%s:HDF5:DroppedArrays'%device, 0) # Set the dropped arrays to 0

        caput ('%s:CAM:Acquire'%device, 1) # After CAM and HDF set up, begin aquiring data

    def get_HDF_start(self):
    # Function to read the capture read back value to determine weather the capture is finished or not
    # Arguments: None, Returns: None
        return caget ('%s:HDF5:Capture_RBV'%self.pv)

    def put_HDF_start(self, togg):
    # Function to set the start capture button to start or stop
    # Arguments togg (toggle boolean: 1 for start, 0 for stop), Retruns: None
        caput('%s:HDF5:Capture'%self.pv, togg) # Start HDF5
        caget('%s:HDF5:Capture'%self.pv) # To make sure it runs

    def put_WriteFile(self, togg):
    # Write the file ancd check if it was written
        # Get the current file number
        curr_val = caget ('%s:HDF5:FileNumber_RBV'%self.pv) 

        # Write the File
        success = caput('%s:HDF5:WriteFile'%self.pv, togg, timeout=MantaCam.timeout,wait=True,throw = False) # Write Camera, WITH WAIT = TRUE

        # Get the new value
        time.sleep(3)
        new_val = caget ('%s:HDF5:FileNumber_RBV'%self.pv)

        # Check for increment 
        increment_check = (curr_val != new_val)

        # Return verdict - sometimes it says it hasnt saved but it actually has.
        return (success.ok or increment_check) 

        # Truth Table:
        # sucess.ok                 increm_check                RESULT - as you can see this is an or function
        #   0 (nosave)               0 (noincrement)            0 (not actually saved)
        #   1 (save)                 0 (will not happen)        
        #   0 (nosave)               1 (incememnt)              1 (actually saved) - sometimes it gives false but it increments and actually saves
        #   1 (save)                 1 (incrememnt)             1 (actually saved)     

    def set_dropped(self):
    # Set dropped frames 0
        caput ('%s:HDF5:DroppedArrays'%self.pv, 0)
        caget ('%s:HDF5:DroppedArrays'%self.pv)

    def get_dropped(self):
    # Get dropped frames
        return caget ('%s:HDF5:DroppedArrays_RBV'%self.pv)

    def put_Acquire(self, togg):
        caput ('%s:CAM:Acquire'%self.pv, togg)
        caget ('%s:CAM:Acquire'%self.pv)

    def get_fps(self):
    # Get current fps
        return caget('%s:CAM:ArrayRate_RBV'%self.pv)

    def get_fps_default(self):
    # Return default fps
        return self.fps

    def get_current_increment(self):
        val = caget ('%s:HDF5:FileNumber_RBV'%self.pv)
        return val

    def set_increment(self):
        curr_val = caget ('%s:HDF5:FileNumber_RBV'%self.pv)
        caput('%s:HDF5:FileNumber'%self.pv, (curr_val + 1)) 

    def set_increment_minus(self):
        curr_val = caget ('%s:HDF5:FileNumber_RBV'%self.pv)
        caput('%s:HDF5:FileNumber'%self.pv, (curr_val - 1)) 

    def set_increment_restart(self):
        caput('%s:HDF5:FileNumber'%self.pv, 0) 
        caget('%s:HDF5:FileNumber'%self.pv) 

    def reset(self):
        # This will be called after acquisition has stopped
        print('Am resetting (MantaCam)')
        # Convert to freerun:
        caput ('%s:CAM:TriggerSource'%self.pv, 0)
        # Reset some values:
        caput ('%s:CAM:AcquirePeriod'%self.pv, MantaCam.acq_period)
        caput ('%s:CAM:AcquireTime'%self.pv, MantaCam.exposure)
        caput ('%s:ARR:EnableCallbacks'%self.pv, MantaCam.enable_arr)
        caput ('%s:HDF5:DroppedArrays'%self.pv, 0) # Reset Dropped Arrays
        caput ('%s:ARR:DroppedArrays'%self.pv, 0) # Reset Dropped Arrays
        # Let Acquire for 3 seconds:
        caput ('%s:CAM:Acquire'%self.pv, 1) 
        time.sleep(3)
        # Stop and set to trigger externally, do not start acquiring yet
        caput ('%s:CAM:Acquire'%self.pv, 0)
        caput ('%s:CAM:TriggerSource'%self.pv, MantaCam.trigg_source)
        print('Done resetting (MantaCam), Acquire is off')


    def reset_from_diagnostics_gui(self):
    # Function to reset all the values with the origial values. Calls reset function but adds acquire
    # Arguments: None
    # Returns: None        
        # Reset the HDF values and CAM values, using the preexisting methods:
        # Stop Acquiring
        MantaCam.put_Acquire(self,0)
        time.sleep(0.5) # Wait
        MantaCam.reset(self)
        MantaCam.set_increment_restart(self)
        time.sleep(0.5)
        # Put the other important values that are not present in reset
        caput ('%s:CAM:Gain'%self.pv, MantaCam.gain)
        caput ('%s:CAM:BinX'%self.pv, MantaCam.binning_x)
        caput ('%s:CAM:BinY'%self.pv, MantaCam.binning_y)
        caput ('%s:CAM:MinX'%self.pv, MantaCam.reg_start_x)
        caput ('%s:CAM:MinY'%self.pv, MantaCam.reg_start_y)
        caput ('%s:CAM:SizeX'%self.pv, MantaCam.reg_size_x)
        caput ('%s:CAM:SizeY'%self.pv, MantaCam.reg_size_y)
        time.sleep(0.5)
        MantaCam.put_Acquire(self,1)
        print('Acquisition on (MantaCam)')

    def update_all_values_from_epics(self):
    # Funciton to update the class values from the epics values
    # Arguments: None
    # Returns: None
        MantaCam.put_Acquire(self,0)

        # Grab all the data needed from the CAM page
        MantaCam.acq_period = caget ('%s:CAM:AcquirePeriod_RBV'%self.pv)
        MantaCam.exposure = caget ('%s:CAM:AcquireTime_RBV'%self.pv)
        MantaCam.gain = caget ('%s:CAM:Gain'%self.pv)
        MantaCam.binning_x = caget ('%s:CAM:BinX'%self.pv)
        MantaCam.binning_y = caget ('%s:CAM:BinY'%self.pv)
        MantaCam.reg_start_x = caget ('%s:CAM:MinX'%self.pv)
        MantaCam.reg_start_y = caget ('%s:CAM:MinY'%self.pv)
        MantaCam.reg_size_x = caget ('%s:CAM:SizeX'%self.pv)
        MantaCam.reg_size_y = caget ('%s:CAM:SizeY'%self.pv)

        # Grab all the data needed from the HDF page
        
        # Convert the ascii to strings   
        fp_ascii = caget ('%s:HDF5:FilePath'%self.pv) # file path
        fn_ascii = caget ('%s:HDF5:FileName'%self.pv) # file name
        ff_ascii = caget ('%s:HDF5:FileTemplate'%self.pv) # file format

        self.file_path = MantaCam.text_ascii_converter(self,fp_ascii,1)
        self.file_name = MantaCam.text_ascii_converter(self,fn_ascii,1)  
        MantaCam.file_format = MantaCam.text_ascii_converter(self,ff_ascii,1)

        MantaCam.number_capture = caget ('%s:HDF5:NumCapture_RBV'%self.pv) # num captures
        MantaCam.next_file = caget ('%s:HDF5:FileNumber_RBV'%self.pv) # next file
 
        # Update the FPS
        MantaCam.put_Acquire(self,1) # After CAM and HDF set up, begin aquiring data
        caput ('%s:CAM:TriggerSource'%self.pv, 0) # Put to freerun
        caget ('%s:CAM:TriggerSource'%self.pv) # Put to freerun
        time.sleep(4)
        MantaCam.frames_per_second = caget ('%s:CAM:ArrayRate_RBV'%self.pv)
        self.fps = MantaCam.frames_per_second
        self.bin_x = MantaCam.binning_x
        time.sleep(3)
        caput ('%s:CAM:TriggerSource'%self.pv, 1) # Put to external trigger
        caget ('%s:CAM:TriggerSource'%self.pv) # Put to freerun

        print('Done updating class values from EPICS (MantaCam)')


    def text_ascii_converter(self, content, option):
    # Function to convert text to ascii and vice versa for caput commands into the filepath and other writable regions
    # Arguments: content: the text of ascii array, option: the boolean 0 for text to ascii, or 1 for vice versa, Returns: the converted text/ascii
            if option == 0: # text to ascii conversion
                extracted = [ord(c) for c in content]
            else: # ascii to text conversion 
                extracted = ''.join(chr(c) for c in content)

            return extracted

#MantaCam.number_capture = 2100
#e = MantaCam('TS-DI-DCAM-01','/home/dqi23796/Delay','camcam')
