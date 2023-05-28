# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 12:05:29 2019

@author: psarzaeim2
"""

## Reading and cleanning NWS data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
import pandas as pd
import csv

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../output/Download")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../Clean")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"
print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
       
# =============================================================================
# Removing txt files    
# =============================================================================
all_files = os.listdir (Input_dir)
#print(all_files)
for file in all_files:
    if not file.endswith (".csv"):
        os.remove (os.path.join (Input_dir, file))

# =============================================================================
# Removing csv files less that 1 KB (Empty csv files)
# =============================================================================
for (dirpath, dirnames, filenames) in os.walk (Input_dir):
    for file in filenames:
        fullpath = os.path.join(Input_dir, file)
        if os.path.getsize(fullpath) < 1 * 1024: 
#            print("remove")
            os.remove(fullpath)
#        
# =============================================================================
# Reading and fixing each NWS station file as data frame
# =============================================================================
os.chdir (Input_dir)
extension = "csv"
CSV_files = [f for f in glob.glob ("*.{}".format (extension))]

for filename in CSV_files:
    with open (Input_dir + filename) as in_file:
        with open (Output_dir + filename, "w", newline = "") as out_file:
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

NWS_files = os.listdir (Output_dir)
for filename in NWS_files:
    df = pd.read_csv (Output_dir + filename)      
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
    
    df.to_csv (Output_dir + filename)  


station_list = []
Lat_list = []
Lon_list = []

NWS02_files = os.listdir (Output_dir)
for file in NWS02_files:
    
    df = pd.read_csv (Output_dir + file)    
    station = df.iloc [0,1]      
    lat = df.iloc [0,2] 
    lon = df.iloc [0,3]
    
    station_list.append(station)
    Lat_list.append(lat)
    Lon_list.append(lon)

    
    dF = pd.DataFrame (list(zip(station_list, Lat_list, Lon_list)), columns = ["Station", "lat", "lon"])
    dF.index.name = "Record Number"
    os.chdir ("../")
    dF.to_csv ("NWS_lat_lon" + ".csv")
    os.chdir (Output_dir)