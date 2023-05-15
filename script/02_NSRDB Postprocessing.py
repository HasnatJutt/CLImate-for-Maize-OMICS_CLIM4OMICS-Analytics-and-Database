# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:36:32 2020

@author: psarzaeim2
"""

## Creating pivot tables from NSRDB data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../output/Download")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../NSRDB")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"
print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
    
# =============================================================================
# Pivot tables
# =============================================================================    
for filename in os.listdir (Input_dir):
#    print (Output_dir + filename)
    df = pd.read_csv (Input_dir + filename, index_col = "Record Number")
    
    Variables = ["Temperature [C]", "Dew Point [C]", "Solar Radiation [W/m2]", "Wind Speed [m/s]", "Pressure [mb]"]
    
    for var in Variables:
        df_ave = df.pivot_table (var, index = ["Day of Year [Local]"], dropna = False) 
        df_ave ["Min " + var] = df.pivot_table (var, index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)
        df_ave ["Max " + var] = df.pivot_table (var, index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
        
        df_ave.to_csv (Output_dir + var[0] + filename)
    
# =============================================================================        
    "Relative Humidity pivot table"
    Relative_Humidity = df.pivot_table ("Relative Humidity [%]", index = ["Day of Year [Local]"], dropna = False)
    Relative_Humidity ["Min Relative Humidity [%]"] = df.pivot_table ("Relative Humidity [%]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)  
    Relative_Humidity ["Max Relative Humidity [%]"] = df.pivot_table ("Relative Humidity [%]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
    
    Relative_Humidity.to_csv (Output_dir + "H" + filename)
    
# =============================================================================        
    "Wind Direction pivot table"
    Wind_Direction = df.pivot_table ("Wind Direction [degrees]", index = ["Day of Year [Local]"], dropna = False)
    Wind_Direction ["Min Wind Direction [degrees]"] = df.pivot_table ("Wind Direction [degrees]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)  
    Wind_Direction ["Max Wind Direction [degrees]"] = df.pivot_table ("Wind Direction [degrees]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
    
    Wind_Direction.to_csv (Output_dir + "I" + filename)

# =============================================================================       
    "Precipitable Water pivot table"
    Precipitable_Water = df.pivot_table ("Precipitable Water [mm]", index = ["Day of Year [Local]"], dropna = False)
    Precipitable_Water ["Min Precipitable Water [mm]"] = df.pivot_table ("Precipitable Water [mm]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)  
    Precipitable_Water ["Max Precipitable Water [mm]"] = df.pivot_table ("Precipitable Water [mm]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
    
    Precipitable_Water.to_csv (Output_dir + "C" + filename)