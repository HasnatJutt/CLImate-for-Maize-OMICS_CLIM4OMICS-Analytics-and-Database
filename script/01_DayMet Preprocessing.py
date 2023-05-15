# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:36:55 2020

@author: psarzaeim2
"""

## Creating Pivot Tables for G2F Phenotypes Data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd
import numpy as np

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../../../G2F data preprocessing/Meta/output/")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../../../APIs/DayMet/code/")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"
print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
    
# =============================================================================    
# Conversion
# =============================================================================
df = pd.read_csv (Input_dir + "lat_lon.csv")
df = df [["Experiment_ID", "lat", "lon"]]
df ["Experiment_ID"] = df ["Experiment_ID"].astype(str) + ".csv"
convert = {"Experiment_ID": object, "lat": float, "lon": float}
df.dropna (inplace = True)

np.savetxt (Output_dir + "latlon.txt", df.values, fmt = "%s", delimiter = ',')