#! /usr/bin/env python

import os
import sys
import csv
import glob
import pathlib
import argparse
import requests
import numpy as np
import pandas as pd
from shutil import copyfile
from __future__ import print_function
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
            Output_path = os.path.join(Input_path, '../../../APIs/DayMet/output/Download')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../G2F data preprocessing/Meta/output/"):
    Input_dir = "../../../G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../APIs/DayMet/output/Download'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("G2F data preprocessing/Meta/output/"):
    Input_dir = "G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'APIs/DayMet/output/Download'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../G2F data preprocessing/Meta/output/"):
    Input_dir = "../G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../APIs/DayMet/output/Download'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print("Input directory = ", Input_dir)
print("Output directory ", Output_dir)
# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../../../G2F data preprocessing/Meta/output/")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../../../APIs/DayMet/output/Download")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"
print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
os.chdir ("../../code/")
if (len(sys.argv) < 2):
    print("Error: Expected input file")
    print("Usage: $ python daymet_multiple_extraction.py FileName")
    sys.exit()

STARTYEAR = 1980

df = pd.read_csv (Input_dir + "lat_lon.csv")
Year_list = df ["Year"].tolist ()
ENDYEAR = max (Year_list)
#ENDYEAR   = 2018

NO_NAME = "NULL"
YEAR_LINE = "years:"
VAR_LINE  = "variables:"
DAYMET_VARIABLES = ['dayl', 'prcp', 'srad', 'swe', 'tmax', 'tmin', 'vp']
DAYMET_YEARS     = [str(year) for year in range(STARTYEAR, ENDYEAR + 1)]
DAYMET_URL_STR = r'https://daymet.ornl.gov/single-pixel/api/data?lat={}&lon={}'

def parse_params(line, param_list):
    start_idx = line.index(":") + 1
    line_split = line[start_idx:].split(",")
    requested_params = []
    for elem in line_split:
        if elem in param_list:
            requested_params.append(elem)
    return ",".join(requested_params)

inF = open(sys.argv[1])
lines = inF.read().lower().replace(" ", "").split("\n")
inF.close()

lats  = []
lons  = []
names = []
requested_vars = ",".join(DAYMET_VARIABLES)
requested_years = ",".join(DAYMET_YEARS)

for line in lines:
    line = line.lower()
    if line:
        if VAR_LINE in line:
            requested_vars = parse_params(line, DAYMET_VARIABLES)
        elif YEAR_LINE in line:
            requested_years = parse_params(line, DAYMET_YEARS)
        else:
            line_split = line.split(",")
            if (len(line_split) > 2):
                names.append(line_split[0])
                lats.append(line_split[1])
                lons.append(line_split[2])
            else:
                names.append(NO_NAME)
                lats.append(line_split[0])
                lons.append(line_split[1])

var_str = ''
if requested_vars:
    var_str = "&measuredParams=" + requested_vars

years_str = ''
if requested_years:
    years_str = "&year=" + requested_years



num_files_requested = len(lats)
num_downloaded = 0
for i in range(num_files_requested):
    curr_url = DAYMET_URL_STR.format(lats[i], lons[i]) + var_str + years_str
    print("Processing:", curr_url)
    res = requests.get(curr_url)
    if not res.ok:
        print("Could not access the following URL:", curr_url)
    else:
        if names[i] == "NULL":
            outFname = res.headers["Content-Disposition"].split("=")[-1]
        else:
            outFname = names[i]
        text_str = res.content
        os.chdir ("../output/Download")
        outF = open(outFname, 'wb')
        outF.write(text_str)
        outF.close()
        res.close()
        num_downloaded += 1
        os.chdir ("../../code")

print("Finished downloading", num_downloaded, "files.")

#Cleaning
#Dir = os.chdir ("../output/Download")
#CSV_files = os.listdir (Dir)
#
#for filename in CSV_files:
#    Filename = filename [:-4].upper () + ".csv"
#    with open (Output_dir + filename) as in_file:
#        with open (Output_dir + Filename, "w", newline = "") as out_file:
#            next (in_file)
#            next (in_file)
#            next (in_file)
#            next (in_file)  
#            next (in_file)
#            next (in_file)
#            next (in_file)
#
#            writer = csv.writer (out_file)
#            for row in csv.reader (in_file):
#                if any (row):
#                    writer.writerow (row)