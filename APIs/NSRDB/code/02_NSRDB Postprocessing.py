# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:36:32 2020

@author: psarzaeim2, Hasnat

Updated on May 2023
"""

## Creating pivot tables from NSRDB data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import sys
import glob
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
            Output_path = os.path.join(Input_path, '../NSRDB')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../APIs/NSRDB/output/Download"):
    Input_dir = "../../../APIs/NSRDB/output/Download"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../APIs/NSRDB/output/NSRDB'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("APIs/NSRDB/output/Download"):
    Input_dir = "APIs/NSRDB/output/Download"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'APIs/NSRDB/output/NSRDB'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../APIs/NSRDB/output/Download"):
    Input_dir = "../APIs/NSRDB/output/Download"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../APIs/NSRDB/output/NSRDB'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()

print("Input directory = ", Input_dir)
print("Output directory ", Output_dir)

# =============================================================================
# Pivot tables
# =============================================================================    
file_list = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
for filename in file_list:
    #    print (Output_dir + filename)
    df = pd.read_csv(filename, index_col="Record Number")

    Variables = ["Temperature [C]", "Dew Point [C]", "Solar Radiation [W/m2]", "Wind Speed [m/s]", "Pressure [mb]",
                 "Relative Humidity [%]", "Wind Direction [degrees]", "Precipitable Water [mm]"]
    for var in Variables:
        try:
            df[var] = pd.to_numeric(df[var], errors='coerce')
            df_ave = df.groupby("Day of Year [Local]", as_index=True, dropna=False).agg({var: ["mean", "max", "min"]})
            df_ave.columns = df_ave.columns.to_flat_index()
            df_ave.rename(columns={(var, "max"): "Max " + var,
                                   (var, "min"): "Min " + var,
                                   (var, "mean"): var}, inplace=True)
            if var == "Relative Humidity [%]":
                char_var = "H"
            elif var == "Wind Direction [degrees]":
                char_var = "I"
            elif var == "Precipitable Water [mm]":
                char_var = "C"
            else:
                char_var = var[0]
            df_ave.to_csv(os.path.abspath(os.path.join(Output_dir, char_var + os.path.basename(filename))))
        except Exception as E:
            print(f"The following {var} is not processed due to {E} for {filename}")
