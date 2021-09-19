# Class to set up TetrAMM Objects with appropriate parameters

# IMPORTS #
import cothread
from cothread.catools import *
import h5py
import time

# CLASS TETRAMM #
class TetrAMM:
    # Class Variables - Default for all TetrAmms 
    # NOTE: THESE VALUES WILL CHANGE WHEN THE FIRST TETRAMM OBJECT IS SET 
    
    # Variables to populate the QE1 PVs 
    # EDITABLE FROM GUI
    values_per_reading = 5 # These values give a default of 2000 data points to average
    averaging_time = 0.10  # number of data points = averaging_time / values_per_reading * 10e5

    # Variables to populate HDF5 PVs - can change these as defaults
    # EDITABLE FROM GUI
    number_capture = 100 # 30 seconds worth of data default. Calculation: capture = seconds * 10. (each capture is per 0.1 seconds, so total number of seconds is capture * 0.1) 
    file_format = '%s%s_%04d.h5' # HDF5 file type 
    # NON EDITABLE
    capture_mode = 1 # Capture mode capture (single = 0, stream = 2)
    auto_increment = 1 # Yes
    auto_save = 0 # No
    next_file = 0 # Default first file for the name
    hdf_file_format = 0 # Selects HDF5 from dropdown menu in TetrAMM GUI

    # Blank field placeholder for caput functions with text
    blank = [256,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    # Timeout variable
    timeout = 3

    def __init__(self,pv,fp,fn):
    # Initialised method to call when initialising instances
        # Set the PV, file path and the name 
        self.pv = pv # PV name, eg TS-DI-QEM-0e1
        self.file_path = fp # Path of location
        self.file_name = fn # Name of this generation of files

        # SAFETY CLAUSE #
        # This is to stop the TetrAMM continuously saving files in an uncontrollable fashion
        if ((TetrAMM.capture_mode == 0) and (TetrAMM.auto_save ==1)):
            TetrAMM.capture_mode = 1 # Make sure capture mode is never set to single whilst auto save is also 1
        
        TetrAMM.set_up_QE1(self,self.pv)
        TetrAMM.set_up_HDF(self,self.pv)
        
    def return_name(self):
        return self.file_name

    def return_path(self):
        return self.file_path

    def return_trigger_check(self):
    # Check if the mean value has chanegs or not. If not, the trigger is paused, if so it is not paused
    # Arguments: self
    # Returns: Difference between two recorded values 
        test1 = float(caget ('%s:PosX:MeanValue_RBV'%self.pv))
        time.sleep(0.1)
        test2 = float(caget ('%s:PosX:MeanValue_RBV'%self.pv))

        return (test1-test2)

    def set_up_QE1(self,device):
    # Function to set up some QE1 PVs and stop and start acquiring data
    # Arguments: self, device: pv name, Returns: None

        caput ('%s:DRV:Acquire'%device, 0) # First, Stop aquiring data
        caput ('%s:DRV:TriggerMode'%device, 3) # Put to external trigger

        # Put all the set up values in the appropriate PVs
        caput ('%s:DRV:ValuesPerRead'%device, TetrAMM.values_per_reading) 
        caput ('%s:DRV:AveragingTime'%device, TetrAMM.averaging_time)

    def set_up_HDF(self, device):
    # Function to caput the user-specified or default arguments to edit the HDF5 data aquisition options
    # Arguments: self, device: the pv name

        # Convert the strings to ascii    
        fp_ascii = TetrAMM.text_ascii_converter(self,self.file_path,0)
        fn_ascii = TetrAMM.text_ascii_converter(self,self.file_name,0)  
        ff_ascii = TetrAMM.text_ascii_converter(self,TetrAMM.file_format,0)

        # BLANK the fields if not already blank - if you try to overwrite a shorter word onto a previously longer word without blanking, the short word will merge with the tail of the long word
        caput ('%s:HDF5:FilePath'%device, TetrAMM.blank) # file path
        caput ('%s:HDF5:FileName'%device, TetrAMM.blank) # file name
        caput ('%s:HDF5:FileTemplate'%device, TetrAMM.blank) # file template
        
        # Put all the set up values in the appropriate PVs
        caput ('%s:HDF5:EnableCallbacks'%device, 1) # ENABLE THE HDF FILE - HARDCODED
        caput ('%s:HDF5:FilePath'%device,fp_ascii) # file path
        caput ('%s:HDF5:FileName'%device,fn_ascii) # file name
        caput ('%s:HDF5:FileTemplate'%device,ff_ascii) # file format
        caput ('%s:HDF5:NumCapture'%device,TetrAMM.number_capture) # num captures
        caput ('%s:HDF5:FileWriteMode'%device, TetrAMM.capture_mode) # capture mode
        caput ('%s:HDF5:AutoIncrement'%device, TetrAMM.auto_increment) # auto increment
        caput ('%s:HDF5:AutoSave'%device, TetrAMM.auto_save) # auto save
        caput ('%s:HDF5:FileNumber'%device, TetrAMM.next_file) # next file
        caput ('%s:HDF5:FileFormat'%device, TetrAMM.hdf_file_format) # set file format to hdf5
        
        caput ('%s:DRV:Acquire'%device, 1) # After QE1 and HDF set up, begin aquiring data

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

        # Get the current file number
        curr_val = caget ('%s:HDF5:FileNumber_RBV'%self.pv)

        # Write the File
        success = caput('%s:HDF5:WriteFile'%self.pv, togg, timeout=TetrAMM.timeout,wait=True, throw = False) # Write Tetramm, WITH WAIT = TRUE

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


    def put_Acquire(self, togg):
    # Start or stop acquisition
        caput ('%s:DRV:Acquire'%self.pv, togg)
        caget ('%s:DRV:Acquire'%self.pv) # to make sure it runs
        
    def get_current_increment(self):
    # Return increment number
        val = caget ('%s:HDF5:FileNumber_RBV'%self.pv)
        return val

    def set_increment(self):
    # Increment + 1
        curr_val = caget ('%s:HDF5:FileNumber_RBV'%self.pv)
        caput('%s:HDF5:FileNumber'%self.pv, (curr_val + 1)) 
    
    def set_increment_minus(self):
    # Incremetn - 1 
        curr_val = caget ('%s:HDF5:FileNumber_RBV'%self.pv)
        caput('%s:HDF5:FileNumber'%self.pv, (curr_val - 1)) 

    def set_increment_restart(self):
    # Reset to 0
        caput('%s:HDF5:FileNumber'%self.pv, 0) 
        caget('%s:HDF5:FileNumber'%self.pv) 


    def reset(self):
        # This will be called after acquisition has stopped
        print('Am resetting (Tetramm)')
        # Convert to freerun:
        caput ('%s:DRV:TriggerMode'%self.pv, 0)
        # Reset some values:
        caput ('%s:DRV:ValuesPerRead'%self.pv, TetrAMM.values_per_reading) 
        caput ('%s:DRV:AveragingTime'%self.pv, TetrAMM.averaging_time)
        # Let Acquire for 3 seconds:
        caput ('%s:DRV:Acquire'%self.pv, 1) 
        time.sleep(3)
        # Stop and set to trigger externally, do not start acquiring yet
        caput ('%s:DRV:Acquire'%self.pv, 0)
        caput ('%s:DRV:TriggerMode'%self.pv, 3)
        print('Reset Done (TetrAMM), Acquire is off')

    def reset_from_diagnostics_gui(self):
    # Function to reset all the values with the origial values. Calls reset function but adds acquire
    # Arguments: None
    # Returns: None
        # Reset the HDF values and QE1 values, using the preexisting methods:
        # Stop Acquiring
        TetrAMM.put_Acquire(self,0)
        time.sleep(0.5) # Wait
        TetrAMM.reset(self)
        TetrAMM.set_increment_restart(self)
        time.sleep(0.5)
        TetrAMM.put_Acquire(self,1)
        print('Acquisition on (TetrAMM)')

    def update_all_values_from_epics(self):
    # Funciton to update the class values from the epics values
    # Arguments: None
    # Returns: None
        TetrAMM.put_Acquire(self,0) # First, Stop aquiring data

        # G|rab all data needed from the QE1 page
        TetrAMM.values_per_reading = caget ('%s:DRV:ValuesPerRead_RBV'%self.pv) 
        TetrAMM.averaging_time = caget ('%s:DRV:AveragingTime_RBV'%self.pv)
        
        # Grab all data needed from the HDF page
        fp_ascii = caget ('%s:HDF5:FilePath'%self.pv) # file path
        fn_ascii = caget ('%s:HDF5:FileName'%self.pv) # file name
        ff_ascii = caget ('%s:HDF5:FileTemplate'%self.pv) # file format
        
        # Convert ascii to string:        
        self.file_path = TetrAMM.text_ascii_converter(self,fp_ascii,1)
        self.file_name = TetrAMM.text_ascii_converter(self,fn_ascii,1)  
        TetrAMM.file_format = TetrAMM.text_ascii_converter(self, ff_ascii,1)  

        TetrAMM.number_capture = caget ('%s:HDF5:NumCapture'%self.pv) # num captures
        TetrAMM.next_file = caget ('%s:HDF5:FileNumber'%self.pv) # next file

        TetrAMM.put_Acquire(self,1) # Then Start ascquiring again
        print('Done updating class values from EPICS (TetrAMM)')


    def text_ascii_converter(self, content, option):
    # Function to convert text to ascii and vice versa for caput commands into the filepath and other writable regions
    # Arguments: content: the text of ascii array, option: the boolean 0 for text to ascii, or 1 for vice versa, Returns: the converted text/ascii
            if option == 0: # text to ascii conversion
                extracted = [ord(c) for c in content]
            else: # ascii to text conversion 
                extracted = ''.join(chr(c) for c in content)

            return extracted

