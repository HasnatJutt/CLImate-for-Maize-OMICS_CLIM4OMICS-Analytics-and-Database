# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:36:55 2020

@author: psarzaeim2, Hasnat

Updated on May 2023 
"""

## Controlling G2F weather data files and the columns names 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
import pathlib
import argparse
import numpy as np
import pandas as pd
from shutil import copyfile

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
            Output_path = os.path.join(Input_path, '../../../APIs/DayMet/output')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../G2F data preprocessing/Meta/output/"):
    Input_dir = "../../../G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../APIs/DayMet/output'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("G2F data preprocessing/Meta/output/"):
    Input_dir = "G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'APIs/DayMet/output'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../G2F data preprocessing/Meta/output/"):
    Input_dir = "../G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../APIs/DayMet/output'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print("Input directory = ", Input_dir)
print("Output directory ", Output_dir)

# =============================================================================    
# Conversion
# =============================================================================
df = pd.read_csv(os.path.abspath(os.path.join(Input_dir, 'lat_lon.csv')))
df = df [["Experiment_ID", "lat", "lon"]]
df ["Experiment_ID"] = df ["Experiment_ID"].astype(str) + ".csv"
convert = {"Experiment_ID": object, "lat": float, "lon": float}
df.dropna (inplace = True)

np.savetxt(os.path.abspath(os.path.join(Output_dir, "latlon.txt")) , df.values, fmt = "%s", delimiter = ',')