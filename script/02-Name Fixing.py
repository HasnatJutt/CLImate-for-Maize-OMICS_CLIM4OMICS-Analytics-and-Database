# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:57:02 2019

@author: psarzaeim2
"""

## Separating Names
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
from shutil import copyfile

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../output/Weather Data Reading")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../Name Fixing")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"
print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Separating the names of experiments with more than 1 name in their files names (the experiments in the same location)
# ============================================================================= 
G2F_files = os.listdir(Input_dir) 
#print(G2F_files)  

for filename in G2F_files:
    Year = filename [0:4]
    Filename = filename [4:]
    Experiment = Filename.split ()
#    print(Experiment)
    for name in Experiment:
        if ".csv" not in name:
            src = Input_dir + filename
            des = Output_dir + str (Year) + name  + ".csv"
            copyfile (src, des)

        else:
            src = Input_dir + filename
            des = Output_dir + str (Year) + name 
            copyfile (src, des)