# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:08:48 2020

@author: psarzaeim2
"""

## Reading and cleanning DayMet data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../output/Clean")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../DayMet")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"
print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Reading each experiment file as data frame
# =============================================================================
for filename in os.listdir (Input_dir):
#    print (Output_dir + filename)
    df = pd.read_csv (Input_dir + filename, index_col = "Record Number")
    
# =============================================================================
# Pivot tables
# =============================================================================    
    Variables = ["Temperature [C]", "Solar Radiation [W/m2]", "Pressure [mb]"]
    
    for var in Variables:
        df_ave = df.pivot_table (var, index = ["Day of Year [Local]"], dropna = False) 
        df_ave ["Min " + var] = df.pivot_table (var, index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)
        df_ave ["Max " + var] = df.pivot_table (var, index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
        
        df_ave.to_csv (Output_dir + var[0] + filename)
    
# =============================================================================            
    "Rainfall pivot table"
    Rainfall_G = df.groupby ("Day of Year [Local]")["Rainfall [mm]"].sum(min_count = 1)
    Rainfall = Rainfall_G.to_frame ()
    Rainfall ["Min Rainfall [mm]"] = df.pivot_table ("Rainfall [mm]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)
    Rainfall ["Max Rainfall [mm]"] = df.pivot_table ("Rainfall [mm]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
    
    Rainfall.to_csv (Output_dir + "R" + filename)
    
# =============================================================================        
    "Snow Water Equivalent pivot table"
    Snow_Water_Equivalent = df.pivot_table ("Snow Water Equivalent [kg/m2]", index = ["Day of Year [Local]"], dropna = False)
    Snow_Water_Equivalent ["Min Snow Water Equivalent [kg/m2]"] = df.pivot_table ("Snow Water Equivalent [kg/m2]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)  
    Snow_Water_Equivalent ["Max Snow Water Equivalent [kg/m2]"] = df.pivot_table ("Snow Water Equivalent [kg/m2]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
    
    Snow_Water_Equivalent.to_csv (Output_dir + "E" + filename)

# =============================================================================        
    "Day Light pivot table"
    Day_Light = df.pivot_table ("Day Light [s]", index = ["Day of Year [Local]"], dropna = False)
    Day_Light ["Min Day Light [s]"] = df.pivot_table ("Day Light [s]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)  
    Day_Light ["Max Day Light [s]"] = df.pivot_table ("Day Light [s]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
    
    Day_Light.to_csv (Output_dir + "L" + filename)
    
# =============================================================================  
