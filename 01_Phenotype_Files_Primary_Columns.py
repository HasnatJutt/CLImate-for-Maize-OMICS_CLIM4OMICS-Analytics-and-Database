# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 17:08:54 2019

@author: psarzaeim2, Hasnat

Updated on Wed Apr 26 2023
"""

## Controlling G2F phenotype data files and the columns names 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import re
import glob
import chardet
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
if os.path.exists("../../../File Upload/Phenotype"):
    Input_dir = "../../../File Upload/Phenotype"
    if os.path.exists("../../../File Control/Phenotype/output"):
        Output_dir = "../../../File Control/Phenotype/output"
    else:
        os.makedirs("../../../File Control/Phenotype/output")
        Output_dir = "../../../File Control/Phenotype/output"   
elif os.path.exists("File Upload/Phenotype"):
    Input_dir = "File Upload/Phenotype"     
    if os.path.exists("File Control/Phenotype/output"):
        Output_dir = "File Control/Phenotype/output"
    elif len(sys.argv)==2 and re.match(r'[\w$\\/._-\s]', sys.argv[1]):
        Output_dir = sys.argv[1]
    else:
        os.makedirs("File Control/Phenotype/output")
        Output_dir = "File Control/Phenotype/output"
elif os.path.exists("../File Upload/Phenotype"):
    Input_dir = "../File Upload/Phenotype"     
    if os.path.exists("../File Control/Phenotype/output"):
        Output_dir = "../File Control/Phenotype/output"
    elif len(sys.argv)==2 and re.match(r'[\w$\\/._-\s]', sys.argv[1]):
        Output_dir = sys.argv[1]
    else:
        os.makedirs("../File Control/Phenotype/output")
        Output_dir = "../File Control/Phenotype/output"
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
# Read the phenotype files and check the columns names
# =============================================================================        
Defined_col_names = ["Year", "Field-Location", "Pedigree", "Plant Height [cm]", "Ear Height [cm]", "Grain Moisture [%]", "Grain Yield [bu/A]"]

Phenotype_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
#print(Meta_files)
for filename in Phenotype_files:
    #if "Hybrid" or "hybrid" in filename:
    try:
        df = pd.read_csv (filename, low_memory=False)
    except:
        with open(filename, "r") as rawdata:
            encoding_name=rawdata.encoding
        df = pd.read_csv (filename, encoding=encoding_name, low_memory=False)
    col_name = df.columns.tolist()   
    if Defined_col_names [0] not in col_name:
        print ("'Year' column is unrecognized in {}, please find the year column and rename it to 'Year'".format (filename))
   
    if Defined_col_names [1] not in col_name:
        print ("'Field-Location' column is unrecognized in {}, please find the experiment ID column and rename it to 'Field-Location'".format (filename)) 
    
    if Defined_col_names [2] not in col_name:
        print ("'Pedigree' column is unrecognized in {}, plase find the predigree column and rename it to 'Pedigree'".format (filename)) 

    if Defined_col_names [3] not in col_name:
        print ("'Plant Height [cm]' column is unrecognized in {}, please find the plant hight values column and rename it to 'Plant Height [cm]'".format (filename))
      
    if Defined_col_names [4] not in col_name:
        print ("'Ear Height [cm]' column is unrecognized in {}, please find the ear hight values column and rename it to 'Ear Height [cm]'".format (filename))
           
    if Defined_col_names [5] not in col_name:
        print ("'Grain Moisture [%]' column is unrecognized in {}, please find the grain moisture values column and rename it to 'Grain Moisture [%]'".format (filename))

    if Defined_col_names [6] not in col_name:
        print ("'Grain Yield [bu/A]' column is unrecognized in {}, please find the grain yield values column and rename it to 'Grain Yield [bu/A]'".format (filename))
        

      