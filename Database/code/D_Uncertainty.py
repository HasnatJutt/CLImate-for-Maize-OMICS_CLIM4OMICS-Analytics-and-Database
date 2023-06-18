# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 11:40:36 2022

@author: psarzaeim2, Hasnat

Updated on May 2023
"""

## Reading data from data sources  
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
import math
import pathlib
import argparse
import statistics
import numpy as np
import pandas as pd
import seaborn as sns
from shutil import copyfile
from functools import reduce
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt


# =============================================================================
# Input and Output directories
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory (All Files) from Current Path', required=False)
parser.add_argument('-i1', '--input1', help='Path of Input Directory1 (NSRDB) from Current Path', required=False)
parser.add_argument('-i2', '--input2', help='Path of Input Directory2 (DayMet) from Current Path', required=False)
parser.add_argument('-i3', '--input3', help='Path of Input Directory3 (NWS) from Current Path', required=False)
parser.add_argument('-o1', '--output1', help='Path of Output Directory1 (Uncertainty) from Current Path', required=False)
parser.add_argument('-o2', '--output2', help='Path of Output Directory1 (Uncertainty Plots) from Current Path', required=False)
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
    if args.input1 is not None:
        Input_path1 = os.path.abspath(args.input1)
    else:
        Input_path1 = os.path.join(Input_path, '../../APIs/NSRDB/output/NSRDB')
    if args.input2 is not None:
        Input_path2 = os.path.abspath(args.input2)
    else:
        Input_path1 = os.path.join(Input_path, '../../APIs/DayMet/output/DayMet')
    if args.input3 is not None:
        Input_path3 = os.path.abspath(args.input3)
    else:
        Input_path1 = os.path.join(Input_path, '../../APIs/NWS/output/NWS')
    if os.path.exists(Input_path):
        Input_dir = Input_path
        if os.path.exists(Input_path1):
            Input_dir1 = Input_path1
        else:
            print(
                f'The input directory {args.input1} does not exists on system path. Correct the Input directory, provided directory has {Input_path1} path')
        if os.path.exists(Input_path2):
            Input_dir2 = Input_path2
        else:
            print(
                f'The input directory {args.input2} does not exists on system path. Correct the Input directory, provided directory has {Input_path2} path')
        if os.path.exists(Input_path3):
            Input_dir3 = Input_path3
        else:
            print(
                f'The input directory {args.input3} does not exists on system path. Correct the Input directory, provided directory has {Input_path3} path')
        if args.output1 is not None:
            Output_dir1 = output_fdir(args.output1)
            if args.output2 is not None:
                Output_dir2 = output_fdir(args.output2)
            else:
                Output_path2 = os.path.join(Output_dir1, '../../../Database/output/Uncertainty')
                Output_dir2 = output_fdir(Output_path2)


    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../Database/output/All_Files"):
    Input_dir = "../../Database/output/All_Files"
    if os.path.exists("../../APIs/NSRDB/output/NSRDB"):
        Input_dir1 = "../../APIs/NSRDB/output/NSRDB"
    else:
        print(f"The Directory APIs/NSRDB/output/NSRDB do not exits")
    if os.path.exists("../../APIs/DayMet/output/DayMet"):
        Input_dir2 = "../../APIs/DayMet/output/DayMet"
    else:
        print(f"The Directory APIs/DayMet/output/DayMet do not exits")
    if os.path.exists("../../APIs/NWS/output/NWS"):
        Input_dir3 = "../../APIs/NWS/output/NWS"
    else:
        print(f"The Directory APIs/NWS/output/NWS do not exits")
    if args.output1 is not None:
        Output_dir1 = output_fdir(args.output1)
    else:
        Output_path1 = '../../Database/output/Uncertainty'
        Output_dir1 = output_fdir(Output_path1)
    if args.output2 is not None:
        Output_dir2 = output_fdir(args.output2)
    else:
        Output_path2 = '../../Database/output/D/uncertainty_plots'
        Output_dir2 = output_fdir(Output_path2)
elif os.path.exists("Database/output/All_Files"):
    Input_dir = "Database/output/All_Files"
    if os.path.exists("APIs/NSRDB/output/NSRDB"):
        Input_dir1 = "APIs/NSRDB/output/NSRDB"
    else:
        print(f"The Directory APIs/NSRDB/output/NSRDB do not exits")
    if os.path.exists("APIs/DayMet/output/DayMet"):
        Input_dir2 = "APIs/DayMet/output/DayMet"
    else:
        print(f"The Directory APIs/DayMet/output/DayMet do not exits")
    if os.path.exists("APIs/NWS/output/NWS"):
        Input_dir3 = "APIs/NWS/output/NWS"
    else:
        print(f"The Directory APIs/NWS/output/NWS do not exits")
    if args.output1 is not None:
        Output_dir1 = output_fdir(args.output1)
    else:
        Output_path1 = 'Database/output/Uncertainty'
        Output_dir1 = output_fdir(Output_path1)
    if args.output2 is not None:
        Output_dir2 = output_fdir(args.output2)
    else:
        Output_path2 = 'Database/output/D/uncertainty_plots'
        Output_dir2 = output_fdir(Output_path2)

elif os.path.exists("../Database/output/All_Files"):
    Input_dir = "../Database/output/All_Files"
    if os.path.exists("../APIs/NSRDB/output/NSRDB"):
        Input_dir1 = "../APIs/NSRDB/output/NSRDB"
    else:
        print(f"The Directory APIs/NSRDB/output/NSRDB do not exits")
    if os.path.exists("../APIs/DayMet/output/DayMet"):
        Input_dir2 = "../APIs/DayMet/output/DayMet"
    else:
        print(f"The Directory APIs/DayMet/output/DayMet do not exits")
    if os.path.exists("../APIs/NWS/output/NWS"):
        Input_dir3 = "../APIs/NWS/output/NWS"
    else:
        print(f"The Directory APIs/NWS/output/NWS do not exits")
    if args.output1 is not None:
        Output_dir1 = output_fdir(args.output1)
    else:
        Output_path1 = '../Database/output/Uncertainty'
        Output_dir1 = output_fdir(Output_path1)
    if args.output2 is not None:
        Output_dir2 = output_fdir(args.output2)
    else:
        Output_path2 = '../Database/output/D/uncertainty_plots'
        Output_dir2 = output_fdir(Output_path2)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print("Input directory = ", Input_dir)
print ("Output directory = ", Output_dir1)

SC1 = os.listdir (Input_dir1)
SC2 = os.listdir (Input_dir2)
SC3 = os.listdir (Input_dir3)

Abb = "D"
variable = "Dew Point [C]"
files = os.listdir (Input_dir)
for file in files:
    if file [0] == Abb:
        df = pd.read_csv (os.path.join(Input_dir, file))
        df.rename(columns={'Day': 'Day of Year [Local]'}, inplace=True)
        dfs = [df]
        
        for i in SC1:
            if i == file:
                
                data1 = pd.read_csv (os.path.join(Input_dir1, i), usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
                data1.rename (columns = {variable:"NSRDB " + variable,
                                         "Min " + variable:"Min NSRDB " + variable,
                                         "Max " + variable:"Max NSRDB " + variable}, inplace = True)
                dfs.append (data1)
    
        # for j in SC2:
        #     if j == file:
                
        #         data2 = pd.read_csv (Input_dir2 + j, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
        #         data2.rename (columns = {variable:"DayMet " + variable,
        #                                  "Min " + variable:"Min DayMet " + variable,
        #                                  "Max " + variable:"Max DayMet " + variable}, inplace = True)
        #         dfs.append (data2)
                
        for k in SC3:
            if k == file:
                                        
                data3 = pd.read_csv (os.path.join(Input_dir3, k), usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
                data3.rename (columns = {variable:"NWS " + variable,
                                         "Min " + variable:"Min NWS " + variable,
                                         "Max " + variable:"Max NWS " + variable}, inplace = True)      
                dfs.append (data3)
                    
                        
        df_merged = reduce (lambda left, right: pd.merge (left, right, on = ["Day of Year [Local]"], how = "inner"), dfs)
                            
        df_merged.to_csv(os.path.join (Output_dir1 , file), index = None)
        
# =============================================================================
# Error
# =============================================================================
Err1_list = []
Err2_list = []
Err3_list = []

files = os.listdir (Output_dir1)
for file in files:
    if file [0] == Abb:
        df = pd.read_csv (os.path.join(Output_dir1, file))
        
        col_list = list (df)
        # print(file)
        # print(col_list)
        
        if "NSRDB " + variable in col_list:
            df["Err-NSRDB"] = df[Abb + "M"] - df["NSRDB " + variable]
            Err1 = df["Err-NSRDB"].tolist()
            # Err1 = statistics.mean(Err1) 
            Err1_list.append (Err1)
    
        # if "DayMet " + variable in col_list:   
        #     df["Err-DayMet"] = df[Abb + "M"] - df["DayMet " + variable]
        #     Err2 = df["Err-DayMet"].tolist()
        #     # Err2 = statistics.mean(Err2) 
        #     Err2_list.append (Err2)
            
        if "NWS " + variable in col_list:
            df["Err-NWS"] = df[Abb + "M"] - df["NWS " + variable]
            Err3 = df["Err-NWS"].tolist()
            # Err3 = statistics.mean(Err3)
            Err3_list.append (Err3)

    df.to_csv(os.path.join (Output_dir1 , file), index = None)
    
Err1_list_flat = [item for sublist in Err1_list for item in sublist] 
# Err2_list_flat = [item for sublist in Err2_list for item in sublist]
Err3_list_flat = [item for sublist in Err3_list for item in sublist]  
    
# =============================================================================
# Plotting PDFs of Errors
# =============================================================================
ax = plt.subplots()
ax = sns.kdeplot(Err1_list_flat, label = "G2F-NSRDB", color = "mediumseagreen")
SD_1 = statistics.pstdev (Err1_list_flat)
#ax.text (-40, 0.2, '$SD_{G2F-NSRDB}$' + " = " + str (round (SD_1, 2)), fontsize = 10)
# Err2 = sns.displot (Err2_list_flat, label = "G2F-DayMet", color = "coral")
# SD_2 = statistics.pstdev (Err2_list_flat)
# plt.text (-18, 0.41, '$SD_{G2F-DayMet}$' + " = " + str (round (SD_2, 2)), fontsize = 12)

ax = sns.kdeplot(Err3_list_flat, label = "G2F-NWS", color = "cornflowerblue")
Err3_list_flat = [x for x in Err3_list_flat if math.isnan(x) == False]
SD_2 = statistics.pstdev (Err3_list_flat)
# ax.text (-40, 0.18, '$SD_{G2F-NWS}$' + " = " + str (round (SD_2, 2)), fontsize = 10)
xlimits = [abs(ax.get_xlim()[0]), abs(ax.get_xlim()[1])]
if xlimits.index(max(xlimits)) == 0:
    ax.set_xlim(ax.get_xlim()[0], abs(ax.get_xlim()[0]))
else:
    if ax.get_xlim()[0] > 0:
        ax.set_xlim(ax.get_xlim()[0], abs(ax.get_xlim()[1]))
    else:
        ax.set_xlim(-1*(ax.get_xlim()[1]), abs(ax.get_xlim()[1]))
plt.title('$SD_{G2F-NSRDB}$' + " = " + str (round (SD_1, 2))+"  ,  "+'$SD_{G2F-NWS}$' + " = " + str (round (SD_2, 2)))
plt.xlabel ("Err-D")
plt.ylabel ("Density")
plt.legend () 
#plt.title ("Error")
plt.xticks(fontsize = 12)
plt.legend (fontsize = 8)


plt.savefig(os.path.join(Output_dir2, "PDF " + "Error" + ".png"), dpi = 400)
plt.close ()