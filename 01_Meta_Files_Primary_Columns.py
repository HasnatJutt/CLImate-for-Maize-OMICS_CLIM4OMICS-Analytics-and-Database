# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:51:40 2019

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
# print ("Output directory = ", Output_dir)
    
# =============================================================================
# Read the meta files and check the columns names
# =============================================================================        
Defined_col_names = ["Experiment", "lat", "lon"]

Meta_files =  glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))

for filename in Meta_files:
    try:
        df = pd.read_csv (filename, low_memory=False)
    except:
        with open(filename, "r") as rawdata:
            encoding_name=rawdata.encoding
        df = pd.read_csv (filename, encoding=encoding_name, low_memory=False)
    col_name = df.columns.tolist()
        
    if Defined_col_names [0] not in col_name:
        print ("'Experiment' column is unrecognized in {}, please find the experiment ID column and rename it to 'Experiment'".format (filename))
        
    if Defined_col_names [1] not in col_name:
        print ("'lat' column is unrecognized in {}, please find the latitude column and rename it to 'lat'".format (filename))
        
    if Defined_col_names [2] not in col_name:
        print ("'lon' column is unrecognized in {}, please find the longitude column and rename it to 'lon'".format (filename))
