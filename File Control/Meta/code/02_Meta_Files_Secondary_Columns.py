# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:43:32 2020

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
Output_dir = Output_dir + "/"

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Read the meta files and create the columns names
# =============================================================================        
Defined_col_names = ["Experiment", "lat", "lon", "Year"]

Meta_files = os.listdir (Input_dir) 
#print(Meta_files)
for filename in Meta_files:
    df = pd.read_csv (Input_dir + filename, encoding = "latin1")
    col_name = list (df.columns)
    
    if Defined_col_names [3] not in col_name:
        year = filename [4:8]
        df ["Year"] = year
        
    df = df [["Experiment", "Year", "lat", "lon"]]
    
    df ["State"] = df ["Experiment"].str[:2]
    df ["Experiment_ID"] = df ["Year"] + df ["Experiment"]
    
    df ["Experiment_Type"] = df ["Experiment"].str[2]
    
    df.to_csv (filename, index = None)