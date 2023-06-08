# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:19:51 2019

@author: psarzaeim2
"""

## Controlling G2F weather data files and the columns contents 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../../../File Upload/Environment/")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../../File Control/Environment/output")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
        
# =============================================================================
# Read the weather files and create the columns
# =============================================================================    
Defined_col_names = ["Record Number", "Station ID", "Experiment", "Day [Local]", "Month [Local]", "Year [Local]", "Day of Year [Local]", "Time [Local]",
                     "Temperature [C]", "Dew Point [C]", "Relative Humidity [%]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Wind Speed [m/s]",
                     "Wind Direction [degrees]", "Wind Gust [m/s]"]

Weather_files = os.listdir (Input_dir) 
#print(Weather_files)
for filename in Weather_files:
    df = pd.read_csv (Input_dir + filename)
    df ["Record Number"] = df.index + 1
    col_name = list (df.columns)
#    print(col_name) 

    if Defined_col_names [6] not in col_name:
        df ["Date"] = df ["Year [Local]"].apply (str) + "/" + df ["Month [Local]"].apply(str) + "/" + df ["Day [Local]"].apply(str)
        df ["Date"] = pd.to_datetime (df ["Date"], errors = "coerce")
        df ["Day of Year [Local]"] = df ["Date"].dt.dayofyear
    
    df = df [["Record Number", "Station ID", "Experiment", "Day [Local]", "Month [Local]", "Year [Local]", "Day of Year [Local]", "Time [Local]",
                     "Temperature [C]", "Dew Point [C]", "Relative Humidity [%]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Wind Speed [m/s]",
                     "Wind Direction [degrees]", "Wind Gust [m/s]"]]
    
    df.to_csv (filename, index = None)