# IMPORTS #
import Process_Data_MantaCam as mc
import Process_Data_TetrAMM as tt
import Fourier_Analysis as fa
import scipy.io as sio

# VARIABLES #

# FUNCTIONS #


def makefiles(hardware_t, hardware_c, pathtosave, totalfiles, incrementor):
# Arguments: totalfiles (the total number of files), hardware_t (array of tetramm hardware objects), hardware_c (array of camera hardware_objects), pathtosave (path string to save the mat files)

  x = "%04d"%incrementor # configure the number option

  for ht in range(0,len(hardware_t[0])): # For each tetramm hardware object:
    # Get the required data to input to the overnight file creator
    tet_name = hardware_t[2][ht]
    tet_fp = hardware_t[1][ht]

    # Create overnight file
    tt.overnight_file_creator(tet_name, tet_fp, pathtosave, x)

  print(' Done TetrAMMs f%s'%x)

  for hc in range(0,len(hardware_c[0])): # For each camera hardware object:
    # Get the required data to input to the overnight file creator
    cam_name = hardware_c[2][hc]
    cam_fp = hardware_c[1][hc]
    cam_fps = hardware_c[3][hc]
    cam_bin_x = hardware_c[4][hc]

    # Create overnight file
    mc.overnight_file_creator(cam_name, cam_bin_x, cam_fp, cam_fps, pathtosave, x)
  
  print(' Done Cameras f%s'%x)



def makexfile(hardware_t,hardware_c,pathtosave,totalfiles):
  # Now save the x-axis files

  # Create empty dict
  x_savedict = {}
  x = "%04d"%(totalfiles-1) # the last file

  # Tetramm
  for ht in range(0,len(hardware_t[0])): # For each tetramm hardware object:
    # Get the required data to input to the overnight file creator
    tet_name = hardware_t[2][ht]
    tet_fp = hardware_t[1][ht]

    # Create overnight file but this time store the returnd x-acis values
    tx = tt.overnight_file_creator(tet_name, tet_fp, pathtosave, x)
    x_savedict[tet_name] = tx

  print(' Done TetrAMMs f%s'%x)

  # Camera
  for hc in range(0,len(hardware_c[0])): # For each camera hardware object:
    # Get the required data to input to the overnight file creator
    cam_name = hardware_c[2][hc]
    cam_fp = hardware_c[1][hc]
    cam_fps = hardware_c[3][hc]
    cam_bin_x = hardware_c[4][hc]

    # Create overnight file but this time store the returnd x-acis values
    cx = mc.overnight_file_creator(cam_name, cam_bin_x, cam_fp, cam_fps, pathtosave, x)
    x_savedict[cam_name] = cx
    
  print(' Done Cameras f%s'%x) 

  # Save the dict file in the same place as the others
  sio.savemat('%s/XAxis.mat'%pathtosave, x_savedict)

  print('Done XDict')



  



