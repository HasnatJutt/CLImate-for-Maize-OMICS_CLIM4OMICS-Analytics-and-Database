# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 17:08:54 2019

@author: psarzaeim2
"""

## Controlling G2F phenotype data files and the columns names 
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

print ("Input directory = ", Input_dir)
# print ("Output directory = ", Output_dir)

# =============================================================================
# Read the phenotype files and check the columns names
# =============================================================================        
Defined_col_names = ["Year", "Field-Location", "Pedigree", "Plant Height [cm]", "Ear Height [cm]", "Grain Moisture [%]", "Grain Yield [bu/A]"]

Phenotype_files = os.listdir (Input_dir) 
#print(Meta_files)
for filename in Phenotype_files:
    if "Hybrid" or "hybrid" in filename:
        df = pd.read_csv (Input_dir + filename)
        col_name = list (df.columns)
        
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
        

      