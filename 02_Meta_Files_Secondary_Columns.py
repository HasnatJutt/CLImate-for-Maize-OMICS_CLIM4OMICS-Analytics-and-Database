# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:43:32 2020

@author: psarzaeim2, Hasnat

Updated on Wed Apr 26 2023
"""

## Controlling G2F meta data files and the columns names 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
if os.path.exists("../../../File Upload/Meta"):
    Input_dir = "../../../File Upload/Meta"
    if os.path.exists("../../../File Control/Meta/output"):
        Output_dir = "../../../File Control/Meta/output"
    else:
        os.makedirs("../../../File Control/Meta/output")
        Output_dir = "../../../File Control/Meta/output"   
elif os.path.exists("File Upload/Meta"):
    Input_dir = "File Upload/Meta"     
    if os.path.exists("File Control/Meta/output"):
        Output_dir = "File Control/Meta/output"
    elif len(sys.argv)==2 and re.match(r'[\w$\\/._-\s]', sys.argv[1]):
        Output_dir = sys.argv[1]
    else:
        os.makedirs("File Control/Meta/output")
        Output_dir = "File Control/Meta/output"
elif os.path.exists("../File Upload/Meta"):
    Input_dir = "../File Upload/Meta"     
    if os.path.exists("../File Control/Meta/output"):
        Output_dir = "../File Control/Meta/output"
    elif len(sys.argv)==2 and re.match(r'[\w$\\/._-\s]', sys.argv[1]):
        Output_dir = sys.argv[1]
    else:
        os.makedirs("../File Control/Meta/output")
        Output_dir = "../File Control/Meta/output"
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
# Read the meta files and create the columns names
# =============================================================================        
Defined_col_names = ["Experiment", "lat", "lon", "Year"]

Meta_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
#print(Meta_files)
for filename in Meta_files:
    try:
        df = pd.read_csv (filename, low_memory=False)
    except:
        with open(filename, "r") as rawdata:
            encoding_name=rawdata.encoding
        df = pd.read_csv (filename, encoding=encoding_name, low_memory=False)
    col_name = df.columns.tolist()
    
    if Defined_col_names [3] not in col_name:
        year = filename [4:8]
        df ["Year"] = year
    try:   
        df = df [["Experiment", "Year", "lat", "lon"]]
        df ["State"] = df ["Experiment"].str[:2]
        df ["Experiment_ID"] = df ["Year"] + df ["Experiment"]
        df ["Experiment_Type"] = df ["Experiment"].str[2]
        df.to_csv (os.path.abspath(os.path.join(Output_dir, os.path.basename(filename))), index = None)
    except Exception as E:
        print(f"The following file {os.path.basename(filename)} is not processed due to exception {E}")