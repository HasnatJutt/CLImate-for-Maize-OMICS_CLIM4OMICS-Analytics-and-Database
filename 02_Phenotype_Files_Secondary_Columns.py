# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 17:31:21 2019

@author: psarzaeim2, Hasnat

Updated on Wed Apr 26 2023
"""

## Controlling G2F phenotype data files and the columns contents 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
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

print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Read the phenotype files and create the columns
# =============================================================================    
Defined_col_names = ["Year", "Field-Location", "Pedigree", "Plant Height [cm]", "Ear Height [cm]", "Grain Moisture [%]", "Grain Yield [bu/A]"]

Phenotype_files =  glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
#print(Meta_files)
for filename in Phenotype_files:
    try:
        df = pd.read_csv (filename, low_memory=False)
    except:
        with open(filename, "r") as rawdata:
            encoding_name=rawdata.encoding
        df = pd.read_csv (filename, encoding=encoding_name, low_memory=False)  
    col_name = df.columns.tolist()
    try:
        df ["ID"] =  df ["Year"].apply (str) + "_" + df ["Field-Location"].apply (str) + "_" + df ["Pedigree"].apply (str)
        df ["Year.x"] = df ["Year"]
        df ["Loc.x"] = df ["Field-Location"]
        df ["Env.x"] = df ["Year"].apply (str) + "_" + df ["Field-Location"].apply (str)
        df ["Pedigree.x"] = df ["Pedigree"]
        df ["Year.y"] = df ["Year"]
        df ["Experiment"] = df ["Field-Location"]
        df [["P1", "P2"]] = df.Pedigree.str.split ("/", expand = True)
        df = df [["ID", "Year.x", "Loc.x", "Env.x", "Pedigree.x", "Year.y", "Experiment", "P1", "P2", "Plant Height [cm]", "Ear Height [cm]", "Grain Moisture [%]", "Grain Yield [bu/A]"]] 
        df.to_csv (os.path.abspath(os.path.join(Output_dir, os.path.basename(filename))), index = None)
    except Exception as E:
        print(f"The following file {os.path.basename(filename)} is not processed due to exception {E}")