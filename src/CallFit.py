import sys
import os
import numpy as np
#sys.path.append(os.path.realpath(
#   os.path.join(os.path.dirname(__file__), '..')))

PATHadd='/home/dqi23796/VirtPython/fit_lib'
sys.path.insert(0,PATHadd)

import fit_lib

def Fitting(array, dem): # 2d array and dem is 2
    if dem ==2:
        fit, error= fit_lib.doFit2dGaussian(array,maxiter = 60)
        [sigmay, sigmax, rotation] = fit_lib.convert_abc(fit[4], fit[5], fit[6])
        fit = [fit[0],fit[1],fit[3],fit[2],sigmax,sigmay,rotation]
    return fit, error



