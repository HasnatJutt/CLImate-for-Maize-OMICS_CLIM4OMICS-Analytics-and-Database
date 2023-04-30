# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:21:04 2019

@author: psarzaeim2

Updated on Wed Sep 21 2022 
@by: Hasnat
"""

## Controlling G2F weather data files and the columns names 
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
# print ("Output directory = ", Output_dir)

# =============================================================================
# Read the weather files and check the columns names
# =============================================================================        
Defined_col_names = ["Station ID", "Experiment", "Day [Local]", "Month [Local]", "Year [Local]", "Time [Local]",
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

    if Defined_col_names [0] not in col_name:
        print ("'Station ID' column is unrecognized in {}, please find the station ID values column and rename it to 'Statio ID'".format (filename))
   
    if Defined_col_names [1] not in col_name:
        print ("'Experiment' column is unrecognized in {}, please find the experiment ID column and rename it to 'Experiment'".format (filename)) 
    
    if Defined_col_names [2] not in col_name:
        print ("'Day [Local]' column is unrecognized in {}, please find the day values column and rename it to 'Day [Local]'".format (filename)) 
    
    if Defined_col_names [3] not in col_name:
        print ("'Month [Local]' column is unrecognized in {}, please find the month values column and rename it to 'Month [Local]'".format (filename))
      
    if Defined_col_names [4] not in col_name:
        print ("'Year [Local]' column is unrecognized in {}, please find the year values column and rename it to 'Year [Local]'".format (filename))
           
    if Defined_col_names [5] not in col_name:
        print ("'Time [Local]' column is unrecognized in {}, please find the time values column and rename it to 'Time [Local]'".format (filename))
    
    if Defined_col_names [6] not in col_name:
        print ("'Temperture [C]' column is unrecognized in {}, please find the temperature values column and rename it to 'Temperature [C]'".format (filename))
        
    if Defined_col_names [7] not in col_name:
        print ("'Dew Point [C]' column is unrecognized in {}, please find the dew point values column and rename it to 'Dew Point [C]'".format (filename))
        
    if Defined_col_names [8] not in col_name:
        print ("'Relative Humidity [%]' column is unrecognized in {}, please find the relative humidity values column and rename it to 'Relative Humidity [%]'".format (filename))
        
    if Defined_col_names [9] not in col_name:
        print ("'Solar Radiation [W/m2]' column is unrecognized in {}, please find the solar radiation values column and rename it to 'Solar Radiation [W/m2]'".format (filename))
        
    if Defined_col_names [10] not in col_name:
        print ("'Rainfall [mm]' column is unrecognized in {}, please find the rainfall values column and rename it to 'Rainfall [mm]'".format (filename))
        
    if Defined_col_names [11] not in col_name:
        print ("'Wind Speed [m/s]' column is unrecognized in {}, please find the wind speed values column and rename it to 'Wind Speed [m/s]'".format (filename))
 
    if Defined_col_names [12] not in col_name:
        print ("'Wind Direction [degrees]' column is unrecognized in {}, please find the wind direction values column and rename it to 'Wind Direction [degrees]'".format (filename))
        
    if Defined_col_names [13] not in col_name:
        print ("'Wind Gust [m/s]' column is unrecognized in {}, please find the wind gust values column and rename it to 'Wind Gust [m/s]'".format (filename))      
