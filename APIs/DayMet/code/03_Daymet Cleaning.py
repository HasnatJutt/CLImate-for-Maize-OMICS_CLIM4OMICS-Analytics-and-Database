# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:52:16 2020

@author: psarzaeim2
"""

## Reading and cleanning DayMet data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd
import csv

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../output/Download")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../Clean")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"
print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
    
# =============================================================================
# Reading and fixing each DayMet station file as data frame
# =============================================================================
CSV_files = os.listdir (Input_dir)

for filename in CSV_files:
    Filename = filename [:-4].upper () + ".csv"
    with open (Input_dir + Filename) as in_file:
        with open (Output_dir + Filename, "w", newline = "") as out_file:
            next (in_file)
            next (in_file)
            next (in_file)
            next (in_file)  
            next (in_file)
            next (in_file)
            next (in_file)

            writer = csv.writer (out_file)
            for row in csv.reader (in_file):
                if any (row):
                    writer.writerow (row)

DayMet_files = os.listdir (Output_dir)
for filename in DayMet_files:
    Filename = filename [:-4].upper () + ".csv"
    df = pd.read_csv (Output_dir + Filename) 
    
    df ["Temperature [C]"] = df [["tmin (deg c)", "tmax (deg c)"]].mean (axis = 1)
    df ["Pressure [mb]"] = df["vp (Pa)"]*0.01
       
    df.rename (columns = {"year": "Year [Local]", "yday":"Day of Year [Local]", "srad (W/m^2)":"Solar Radiation [W/m2]", "prcp (mm/day)":"Rainfall [mm]",
                          "swe (kg/m^2)":"Snow Water Equivalent [kg/m2]", "dayl (s)":"Day Light [s]"}, inplace = True)    
    
    df = df [["Day of Year [Local]", "Year [Local]", "Temperature [C]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Pressure [mb]", "Snow Water Equivalent [kg/m2]", "Day Light [s]"]]
    df.index.name = "Record Number"
    
    Year = Filename [:4]
    df = df[df["Year [Local]"] == int(Year)]
    
    df.to_csv (Output_dir + Filename)
    

    