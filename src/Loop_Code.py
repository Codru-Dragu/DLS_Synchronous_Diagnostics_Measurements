''' LOOP CODE TO RUN IN PARALLEL WITH THE TRIGGER '''

# IMPORTS #
import cothread
from cothread.catools import *
import h5py
import time
from datetime import datetime
import re

import TetrAMM as T
import MantaCam as MC

import sys
import shelve

# Variables

tet_array = [] # Array of tet
cam_array = [] # Array of cam NOTE: if you have another obj, add a new array tupe
beamline_topup = ' '
gate_signal = 0
normal_fps = [int]
camera_exists = False # check to see if there is a camera
timeout_time = 0


def set_up(t_arr, c_arr, b_topup):
# Function to set up Globals
# Arguments: t_arr (array of tetramm objects), c_arr (array of camera objects), b_toupup (beamline topup pv string), gate_time (the gate time length that is required)
# Returns: None    
    # Call Globals
    global tet_array
    global cam_array
    global beamline_topup
    global camera_exists

    # Set Globals
    tet_array = t_arr
    cam_array = c_arr
    beamline_topup = b_topup

def set_up_gate_timeout(timeout,gate):
# Function to set up gate and timeout globals
# Arguments: timeout (the timeout length of time that is required), gate (the gate time length that is required)
# Returns: None    
    # Call Globals
    global timeout_time
    global gate_signal
    global tet_array
    global cam_array

    # Set Globals
    timeout_time = int(timeout)
    gate_signal = int(gate)

    # If there are tetramms
    if tet_array:
        for tet_obj in tet_array:
            tet_obj.timeout = timeout_time
    
    # If there are cameras
    if cam_array:
        for cam_obj in cam_array:
            cam_obj.timeout = timeout_time

def set_camera_fps_range():
# Function to Set the Camera fps and set camera = true marker
# Arguments: None
# Returns: None    
    # Call Gloabls
    global cam_array
    global normal_fps
    global camera_exists

    # If there are cameras, get the frame rates of the cameras
    # use the fps value of the ith position object.
    if cam_array: 
        camera_exists = True # set as true that a camera exists
        for i in range(0,len(cam_array)):
            normal_fps[i] = int(cam_array[i].get_fps())     

def set_hdf_toggles():
# Fucntion to start the HDF toggles
# Arguments: None
# Returns: None
    if tet_array:
        for i in range(0,len(tet_array)):
            tet_array[i].put_HDF_start(1)

    if cam_array:
        for i in range(0,len(cam_array)):
            cam_array[i].put_HDF_start(1)


def main_loop():
# Function that will be called per loop
# Arguments: None
# Returns: Live Gui Update Messages

# Make a variable to store messages

    error_store = [] # Store error messages
    files_store_camera = [] # Store messages from dropped files
    files_store_tetramm = [] # Store messages from dropped files
    increm_store = [] # Store increment files for current file box

    # Boolean to specify whether the file should be saved or not in the event of topup
    topup_file_to_save = 1 # Default, the file should be saved :)
    # Check if the hdf is stopped:
    boolean_stopped = [] # list of boolean values to indicate whether hdf acquisition is stopped or not
    # Loop through available hardware and checkS
    for i in range(0,len(tet_array)):
        boolean_stopped.append(tet_array[i].get_HDF_start() == 0)
        # Also format files store slots
        files_store_tetramm.insert(i,[])
    
    for i in range(0,len(cam_array)):
        boolean_stopped.append(cam_array[i].get_HDF_start() == 0)
        # Also format files store slots
        files_store_camera.insert(i,[])

    if(all(boolean_stopped)): # if all the devices have their hdf off, then they are done acquiring
        
        # Should have fininshed taking data
        time.sleep(1) # wait 1 seconds

        # CHECK IF TOPUP HAPPENED BEFORE SAVING 
        topup_check = caget(beamline_topup) 

        if((topup_check > (600-gate_signal-33)) or (topup_check < 1)): # topup approx 30 seconds, 
        # if this is true, topup has happened during the acquisition of data or topup is happening now at the end of the data. 
        # Regardless, that means this data is corrupted and should not be taken. Wait and move on without saving  
            time.sleep(0.5)
            # Get the timestamp:
            dateTimeObj = datetime.now()
            error_time = '%(a)s:%(b)s:%(c)s'%{ 'a': dateTimeObj.time().hour, 'b': dateTimeObj.time().minute, 'c': dateTimeObj.time().second}
            error_store.append(' %s : No files saved due to topup'%error_time)
            topup_file_to_save = 0 # do not save any file

        # CHECK THE DROPPED FRAMES if a camera exists only, and only if it is worth saving the file
        dropped_frames = []
        if ((topup_file_to_save == 1) and (camera_exists == True)):
            for cam_obj in cam_array:
                dropped_frames.append((cam_obj.get_dropped() > 1))
        # Now check for frames- if there are cameras, and if any of them have dropped frames more than 1, BUT ONLY IF THE FILE IS WORTH SAVING
        if ((topup_file_to_save == 1) and (camera_exists == True) and (True in dropped_frames)): # Evaluates the LHS expression first, so if the camera does not exist it will not call True in dropped frames and result in an error
            print('Error: Dropped Frames')
            dateTimeObj = datetime.now()
            error_time = '%(a)s:%(b)s:%(c)s'%{ 'a': dateTimeObj.time().hour, 'b': dateTimeObj.time().minute, 'c': dateTimeObj.time().second}
            error_store.append(' %s : No Files saved due to dropped frames camera'%error_time)
            topup_file_to_save = 0 # use the same marker but indicate that the file should not be saved
            # For each value in the list, check if it did drop frames (true) or it didnt (false), and if it did, reset it
            for i in range(0,len(dropped_frames)):
                if(dropped_frames[i] == True): # frames were dropped
                    cam_array[i].put_Acquire(0) # Stop Acquiring
                    cam_array[i].reset() # Reset the camera (note: this automatically will reset the dropped frames to 0)
                    print('Resetting Camera Due to Dropped Frames')
                    time.sleep(1.5)
                    cam_array[i].put_Acquire(1) # Start acquiring again
                    time.sleep(1)
                    # Get the file number that was not saved and increment in in the appropriate place
                    file_affected = int(cam_array[i].get_current_increment())
                    padded_zeroes = "%04d"%file_affected
                    files_store_camera[i] = ['File %s Error, will be overwritten...'%padded_zeroes]

            print('Waiting for next trigger signal...')
            # Next, wait for the end of the trigger break. You can use only the first camera as an fps monitor, as the other will mimic the behaviour
            while (cam_array[0].get_fps() < 4):
                time.sleep(0.5)
                pass
            print('Waiting for next trigger signal to finish...')
            # Now, the trigger break should have ended
            # Wait during the trigger
            while (cam_array[0].get_fps() > 3):
                time.sleep(0.5)
                pass

        if(topup_file_to_save == 1): # if the file is worth saving
            # Write the data, but make note of whether it was written successfully or not.
            response_status = {} # empty response status dict
            
            if cam_array:
                for i in range(0,len(cam_array)):
                    camera_success = cam_array[i].put_WriteFile(1)
                    time.sleep(1)
                    response_status['cam_array[%s]'%i] = camera_success

            if tet_array:
                for i in range(0,len(tet_array)):
                    tetramm_success = tet_array[i].put_WriteFile(1)
                    time.sleep(1)
                    response_status['tet_array[%s]'%i] = tetramm_success

            # Check if there was a problem  - if there are any falses recorded
            if (False in response_status.values()):
                print('Error: Problem with savving files')
                # First stop all devices from acquiring data
                if cam_array:
                    for i in range(0,len(cam_array)):
                        cam_array[i].put_Acquire(0)

                if tet_array:
                    for i in range(0,len(tet_array)):
                        tet_array[i].put_Acquire(0)

                # Next reset the hardware that didnt work, and for the ones that DID work, de-incrememnt by 1 to override the files
                for key in response_status.keys():
                    if (response_status[key] == False):
                        print('Restting %s'%key)
                        exec('%s.reset()'%key) # execute the reset function
                        print('Done reset')
                        # Get the message values required
                        name_of_hw = exec('%s.return_name()'%key)
                        dateTimeObj = datetime.now()
                        error_time = '%(a)s:%(b)s:%(c)s'%{ 'a': dateTimeObj.time().hour, 'b': dateTimeObj.time().minute, 'c': dateTimeObj.time().second}
                        file_affected = int(exec('%s.get_current_increment()'%key))
                        padded_zeroes = "%04d"%file_affected
                        # Save the messages
                        error_store.append('%(a)s : Error with saving file number %(b)s for %(c)s'%{'a': error_time, 'b': padded_zeroes, 'c': name_of_hw})
                        # save in the respective array stores
                        if 'tet_' in key: # if it is a tetramm type object, 
                            tetnum = re.search(r"\[([A-Za-z0-9_]+)\]", key) # search for the index number of that tetramm
                            tetnum_int = int(tetnum.group(1))
                            files_store_tetramm[tetnum_int] =['File %s Error, will be overwritten...'%padded_zeroes]
                        elif 'cam_' in key: # if it is a camera type object, 
                            camnum = re.search(r"\[([A-Za-z0-9_]+)\]", key) # search for the index number of that tetramm
                            camnum_int = int(camnum.group(1))
                            files_store_camera[camnum_int] = ['File %s Error, will be overwritten...'%padded_zeroes]                      
                    else: # else if the response status key is true,reduce the increment by 1 to overwrite the unpaired file for the other hardwraes
                        exec('%s.set_increment_minus()'%key)
                        time.sleep(0.5)
                        increm_store = [key.get_current_increment()]

                # Now set all hardware acquiring data again
                if cam_array:
                    for i in range(0,len(cam_array)):
                        cam_array[i].put_Acquire(1)

                if tet_array:
                    for i in range(0,len(tet_array)):
                        tet_array[i].put_Acquire(1)                    


                # Next, wait for next trigger cycle break. 
                # There is no way of knowing when the next trigger cycle is, 
                # So a way we can check is to see whether either the camera fps has changed (if there is a camera)
                # or to look at a changing tetramm value

                if cam_array: # if the camera exists, do this
                    print('Wait for next trigger signal...')
                # First wait until the next trigger session (can use the 0th position camera)
                    while (cam_array[0].get_fps() < 4):
                        time.sleep(0.2)
                        pass
                    print('Wait for trigger session to pass...')
                    # Now, the break should have ended
                    # Wait duing the trigger
                    while (cam_array[0].get_fps() > 3):
                        time.sleep(0.2)
                        pass

                # Exit the if statement once trigger is done

                else: # if there is no cam array use the tetrAMM
                    # First wait until the next trigger session (can use the 0th position camera)
                    while (tet_array[0].return_trigger_check() == 0.0):
                        time.sleep(0.2)
                        pass
                    # Now, the break should have ended
                    # Wait duing the trigger
                    while (tet_array[0].return_trigger_check() != 0.0):
                        time.sleep(0.2)
                        pass     

                # Exit the if statement once trigger is done
            else: # If all has saved correctly
                if tet_array:
                    increm_store = [tet_array[0].get_current_increment()]
                    
                elif cam_array:
                    increm_store = [cam_array[0].get_current_increment()]

        time.sleep(1)
        
        # Now start all the devices acquisitions:
        print('Start the HDF acquiring again')
        for tet_obj in tet_array:
            tet_obj.put_HDF_start(1)
            time.sleep(1.5)

    
        for cam_obj in cam_array:
            cam_obj.put_HDF_start(1)
            time.sleep(1.5)

    return error_store, files_store_tetramm, files_store_camera, increm_store # return the error messages
