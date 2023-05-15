# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 15:49:18 2019

@author: psarzaeim2
"""

## Reading and Crearing Pivot Tables for NWS Environmental Data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd
import math

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../output/Clean")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"

path = os.chdir ("..")
Input_dir1 = os.getcwd ().replace ("\\", "/")
Input_dir1 = Input_dir1 + "/"

path = os.chdir ("../../../G2F data preprocessing/Meta/output/")
Input_dir2 = os.getcwd ().replace ("\\", "/")
Input_dir2 = Input_dir2 + "/"

Output_dir = os.chdir ("../../../APIs/NWS/output/Near/")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"

print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
    
# =============================================================================
# Reading each NWS station file as data frame and finding the nearest NWS station
# =============================================================================
NWS_list = []
dist_list = []
Nearest_NWS_list = []
ind = []

G2F = pd.read_csv (Input_dir2 + "lat_lon.csv")
G2F.dropna (inplace = True)
NWS = pd.read_csv (Input_dir1 + "NWS_lat_lon.csv")

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
               

    for filename in os.listdir (Input_dir):
        if filename [:-4] == Nearest_NWS:
#            print("YES")
            df = pd.read_csv (Input_dir + filename)
            df.to_csv (Output_dir + str (year) + station + ".csv", index = None)
            