# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 12:05:29 2019

@author: psarzaeim2, Hasnat

Updated on May 2023
"""

## Reading and cleanning NWS data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import sys
import glob
import argparse
import pandas as pd
import csv

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

elif os.path.exists("../../../APIs/NWS/output/Download"):
    Input_dir = "../../../APIs/NWS/output/Download"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../APIs/NWS/output/Clean'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("APIs/NWS/output/Download"):
    Input_dir = "APIs/NWS/output/Download"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'APIs/NWS/output/Clean'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../APIs/NWS/output/Download"):
    Input_dir = "../APIs/NWS/output/Download"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../APIs/NWS/output/Clean'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()

print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Removing csv files less that 1 KB (Empty csv files)
# =============================================================================
all_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
for file in all_files:
    if os.stat(file).st_size < 1024:
        os.remove(file)

# =============================================================================
# Reading and fixing each NWS station file as data frame
# =============================================================================

CSV_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))

for filename in CSV_files:
    with open (filename) as in_file:
        with open (os.path.join(Output_dir, os.path.basename(filename)), "w", newline = "") as out_file:
            next (in_file)
            next (in_file)
            next (in_file)
            next (in_file)  
            next (in_file)
            next (in_file)
            next (in_file)
            next (in_file)
            next (in_file)

            writer = csv.writer (out_file)
            for row in csv.reader (in_file):
                if any (row):
                    writer.writerow (row)

NWS_files = glob.glob(os.path.abspath(os.path.join(Output_dir,'*.csv')))
for filename in NWS_files:
    df = pd.read_csv (filename)
    df = df[["station", "valid", "lat", "lon", "tmpf", "dwpf", "relh", "drct", "sknt", "p01i", "alti"]] 
    df.rename (columns = {"valid":"Date", "tmpf":"Temperature [F]", "dwpf":"Dew Point [F]", "relh":"Relative Humidity [%]", 
                          "p01i":"Rainfall [in]", "sknt":"Wind Speed [knot]", "drct":"Wind Direction [degrees]", "alti":"Pressure [in]"}, inplace = True) 
    
    df.index.name = "Record Number"
    
    df ["Date"] = pd.to_datetime (df["Date"], errors = "coerce")
    df ["Day"] = df["Date"].dt.day
    df ["Month"] = df["Date"].dt.month
    df ["Year"] = df["Date"].dt.year
    df ["Day of Year"] = df ["Date"].dt.dayofyear
    df["lat"] = pd.to_numeric (df["lat"], errors = "coerce")
    df["lon"] = pd.to_numeric (df["lon"], errors = "coerce")
    df["Temperature [F]"] = pd.to_numeric (df["Temperature [F]"], errors = "coerce")
    df["Dew Point [F]"] = pd.to_numeric (df["Dew Point [F]"], errors = "coerce")
    df["Relative Humidity [%]"] = pd.to_numeric (df["Relative Humidity [%]"], errors = "coerce")
    df["Rainfall [in]"] = pd.to_numeric (df["Rainfall [in]"], errors = "coerce")
    df["Wind Speed [knot]"] = pd.to_numeric (df["Wind Speed [knot]"], errors = "coerce")
    df["Wind Direction [degrees]"] = pd.to_numeric (df["Wind Direction [degrees]"], errors = "coerce")
    df["Pressure [in]"] = pd.to_numeric (df["Pressure [in]"], errors = "coerce")
    
    convert_dict = {"station": str, "Date": str, "Year": str, "Month": str, "Day": str, "lat": float, "lon": float, "Temperature [F]": float, "Dew Point [F]": float, "Relative Humidity [%]": float, "Rainfall [in]": float, 
                    "Wind Speed [knot]": float, "Wind Direction [degrees]": float, "Pressure [in]": float}
    df = df.astype (convert_dict)
    
    df ["Temperature [C]"] = (df["Temperature [F]"]-32)*5/9
    df ["Dew Point [C]"] = (df["Dew Point [F]"]-32)*5/9
    df ["Rainfall [mm]"] = df["Rainfall [in]"]*25.4
    df ["Wind Speed [m/s]"] = df["Wind Speed [knot]"]*0.5144
    df ["Pressure [mb]"] = df["Pressure [in]"]*33.683
    
    df[["Date", "Time"]] = df["Date"].str.split(" ", expand = True)
       
    df.rename (columns = {"Date": "Date [Local]", "Day":"Day [Local]", "Month":"Month [Local]", "Year":"Year [Local]", 
                          "Time": "Time [Local]", "Day of Year":"Day of Year [Local]"}, inplace = True) 
    
    df = df [["station", "lat", "lon", "Day [Local]", "Month [Local]", "Year [Local]", "Day of Year [Local]", "Date [Local]", "Time [Local]", "Temperature [C]",
              "Dew Point [C]", "Relative Humidity [%]", "Rainfall [mm]", "Wind Speed [m/s]", "Wind Direction [degrees]", "Pressure [mb]"]]
#    df["Date"] = df["Date"].str.replace("/","-")
#    df["Day_of_Year"] = df["Date"].dt.dayofyear
    
    df.to_csv(filename)


station_list = []
Lat_list = []
Lon_list = []

NWS02_files = glob.glob(os.path.abspath(os.path.join(Output_dir,'*.csv')))
for file in NWS02_files:
    df = pd.read_csv ( file)
    station = df.iloc[0,1]
    lat = df.iloc [0,2] 
    lon = df.iloc [0,3]
    
    station_list.append(station)
    Lat_list.append(lat)
    Lon_list.append(lon)

    
    dF = pd.DataFrame (list(zip(station_list, Lat_list, Lon_list)), columns = ["Station", "lat", "lon"])
    dF.index.name = "Record Number"
    dF.to_csv(os.path.join(Output_dir, "../NWS_lat_lon.csv"))