# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 08:46:38 2019

@author: psarzaeim2, Hasnat

Updated on May 2023 
"""

# Reading G2F Metadata Files  
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
import pathlib
import argparse
import pandas as pd

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
            Output_path = os.path.join(Input_path,'../../G2F data preprocessing/Meta/output')
            Output_dir = output_fdir(Output_path)
    else:
        print(f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../File Control/Meta/output"):
    Input_dir = "../../../File Control/Meta/output"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../G2F data preprocessing/Meta/output'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("File Control/Meta/output"):
    Input_dir = "File Control/Meta/output"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'G2F data preprocessing/Meta/output'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("../File Control/Meta/output"):
    Input_dir = "../File Control/Meta/output"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../G2F data preprocessing/Meta/output'
        Output_dir = output_fdir(Output_path)
else:
    print("No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)


# =============================================================================
# Concatenating the meta files
# =============================================================================
Meta_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
lat_lon_file = pd.concat ([pd.read_csv (f) for f in Meta_files])
lat_lon_file = lat_lon_file [lat_lon_file.Experiment_Type == "H"]
lat_lon_file.to_csv (os.path.abspath(os.path.join(Output_dir ,"All_lat_lon.csv")), index = False)

lat_lon_file.dropna (subset = ["lat", "lon"], inplace = True)
lat_lon_file.to_csv (os.path.abspath(os.path.join(Output_dir ,"0lat_lon.csv")), index = False)