# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:51:40 2019

@author: psarzaeim2
"""

## Controlling G2F meta data files and the columns names 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../../../File Upload/Meta/")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../../File Control/Meta/output")
Output_dir = os.getcwd ().replace ("\\", "/")

print ("Input directory = ", Input_dir)
# print ("Output directory = ", Output_dir)
    
# =============================================================================
# Read the meta files and check the columns names
# =============================================================================        
Defined_col_names = ["Experiment", "lat", "lon"]

Meta_files = os.listdir (Input_dir) 
#print(Meta_files)
for filename in Meta_files:
    df = pd.read_csv (filename, encoding = "latin1")
    col_name = list (df.columns)
        
    if Defined_col_names [0] not in col_name:
        print ("'Experiment' column is unrecognized in {}, please find the experiment ID column and rename it to 'Experiment'".format (filename))
        
    if Defined_col_names [1] not in col_name:
        print ("'lat' column is unrecognized in {}, please find the latitude column and rename it to 'lat'".format (filename))
        
    if Defined_col_names [2] not in col_name:
        print ("'lon' column is unrecognized in {}, please find the longitude column and rename it to 'lon'".format (filename))
