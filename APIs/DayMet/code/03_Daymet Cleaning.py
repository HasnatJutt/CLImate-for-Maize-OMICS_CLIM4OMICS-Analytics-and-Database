# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:52:16 2020

@author: psarzaeim2, Hasnat

Updated on May 2023
"""

## Reading and cleanning DayMet data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import sys
import glob
import csv
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
            Output_path = os.path.join(Input_path, '../Clean')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../APIs/DayMet/output/Download"):
    Input_dir = "../../../APIs/DayMet/output/Download"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../APIs/DayMet/output/Clean'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("APIs/DayMet/output/Download"):
    Input_dir = "APIs/DayMet/output/Download"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'APIs/DayMet/output/Clean'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../APIs/DayMet/output/Download"):
    Input_dir = "../APIs/DayMet/output/Download"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../APIs/DayMet/output/Clean'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()

print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
    
# =============================================================================
# Reading and fixing each DayMet station file as data frame
# =============================================================================
CSV_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))

for filename in CSV_files:
    Filename = os.path.basename(filename)[:-4].upper() + ".csv"
    with open (os.path.join(Input_dir, Filename), "r") as in_file:
        with open (os.path.join(Output_dir, Filename), "w", newline = "") as out_file:
            next (in_file)
            next (in_file)
            next (in_file)
            next (in_file)  
            next (in_file)
            next (in_file)
            next (in_file)

            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if any (row):
                    writer.writerow(row)

DayMet_files = glob.glob(os.path.abspath(os.path.join(Output_dir,'*.csv')))
for filename in DayMet_files:
    Filename = os.path.basename(filename)[:-4].upper() + ".csv"
    df = pd.read_csv(os.path.join(Output_dir, Filename))
    
    df["Temperature [C]"] = df[["tmin (deg c)", "tmax (deg c)"]].mean(axis = 1)
    df["Pressure [mb]"] = df["vp (Pa)"]*0.01
       
    df.rename(columns = {"year": "Year [Local]", "yday":"Day of Year [Local]", "srad (W/m^2)":"Solar Radiation [W/m2]", "prcp (mm/day)":"Rainfall [mm]",
                          "swe (kg/m^2)":"Snow Water Equivalent [kg/m2]", "dayl (s)":"Day Light [s]"}, inplace = True)    
    
    df = df[["Day of Year [Local]", "Year [Local]", "Temperature [C]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Pressure [mb]", "Snow Water Equivalent [kg/m2]", "Day Light [s]"]]
    df.index.name = "Record Number"
    
    Year = Filename[:4]
    df = df[df["Year [Local]"] == int(Year)]
    
    df.to_csv(os.path.join(Output_dir, Filename))
    

    