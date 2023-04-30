# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:56 2020

@author: psarzaeim2, Hasnat

Updated on Wed Apr 26 2023 
"""

## Controlling G2F weather data files and the columns contents 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
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
if os.path.exists("../File Upload/Environment"):
    Input_dir = "../File Upload/Environment"     
    Output_dir = "../File Control/Environment/output"
elif os.path.exists("File Upload/Environment"):
    Input_dir = "File Upload/Environment"     
    Output_dir = "File Control/Environment/output"
elif os.path.exists("../../../File Upload/Environment"):
    Input_dir = "../../../File Upload/Environment"
    Output_dir = "../../../File Control/Environment/output"  
elif len(sys.argv)==2 and re.match(r'[\w$\\/._-\s]', sys.argv[1]):
    Input_dir = sys.argv[1]
    Output_dir = sys.argv[1]
else:
    print("No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Check the false value
# =============================================================================  
Weather_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv'))) 

for filename in Weather_files:
    try:
        df = pd.read_csv (filename, low_memory=False)
    except:
        with open(filename, "r") as rawdata:
            encoding_name=rawdata.encoding
        df = pd.read_csv (filename, encoding=encoding_name, low_memory=False)
    col_name = df.columns.tolist()
    try:
        df ["Relative Humidity [%]"] = pd.to_numeric(df ["Relative Humidity [%]"], downcast='float', errors='coerce')
        df ["Solar Radiation [W/m2]"] = pd.to_numeric(df ["Solar Radiation [W/m2]"], downcast='float', errors='coerce')
        df ["Rainfall [mm]"] = pd.to_numeric(df ["Rainfall [mm]"], downcast='float', errors='coerce')
        df ["Wind Direction [degrees]"] = pd.to_numeric(df ["Wind Direction [degrees]"], downcast='float', errors='coerce')
        df.loc [(df ["Relative Humidity [%]"] < 0 ) | (df ["Relative Humidity [%]"] > 100), "Relative Humidity [%]"] = " "
        df.loc [(df ["Solar Radiation [W/m2]"] < 0 ) , "Solar Radiation [W/m2]"] = " "
        df.loc [(df ["Rainfall [mm]"] < 0 ) , "Rainfall [mm]"] = " "
        df.loc [(df ["Wind Direction [degrees]"] < 0 ) | (df ["Wind Direction [degrees]"] > 360), "Wind Direction [degrees]"] = " "
        # df.loc [(df ["Wind Speed [m/s]"] == 0) & (df ["Wind Direction [degrees]"].isnull ()), "Wind Direction [degrees]"] = " "
        df.to_csv (os.path.abspath(os.path.join(Output_dir, os.path.basename(filename))), index = None)
    except Exception as E:
        print(f"The following file {os.path.basename(filename)} is not processed due to exception {E}")