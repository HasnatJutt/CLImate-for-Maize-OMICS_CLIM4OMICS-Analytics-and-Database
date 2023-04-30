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
if os.path.exists("../../../File Upload/Environment"):
    Input_dir = "../../../File Upload/Environment"
    if os.path.exists("../../../File Control/Environment/output"):
        Output_dir = "../../../File Control/Environment/output"
    else:
        os.makedirs("../../../File Control/Environment/output")
        Output_dir = "../../../File Control/Environment/output"   
elif os.path.exists("File Upload/Environment"):
    Input_dir = "File Upload/Environment"     
    if os.path.exists("File Control/Environment/output"):
        Output_dir = "File Control/Environment/output"
    elif len(sys.argv)==2 and re.match(r'[\w$\\/._-\s]', sys.argv[1]):
        Output_dir = sys.argv[1]
    else:
        os.makedirs("File Control/Environment/output")
        Output_dir = "File Control/Environment/output"
elif os.path.exists("../File Upload/Environment"):
    Input_dir = "../File Upload/Environment"     
    if os.path.exists("../File Control/Environment/output"):
        Output_dir = "../File Control/Environment/output"
    elif len(sys.argv)==2 and re.match(r'[\w$\\/._-\s]', sys.argv[1]):
        Output_dir = sys.argv[1]
    else:
        os.makedirs("../File Control/Environment/output")
        Output_dir = "../File Control/Environment/output"
elif len(sys.argv)==3 and re.match(r'[\w$\\/._-\s]', sys.argv[1]):
    Input_dir = sys.argv[1]
    if os.path.exists(sys.argv[2]):
        Output_dir = sys.argv[2]
    else:
        os.makedirs(sys.argv[2])
        Output_dir = sys.argv[2]
else:
    print("No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
        
# =============================================================================
# Read the weather files and create the columns
# =============================================================================    
Defined_col_names = ["Record Number", "Station ID", "Experiment", "Day [Local]", "Month [Local]", "Year [Local]", "Day of Year [Local]", "Time [Local]",
                     "Temperature [C]", "Dew Point [C]", "Relative Humidity [%]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Wind Speed [m/s]",
                     "Wind Direction [degrees]", "Wind Gust [m/s]"]

Weather_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
#print(Weather_files)
for filename in Weather_files:
    try:
        df = pd.read_csv (filename, low_memory=False)
    except:
        with open(filename, "r") as rawdata:
            encoding_name=rawdata.encoding
        df = pd.read_csv (filename, encoding=encoding_name, low_memory=False)
    col_name = df.columns.tolist()
    try:
        if Defined_col_names [6] not in col_name:
            df ["Date"] = df ["Year [Local]"].apply (str) + "/" + df ["Month [Local]"].apply(str) + "/" + df ["Day [Local]"].apply(str)
            df ["Date"] = pd.to_datetime (df ["Date"], errors = "coerce")
            df ["Day of Year [Local]"] = df ["Date"].dt.dayofyear
        df = df [["Record Number", "Station ID", "Experiment", "Day [Local]", "Month [Local]", "Year [Local]", "Day of Year [Local]", "Time [Local]",
                     "Temperature [C]", "Dew Point [C]", "Relative Humidity [%]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Wind Speed [m/s]",
                     "Wind Direction [degrees]", "Wind Gust [m/s]"]]
        df.to_csv (os.path.abspath(os.path.join(Output_dir, os.path.basename(filename))), index = None)
    except Exception as E:
        print(f"The following file {os.path.basename(filename)} is not processed due to exception {E}")