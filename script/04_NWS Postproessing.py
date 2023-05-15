# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 16:56:13 2019

@author: psarzaeim2
"""

## Creating pivot tables from NWS data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../output/Near")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../NWS")
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
    
    Variables = ["Temperature [C]", "Dew Point [C]", "Wind Speed [m/s]", "Pressure [mb]"]
    
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
    "Rainfall pivot table"
    Rainfall_G = df.groupby ("Day of Year [Local]")["Rainfall [mm]"].sum(min_count = 1)
    Rainfall = Rainfall_G.to_frame ()
    Rainfall ["Min Rainfall [mm]"] = df.pivot_table ("Rainfall [mm]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)
    Rainfall ["Max Rainfall [mm]"] = df.pivot_table ("Rainfall [mm]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
    
    Rainfall.to_csv (Output_dir + "R" + filename)
    