# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 15:49:18 2019

@author: psarzaeim2, Hasnat

Updated on May 2023
"""

## Reading and Crearing Pivot Tables for NWS Environmental Data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import sys
import pathlib
import argparse
import glob
import pandas as pd
import math

# =============================================================================
# Input and Output directories
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory from Current Path', required=False)
parser.add_argument('-o', '--output', help='Path of Output Directory from Current Path', required=False)
parser.add_argument('-m', '--meta', help='Path of Meta Directory (G2F Processing meta) from Current Path', required=False)
parser.add_argument('-nf', '--nearmetafile', help='Name and Path of Near Station File from Current Path', required=False)
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
            Output_path = os.path.join(Input_path, '../Near')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../APIs/NWS/output/Clean"):
    Input_dir = "../../../APIs/NWS/output/Clean"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../APIs/NWS/output/Near'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("APIs/NWS/output/Clean"):
    Input_dir = "APIs/NWS/output/Clean"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'APIs/NWS/output/Near'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../APIs/NWS/output/Clean"):
    Input_dir = "../APIs/NWS/output/Clean"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../APIs/NWS/output/Near'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
if args.nearmetafile is not None:
    latlonpath = os.path.abspath(args.nearmetafile)
    if os.path.exists(latlonpath):
        if os.path.isfile(latlonpath):
            latlonfile = latlonpath
        else:
            latlonfile = os.path.join(latlonpath, "NWS_lat_lon.csv")
    else:
        print(f"The provided path {args.nearmetafile} does not exists. Absolute path based on provided path is {latlonpath}")
elif os.path.exists(Input_dir):
    if os.path.isfile(os.path.join(pathlib.Path(Input_dir).parent, "NWS_lat_lon.csv")):
        latlonfile = os.path.join(pathlib.Path(Input_dir).parent, "NWS_lat_lon.csv")
    elif os.path.isfile(os.path.join(pathlib.Path(Input_dir).parent.parent, "code/NWS_lat_lon.csv")):
        latlonfile = os.path.join(pathlib.Path(Input_dir).parent.parent, "code/NWS_lat_lon.csv")
    elif os.path.isfile(os.path.join(pathlib.Path(Input_dir).parent.parent, "NWS_lat_lon.csv")):
        latlonfile = os.path.join(pathlib.Path(Input_dir).parent.parent, "NWS_lat_lon.csv")
    elif os.path.isfile(os.path.join(pathlib.Path(Input_dir).parent.parent.parent, "NWS_lat_lon.csv")):
        latlonfile = os.path.join(pathlib.Path(Input_dir).parent.parent.parent, "NWS_lat_lon.csv")
    elif os.path.isfile(os.path.join(os.getcwd(), "NWS_lat_lon.csv")):
        latlonfile = os.path.join(os.getcwd(), "NWS_lat_lon.csv")
    elif os.path.isfile(os.path.join(os.getcwd().parent, "output/NWS_lat_lon.csv")):
        latlonfile = os.path.join(os.getcwd().parent, "output/NWS_lat_lon.csv")
    else:
        print(f"The Meta file (lat lon) does not exists, use -m flag to provide location of file")
else:
    if os.path.isfile(os.path.join(os.getcwd(), "NWS_lat_lon.csv")):
        latlonfile = os.path.join(os.getcwd(), "NWS_lat_lon.csv")
    elif os.path.isfile(os.path.join(os.getcwd().parent, "output/NWS_lat_lon.csv")):
        latlonfile = os.path.join(os.getcwd().parent, "output/NWS_lat_lon.csv")
    else:
        print(f"The Meta file (lat lon) does not exists, use -m flag to provide location of file")
if args.meta is not None:
    Input_path2 = os.path.abspath(args.meta)
    if os.path.exists(Input_path2):
        Input_dir2 = Input_path2
    else:
        print(
            f'The input directory {args.meta} does not exists on system path. Correct the Input directory, provided directory has {Input_path1} path')

elif os.path.exists("../../../G2F data preprocessing/Meta/output"):
    Input_dir2 = "../../../G2F data preprocessing/Meta/output"

elif os.path.exists("G2F data preprocessing/Meta/output"):
    Input_dir2 = "G2F data preprocessing/Meta/output"

elif os.path.exists("../G2F data preprocessing/Meta/output"):
    Input_dir2 = "../G2F data preprocessing/Meta/output"
elif os.path.exists("../../G2F data preprocessing/Meta/output"):
    Input_dir2 = "../../G2F data preprocessing/Meta/output"
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()
print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
    
# =============================================================================
# Reading each NWS station file as data frame and finding the nearest NWS station
# =============================================================================
NWS_list = []
dist_list = []
Nearest_NWS_list = []
ind = []

G2F = pd.read_csv(os.path.join(Input_dir2, "lat_lon.csv"))
G2F.dropna(inplace = True)
NWS = pd.read_csv(latlonfile)

for index, row in G2F.iterrows ():
    x = row ["lat"]
    y = row ["lon"]
    station = row ["Experiment"]
    year = row ["Year"]
    
    for index, row in NWS.iterrows ():
        X = row ["lat"]
        Y = row ["lon"]
        Station = row ["Station"]
        
        distance = math.sqrt ((X-x)**2 + (Y-y)**2)
        
        NWS_list.append (Station)
        dist_list.append (distance)
    
    dic = dict (zip (NWS_list, dist_list))
#    print(dic)
         
    Nearest_NWS = min (dic, key = dic.get)
#    Nearest_NWS_list.append (Nearest_NWS)
#    
    print ("Nearest NWS station to {}{} G2F station is: {}".format (year, station, Nearest_NWS))

    file_list = glob.glob(os.path.abspath(os.path.join(Input_dir, '*.csv')))
    for filename in file_list:
        if os.path.basename(filename)[:-4] == Nearest_NWS:
            df = pd.read_csv (filename)
            df.to_csv(os.path.join(Output_dir, str(year) + station + ".csv"), index = None)
            