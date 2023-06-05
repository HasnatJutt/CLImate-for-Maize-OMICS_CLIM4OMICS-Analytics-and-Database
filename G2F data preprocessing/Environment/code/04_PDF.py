# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 16:54:33 2020

@author: psarzaeim2, Hasnat

Updated on May 2023 
"""

## Generating PDF Plots for Environmental Variables
# =============================================================================
# Import necessary libraries
# =============================================================================
import os 
import re
import os.path
import glob
import pathlib
import argparse
import numpy as np
import pandas as pd
import seaborn as sns
from functools import reduce
import matplotlib.pyplot as plt

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
            Output_path = os.path.join(Input_path,'../../../G2F data preprocessing/Environment/output/PDF')
            Output_dir = output_fdir(Output_path)
    else:
        print(f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../G2F data preprocessing/Environment/output/G2F Separating"):
    Input_dir = "../../../G2F data preprocessing/Environment/output/G2F Separating"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../G2F data preprocessing/Environment/output/PDF'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("G2F data preprocessing/Environment/output/G2F Separating"):
    Input_dir = "G2F data preprocessing/Environment/output/G2F Separating"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'G2F data preprocessing/Environment/output/PDF'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("../G2F data preprocessing/Environment/output/G2F Separating"):
    Input_dir = "../G2F data preprocessing/Environment/output/G2F Separating"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../G2F data preprocessing/Environment/output/PDF'
        Output_dir = output_fdir(Output_path)
else:
    print("No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================    
# Concatenate variables for each experiment
# =============================================================================
for root, dirs, files in os.walk (Output_dir):
    for file in files:
        os.remove (os.path.join (root, file))
Weather_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
#for f in Weather_files:
lst = [os.path.basename(f)[1:] for f in Weather_files]
Experiments = list (dict.fromkeys (lst))

merge_list = []
read_list = []
for Exp in Experiments:
    for f in Weather_files:
        if os.path.basename(f)[1:] == Exp:
            merge_list.append(f)
    
    for i in merge_list:
        df = pd.read_csv(i)
        df.drop (["Day of Year [Local]"], axis = 1)
#        df ["Experiment"] = Exp 
        read_list.append (df)
        merge = reduce (lambda left,right: pd.merge(left, right, on = ["Day of Year [Local]"], how = "outer"), read_list)
#        concat = pd.concat (read_list, axis = 1)
    merge.to_csv(os.path.abspath(os.path.join(Output_dir , Exp)), index = None)
    
    read_list = []
    merge_list = []
    
# =============================================================================    
# Concatenate experiments to one file
# =============================================================================    
Read_list = []
Experiment_files = glob.glob(os.path.abspath(os.path.join(Output_dir,'*.csv')))
for F in Experiment_files:
    dF = pd.read_csv(F)
    Read_list.append(dF)
    Concat = pd.concat (Read_list, axis = 0)
Concat.to_csv(os.path.abspath(os.path.join(Output_dir , "Weather_File.csv")), index = None)

# =============================================================================    
# Fitting distrubution functions
# =============================================================================  
data = pd.read_csv(os.path.abspath(os.path.join(Output_dir , "Weather_File.csv")), low_memory=False)
data.dropna(inplace = True)
data.drop (data[data["Wind Direction [degrees]"] == "No Wind"].index, inplace = True)

var = ["Temperature [C]", "Dew Point [C]", "Relative Humidity [%]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Wind Speed [m/s]",
       "Wind Direction [degrees]", "Wind Gust [m/s]"] 

for i in var:
    data[i]=pd.to_numeric(data[i], errors='coerce')
    sns.set (style = "darkgrid")
    if i=="Rainfall [mm]":
        pdf = sns.histplot(data[i], kde=True, stat="density", binwidth=5)
    else:
        pdf = sns.histplot(data[i], kde=True, stat="density")
    plt.title ("PDF")
    plt.savefig (os.path.abspath(os.path.join(Output_dir ,"PDF " +  i [:9] + ".png")), dpi = 400)
    plt.close () 
    
    
Data = data [["Temperature [C]", "Dew Point [C]", "Relative Humidity [%]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Wind Speed [m/s]",
       "Wind Direction [degrees]", "Wind Gust [m/s]"]]

pair = sns.pairplot (Data)
plt.savefig (os.path.abspath(os.path.join(Output_dir ,"pairplot" + ".png")), dpi = 400)
plt.close ()