# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 17:31:21 2019

@author: psarzaeim2
"""

## Controlling G2F phenotype data files and the columns contents 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../../../File Upload/Phenotype/")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../../File Control/Phenotype/output")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"

print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Read the phenotype files and create the columns
# =============================================================================    
Defined_col_names = ["Year", "Field-Location", "Pedigree", "Plant Height [cm]", "Ear Height [cm]", "Grain Moisture [%]", "Grain Yield [bu/A]"]

Phenotype_files = os.listdir (Input_dir) 
#print(Meta_files)
for filename in Phenotype_files:
    if "Hybrid" or "hybrid" in filename:
        df = pd.read_csv (Input_dir + filename)
        col_name = list (df.columns)
    
        df ["ID"] =  df ["Year"].apply (str) + "_" + df ["Field-Location"].apply (str) + "_" + df ["Pedigree"].apply (str)
        df ["Year.x"] = df ["Year"]
        df ["Loc.x"] = df ["Field-Location"]
        df ["Env.x"] = df ["Year"].apply (str) + "_" + df ["Field-Location"].apply (str)
        df ["Pedigree.x"] = df ["Pedigree"]
        df ["Year.y"] = df ["Year"]
        df ["Experiment"] = df ["Field-Location"]
        df [["P1", "P2"]] = df.Pedigree.str.split ("/", expand = True)
    
    df = df [["ID", "Year.x", "Loc.x", "Env.x", "Pedigree.x", "Year.y", "Experiment", "P1", "P2", "Plant Height [cm]", "Ear Height [cm]", "Grain Moisture [%]", "Grain Yield [bu/A]"]] 
         
    df.to_csv (filename, index = None) 