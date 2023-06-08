# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 16:54:33 2020

@author: psarzaeim2
"""

## Generating PDF Plots for Environmental Variables
# =============================================================================
# Import necessary libraries
# =============================================================================
import os, re, os.path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
#from sklearn.preprocessing import MinMaxScaler

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../output/G2F Separating")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../PDF")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
    
# =============================================================================    
# Concatenate variables for each experiment
# =============================================================================
for root, dirs, files in os.walk (Output_dir):
    for file in files:
        os.remove (os.path.join (root, file))
Weather_files = os.listdir (Input_dir)
for f in Weather_files:
    lst = [f[1:] for f in Weather_files]
Experiments = list (dict.fromkeys (lst))

merge_list = []
read_list = []
for Exp in Experiments:
    for f in Weather_files:
        if f[1:] == Exp:
            merge_list.append (f)
    
    for i in merge_list:
        df = pd.read_csv (Input_dir + i)
        df.drop (["Day of Year [Local]"], axis = 1)
#        df ["Experiment"] = Exp 
        read_list.append (df)
        merge = reduce (lambda left,right: pd.merge(left, right, on = ["Day of Year [Local]"], how = "outer"), read_list)
#        concat = pd.concat (read_list, axis = 1)
    merge.to_csv (Output_dir + Exp, index = None)
    
    read_list = []
    merge_list = []
    
# =============================================================================    
# Concatenate experiments to one file
# =============================================================================    
Read_list = []
Experiment_files = os.listdir (Output_dir)
for F in Experiment_files:
    dF = pd.read_csv (Output_dir + F)
    Read_list.append (dF)
    Concat = pd.concat (Read_list, axis = 0)
Concat.to_csv (Output_dir + "Weather_File" + ".csv", index = None)

# =============================================================================    
# Fitting distrubution functions
# =============================================================================  
data = pd.read_csv (Output_dir + "Weather_File.csv", dtype = "float64")
data.dropna (inplace = True)
data.drop (data[data["Wind Direction [degrees]"] == "No Wind"].index, inplace = True)

var = ["Temperature [C]", "Dew Point [C]", "Relative Humidity [%]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Wind Speed [m/s]",
       "Wind Direction [degrees]", "Wind Gust [m/s]"] 

for i in var:
    sns.set (style = "darkgrid")
    pdf = sns.distplot (data [i])
    plt.title ("PDF")
    plt.savefig ("PDF " +  i [:9] + ".png", dpi = 400)
    plt.close () 
    
    
Data = data [["Temperature [C]", "Dew Point [C]", "Relative Humidity [%]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Wind Speed [m/s]",
       "Wind Direction [degrees]", "Wind Gust [m/s]"]]

pair = sns.pairplot (Data)
plt.savefig ("pairplot" + ".png", dpi = 400)
plt.close ()