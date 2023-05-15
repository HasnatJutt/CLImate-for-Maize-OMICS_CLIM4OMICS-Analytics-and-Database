# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:56 2020

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
path = os.chdir ("../output")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../output")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Check the false value
# =============================================================================  
Weather_files = os.listdir (Input_dir) 

for filename in Weather_files:
    df = pd.read_csv (Input_dir + filename)
    
    df.loc [(df ["Relative Humidity [%]"] < 0 ) | (df ["Relative Humidity [%]"] > 100), "Relative Humidity [%]"] = " "
    df.loc [(df ["Solar Radiation [W/m2]"] < 0 ) , "Solar Radiation [W/m2]"] = " "
    df.loc [(df ["Rainfall [mm]"] < 0 ) , "Rainfall [mm]"] = " "
    df.loc [(df ["Wind Direction [degrees]"] < 0 ) | (df ["Wind Direction [degrees]"] > 360), "Wind Direction [degrees]"] = " "
    # df.loc [(df ["Wind Speed [m/s]"] == 0) & (df ["Wind Direction [degrees]"].isnull ()), "Wind Direction [degrees]"] = " "

    df.to_csv (filename, index = None)