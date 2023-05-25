# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 16:57:02 2019

@author: psarzaeim2, Hasnat

Updated on May 2023 
"""

## Controlling G2F weather data files and the columns names 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import re
import glob
import pathlib
import argparse
import pandas as pd
from shutil import copyfile, copy2

# =============================================================================
# Input and Output directories
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory from Current Path', required=False)
parser.add_argument('-o', '--output', help='Path of Output Directory from Current Path', required=False)
args = parser.parse_args()
def output_fdir(argument_path):
    dir_path = os.path.abspath(argument_path)
    if os.path.exists(dir_path):
        dir_name = dir_path
    else:
        os.makedirs(dir_path)
        dir_name = dir_path
    return dir_name

if args.input is not None:
    Input_path = os.path.abspath(args.input)
    if os.path.exists(Input_path):
        Input_dir = Input_path
        if args.output is not None:
            Output_dir = output_fdir(args.output)
        else:
            Output_path = os.path.join(Input_path,'../../../G2F data preprocessing/Environment/output/Name Fixing')
            Output_dir = output_fdir(Output_path)
    else:
        print(f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../G2F data preprocessing/Environment/output/Weather Data Reading"):
    Input_dir = "../../../G2F data preprocessing/Environment/output/Weather Data Reading"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../G2F data preprocessing/Environment/output/Name Fixing'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("G2F data preprocessing/Environment/output/Weather Data Reading"):
    Input_dir = "G2F data preprocessing/Environment/output/Weather Data Reading"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'G2F data preprocessing/Environment/output/Name Fixing'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("../G2F data preprocessing/Environment/output/Weather Data Reading"):
    Input_dir = "../G2F data preprocessing/Environment/output/Weather Data Reading"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../G2F data preprocessing/Environment/output/Name Fixing'
        Output_dir = output_fdir(Output_path)
else:
    print("No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Separating the names of experiments with more than 1 name in their files names (the experiments in the same location)
# ============================================================================= 
G2F_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
#print(G2F_files)  

for file in G2F_files:
    filename = os.path.basename(file)
    Year = filename[0:4]
    Experiment = re.split(r'[_\n\t\f\v\r ]+', filename[4:].split('.')[0])
    for name in Experiment:
        src = file
        des = os.path.join(Output_dir, str(Year) + name  + ".csv")
        copyfile(src, des)
