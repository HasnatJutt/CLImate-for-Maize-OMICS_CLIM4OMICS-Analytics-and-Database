# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:45:11 2019

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
            Output_path = os.path.join(Input_path,'../../G2F data preprocessing/Environment/output/Weather Data Reading')
            Output_dir = output_fdir(Output_path)
    else:
        print(f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../File Control/Environment/output"):
    Input_dir = "../../../File Control/Environment/output"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../G2F data preprocessing/Environment/output/Weather Data Reading'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("File Control/Environment/output"):
    Input_dir = "File Control/Environment/output"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'G2F data preprocessing/Environment/output/Weather Data Reading'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("../File Control/Environment/output"):
    Input_dir = "../File Control/Environment/output"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../G2F data preprocessing/Environment/output/Weather Data Reading'
        Output_dir = output_fdir(Output_path)
else:
    print("No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Counting the number of yaers and list the subdirectory of environment data files
# =============================================================================
Weather_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv'))) 
for filename in Weather_files:
    try:
        df = pd.read_csv (filename, low_memory=False)
    except:
        with open(filename, "r") as rawdata:
            encoding_name=rawdata.encoding
        df = pd.read_csv (filename, encoding=encoding_name, low_memory=False)
    df["Experiment_ID"] = df["Year [Local]"].astype(str) + df["Experiment"]
    Experiments = df["Experiment"].unique().tolist()
#    print(Experiments)
    for exp in Experiments:
        Experiment = df.loc [df["Experiment"] == exp]
        Year = Experiment ["Year [Local]"].unique ()
#        print (str (exp))
#        print (str (Year))
        Experiment.to_csv(os.path.abspath(os.path.join(Output_dir, str(Year[0]) + str(exp) + ".csv")), index = None)