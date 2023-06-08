# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 08:46:38 2019

@author: psarzaeim2
"""

# Reading G2F Metadata Files  
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../../../File Control/Meta/output/")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../../../G2F data preprocessing/Meta/output/")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Concatenating the meta files
# =============================================================================
Meta_files = os.listdir (Input_dir)
os.chdir (Input_dir)
lat_lon_file = pd.concat ([pd.read_csv (f) for f in Meta_files])
os.chdir (Output_dir)
lat_lon_file = lat_lon_file [lat_lon_file.Experiment_Type == "H"]
lat_lon_file.to_csv ("All_lat_lon.csv", index = False, encoding = 'utf-8-sig')

lat_lon_file.dropna (subset = ["lat", "lon"], inplace = True)
lat_lon_file.to_csv ("0lat_lon.csv", index = False, encoding = 'utf-8-sig')