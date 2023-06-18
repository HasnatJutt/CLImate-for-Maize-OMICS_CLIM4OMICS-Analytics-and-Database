# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 09:12:58 2020

@author: psarzaeim2, Hasnat

Updated on May 2023
"""

## Reading data from data sources  
# =============================================================================
# Import necessary libraries
# =============================================================================



import os
import glob
import pathlib
import argparse
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
parser.add_argument('-i', '--input', help='Path of Input Directory (G2F Separating) from Current Path', required=False)
parser.add_argument('-i1', '--input1', help='Path of Input Directory1 (NSRDB) from Current Path', required=False)
parser.add_argument('-i2', '--input2', help='Path of Input Directory2 (DayMet) from Current Path', required=False)
parser.add_argument('-i3', '--input3', help='Path of Input Directory3 (NWS) from Current Path', required=False)
parser.add_argument('-o1', '--output1', help='Path of Output Directory1 (Output) from Current Path', required=False)
parser.add_argument('-o2', '--output2', help='Path of Output Directory2 (Plots) from Current Path', required=False)
parser.add_argument('-o3', '--output3', help='Path of Output Directory3 (Complete) from Current Path', required=False)
parser.add_argument('-o4', '--output4', help='Path of Output Directory4 (Empty) from Current Path', required=False)
parser.add_argument('-o5', '--output5', help='Path of Output Directory5 (Enough) from Current Path', required=False)
parser.add_argument('-o6', '--output6', help='Path of Output Directory6 (Not Enough) from Current Path', required=False)
parser.add_argument('-o7', '--output7', help='Path of Output Directory7 (Less) from Current Path', required=False)
parser.add_argument('-o8', '--output8', help='Path of Output Directory8 (More) from Current Path', required=False)
parser.add_argument('-o9', '--output9', help='Path of Output Directory9 (No Lat Lon) from Current Path', required=False)
parser.add_argument('-o10', '--output10', help='Path of Output Directory10 (All Files) from Current Path', required=False)

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
        Input_path1 = os.path.join(Input_path, '../../../../APIs/NSRDB/output/NSRDB')
    if args.input2 is not None:
        Input_path2 = os.path.abspath(args.input2)
    else:
        Input_path1 = os.path.join(Input_path, '../../../../APIs/DayMet/output/DayMet')
    if args.input3 is not None:
        Input_path3 = os.path.abspath(args.input3)
    else:
        Input_path1 = os.path.join(Input_path, '../../../../APIs/NWS/output/NWS')
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
                Output_path2 = os.path.join(Output_dir1, '../plots')
                Output_dir2 = output_fdir(Output_path2)
            if args.output3 is not None:
                Output_dir3 = output_fdir(args.output3)
            else:
                Output_path3 = os.path.join(Output_dir1, '../complete')
                Output_dir3 = output_fdir(Output_path3)
            if args.output4 is not None:
                Output_dir4 = output_fdir(args.output4)
            else:
                Output_path4 = os.path.join(Output_dir1, '../empty')
                Output_dir4 = output_fdir(Output_path4)
            if args.output5 is not None:
                Output_dir5 = output_fdir(args.output5)
            else:
                Output_path5 = os.path.join(Output_dir1, '../enough')
                Output_dir5 = output_fdir(Output_path5)
            if args.output6 is not None:
                Output_dir6 = output_fdir(args.output6)
            else:
                Output_path6 = os.path.join(Output_dir1, '../not_enough')
                Output_dir6 = output_fdir(Output_path6)
            if args.output7 is not None:
                Output_dir7 = output_fdir(args.output7)
            else:
                Output_path7 = os.path.join(Output_dir1, '../less')
                Output_dir7 = output_fdir(Output_path7)
            if args.output8 is not None:
                Output_dir8 = output_fdir(args.output8)
            else:
                Output_path8 = os.path.join(Output_dir1, '../more')
                Output_dir8 = output_fdir(Output_path8)
            if args.output9 is not None:
                Output_dir9 = output_fdir(args.output9)
            else:
                Output_path9 = os.path.join(Output_dir1, '../no_lat_lon')
                Output_dir9 = output_fdir(Output_path9)
            if args.output10 is not None:
                Output_dir10 = output_fdir(args.output10)
            else:
                Output_path10 = os.path.join(Output_dir1, '../../All_Files')
                Output_dir10 = output_fdir(Output_path10)

        else:
            Output_path1 = os.path.join(Input_path, '../../../../Database/output/D/output')
            Output_dir1 = output_fdir(Output_path1)
            Output_path2 = os.path.join(Input_path, '../../../../Database/output/D/plots')
            Output_dir2 = output_fdir(Output_path2)
            Output_path3 = os.path.join(Input_path, '../../../../Database/output/D/complete')
            Output_dir3 = output_fdir(Output_path3)
            Output_path4 = os.path.join(Input_path, '../../../../Database/output/D/empty')
            Output_dir4 = output_fdir(Output_path4)
            Output_path5 = os.path.join(Input_path, '../../../../Database/output/D/enough')
            Output_dir5 = output_fdir(Output_path5)
            Output_path6 = os.path.join(Input_path, '../../../../Database/output/D/not_enough')
            Output_dir6 = output_fdir(Output_path6)
            Output_path7 = os.path.join(Input_path, '../../../../Database/output/D/less')
            Output_dir7 = output_fdir(Output_path7)
            Output_path8 = os.path.join(Input_path, '../../../../Database/output/D/more')
            Output_dir8 = output_fdir(Output_path8)
            Output_path9 = os.path.join(Input_path, '../../../../Database/output/D/no_lat_lon')
            Output_dir9 = output_fdir(Output_path9)
            Output_path10 = os.path.join(Input_path, '../../../../Database/output/All_Files')
            Output_dir10 = output_fdir(Output_path10)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../G2F data preprocessing/Environment/output/G2F Separating"):
    Input_dir = "../../G2F data preprocessing/Environment/output/G2F Separating"
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
        Output_path1 = '../../Database/output/D/output'
        Output_dir1 = output_fdir(Output_path1)
    if args.output2 is not None:
        Output_dir2 = output_fdir(args.output2)
    else:
        Output_path2 = '../../Database/output/D/plots'
        Output_dir2 = output_fdir(Output_path2)
    if args.output3 is not None:
        Output_dir3 = output_fdir(args.output3)
    else:
        Output_path3 = '../../Database/output/D/complete'
        Output_dir3 = output_fdir(Output_path3)
    if args.output4 is not None:
        Output_dir4 = output_fdir(args.output4)
    else:
        Output_path4 = '../../Database/output/D/empty'
        Output_dir4 = output_fdir(Output_path4)
    if args.output5 is not None:
        Output_dir5 = output_fdir(args.output5)
    else:
        Output_path5 = '../../Database/output/D/enough'
        Output_dir5 = output_fdir(Output_path5)
    if args.output6 is not None:
        Output_dir6 = output_fdir(args.output6)
    else:
        Output_path6 = '../../Database/output/D/not_enough'
        Output_dir6 = output_fdir(Output_path6)
    if args.output7 is not None:
        Output_dir7 = output_fdir(args.output7)
    else:
        Output_path7 = '../../Database/output/D/less'
        Output_dir7 = output_fdir(Output_path7)
    if args.output8 is not None:
        Output_dir8 = output_fdir(args.output8)
    else:
        Output_path8 = '../../Database/output/D/more'
        Output_dir8 = output_fdir(Output_path8)
    if args.output9 is not None:
        Output_dir9 = output_fdir(args.output9)
    else:
        Output_path9 = '../../Database/output/D/no_lat_lon'
        Output_dir9 = output_fdir(Output_path9)
    if args.output10 is not None:
        Output_dir10 = output_fdir(args.output10)
    else:
        Output_path10 = '../../Database/output/All_Files'
        Output_dir10 = output_fdir(Output_path10)
elif os.path.exists("G2F data preprocessing/Environment/output/G2F Separating"):
    Input_dir = "G2F data preprocessing/Environment/output/G2F Separating"
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
        Output_path1 = 'Database/output/D/output'
        Output_dir1 = output_fdir(Output_path1)
    if args.output2 is not None:
        Output_dir2 = output_fdir(args.output2)
    else:
        Output_path2 = 'Database/output/D/plots'
        Output_dir2 = output_fdir(Output_path2)
    if args.output3 is not None:
        Output_dir3 = output_fdir(args.output3)
    else:
        Output_path3 = 'Database/output/D/complete'
        Output_dir3 = output_fdir(Output_path3)
    if args.output4 is not None:
        Output_dir4 = output_fdir(args.output4)
    else:
        Output_path4 = 'Database/output/D/empty'
        Output_dir4 = output_fdir(Output_path4)
    if args.output5 is not None:
        Output_dir5 = output_fdir(args.output5)
    else:
        Output_path5 = 'Database/output/D/enough'
        Output_dir5 = output_fdir(Output_path5)
    if args.output6 is not None:
        Output_dir6 = output_fdir(args.output6)
    else:
        Output_path6 = 'Database/output/D/not_enough'
        Output_dir6 = output_fdir(Output_path6)
    if args.output7 is not None:
        Output_dir7 = output_fdir(args.output7)
    else:
        Output_path7 = 'Database/output/D/less'
        Output_dir7 = output_fdir(Output_path7)
    if args.output8 is not None:
        Output_dir8 = output_fdir(args.output8)
    else:
        Output_path8 = 'Database/output/D/more'
        Output_dir8 = output_fdir(Output_path8)
    if args.output9 is not None:
        Output_dir9 = output_fdir(args.output9)
    else:
        Output_path9 = 'Database/output/D/no_lat_lon'
        Output_dir9 = output_fdir(Output_path9)
    if args.output10 is not None:
        Output_dir10 = output_fdir(args.output10)
    else:
        Output_path10 = 'Database/output/All_Files'
        Output_dir10 = output_fdir(Output_path10)
elif os.path.exists("../G2F data preprocessing/Environment/output/G2F Separating"):
    Input_dir = "../G2F data preprocessing/Environment/output/G2F Separating"
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
        Output_path1 = '../Database/output/D/output'
        Output_dir1 = output_fdir(Output_path1)
    if args.output2 is not None:
        Output_dir2 = output_fdir(args.output2)
    else:
        Output_path2 = '../Database/output/D/plots'
        Output_dir2 = output_fdir(Output_path2)
    if args.output3 is not None:
        Output_dir3 = output_fdir(args.output3)
    else:
        Output_path3 = '../Database/output/D/complete'
        Output_dir3 = output_fdir(Output_path3)
    if args.output4 is not None:
        Output_dir4 = output_fdir(args.output4)
    else:
        Output_path4 = '../Database/output/D/empty'
        Output_dir4 = output_fdir(Output_path4)
    if args.output5 is not None:
        Output_dir5 = output_fdir(args.output5)
    else:
        Output_path5 = '../Database/output/D/enough'
        Output_dir5 = output_fdir(Output_path5)
    if args.output6 is not None:
        Output_dir6 = output_fdir(args.output6)
    else:
        Output_path6 = '../Database/output/D/not_enough'
        Output_dir6 = output_fdir(Output_path6)
    if args.output7 is not None:
        Output_dir7 = output_fdir(args.output7)
    else:
        Output_path7 = '../Database/output/D/less'
        Output_dir7 = output_fdir(Output_path7)
    if args.output8 is not None:
        Output_dir8 = output_fdir(args.output8)
    else:
        Output_path8 = '../Database/output/D/more'
        Output_dir8 = output_fdir(Output_path8)
    if args.output9 is not None:
        Output_dir9 = output_fdir(args.output9)
    else:
        Output_path9 = '../Database/output/D/no_lat_lon'
        Output_dir9 = output_fdir(Output_path9)
    if args.output10 is not None:
        Output_dir10 = output_fdir(args.output10)
    else:
        Output_path10 = '../Database/output/All_Files'
        Output_dir10 = output_fdir(Output_path10)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print("Input directory = ", Input_dir)
print ("Output directory = ", Output_dir1)
        
# =============================================================================
# Creating dataframes
# =============================================================================
for root, dirs, files in os.walk (Output_dir8):
    for file in files:
        os.remove (os.path.join (root, file))
        
G2F_files = glob.glob(os.path.abspath(os.path.join(Input_dir, '*.csv')))

SC1 = glob.glob(os.path.abspath(os.path.join(Input_dir1, '*.csv')))
SC2 = glob.glob(os.path.abspath(os.path.join(Input_dir2, '*.csv')))
SC3 = glob.glob(os.path.abspath(os.path.join(Input_dir3, '*.csv')))

# =============================================================================
# Dew Point
Abb = "D"
variable = "Dew Point [C]"
for filename in G2F_files:
    if os.path.basename(filename)[0] == Abb:
        G2F = pd.read_csv (filename)
        dfs = [G2F]
        
        for i in SC1:
            if os.path.basename(i) == os.path.basename(filename):
                
                data1 = pd.read_csv ( i, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
                data1.rename (columns = {variable:"NSRDB " + variable,
                                         "Min " + variable:"Min NSRDB " + variable,
                                         "Max " + variable:"Max NSRDB " + variable}, inplace = True)
                dfs.append (data1)
    
        for j in SC2:
            if os.path.basename(j) == os.path.basename(filename):
                
                data2 = pd.read_csv (j, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
                data2.rename (columns = {variable:"DayMet " + variable,
                                         "Min " + variable:"Min DayMet " + variable,
                                         "Max " + variable:"Max DayMet " + variable}, inplace = True)
    
                dfs.append (data2)
                
        for k in SC3:
            if os.path.basename(k) == os.path.basename(filename):
                                        
                data3 = pd.read_csv (k, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
                data3.rename (columns = {variable:"NWS " + variable,
                                         "Min " + variable:"Min NWS " + variable,
                                         "Max " + variable:"Max NWS " + variable}, inplace = True)      
                dfs.append (data3)
                    
                        
        df_merged = reduce (lambda left, right: pd.merge (left, right, on = ["Day of Year [Local]"], how = "inner"), dfs)
                            
        df_merged.to_csv (os.path.join(Output_dir1 ,os.path.basename(filename)), index = None)
  
# =============================================================================
# Performance Metrics
# =============================================================================
files = glob.glob(os.path.abspath(os.path.join(Output_dir1, '*.csv')))

Corr1_list = []
MAE1_list = []
MSE1_list = []
RMSE1_list = []

Corr2_list = []
MAE2_list = []
MSE2_list = []
RMSE2_list = []

Corr3_list = []
MAE3_list = []
MSE3_list = []
RMSE3_list = []


for file in files:
    df = pd.read_csv (file)
    No_of_Days = df.shape [0]
    No_of_Days_with_empty_data = df.iloc [:,1].isnull().sum()  
    
    if No_of_Days - No_of_Days_with_empty_data > 10:
        df.dropna(inplace = True, how = "any")
     
        if variable in df:
            y = df [variable]        
    
            CS = ["NSRDB ", "DayMet ", "NWS "]
            if CS [0] + variable in df:
                y1 = df[CS [0] + variable]
                    
                Corr1 = r2_score(y, y1)
                MAE1 = mean_absolute_error(y, y1)
                MSE1 = mean_squared_error(y, y1)
                RMSE1 = np.sqrt(MSE1)
                
                Corr1_list.append (Corr1)
                MAE1_list.append (MAE1)
                MSE1_list.append (MSE1)
                RMSE1_list.append (RMSE1)
                
            
            if CS [1] + variable in df:
                y2 = df[CS [1] + variable]
                    
                Corr2 = r2_score(y, y2)
                MAE2 = mean_absolute_error(y, y2)
                MSE2 = mean_squared_error(y, y2)
                RMSE2 = np.sqrt(MSE2)
                
                Corr2_list.append(Corr2)
                MAE2_list.append(MAE2)
                MSE2_list.append(MSE2)
                RMSE2_list.append(RMSE2)
                
                
            if CS[2] + variable in df:
                y3 = df[CS [2] + variable]
                    
                Corr3 = r2_score(y, y3)
                MAE3 = mean_absolute_error(y, y3)
                MSE3 = mean_squared_error(y, y3)
                RMSE3 = np.sqrt(MSE3)
                
                Corr3_list.append(Corr3)
                MAE3_list.append(MAE3)
                MSE3_list.append(MSE3)
                RMSE3_list.append(RMSE3)
                
df_performance = pd.DataFrame ({"Experiment": pd.Series (files),
                "Corr_NSRDB": pd.Series (Corr1_list), "MAE_NSRDB": pd.Series (MAE1_list), "MSE_NSRDB": pd.Series (MSE1_list), "RMSE_NSRDB": pd.Series (RMSE1_list),
                "Corr_DayMet": pd.Series (Corr2_list), "MAE_DayMet": pd.Series (MAE2_list), "MSE_DayMet": pd.Series (MSE2_list), "RMSE_DayMet": pd.Series (RMSE2_list),
                "Corr_NWS": pd.Series (Corr3_list), "MAE_NWS": pd.Series (MAE3_list), "MSE_NWS": pd.Series (MSE3_list), "RMSE_NWS": pd.Series (RMSE3_list)})

df_performance.to_csv(os.path.abspath(os.path.join(pathlib.Path(Output_dir1).parent, f"{Abb}_performance.csv")))

# =============================================================================
# Plotting PDFs of Performance Metrics
# =============================================================================
# Correlation
corr1 = sns.kdeplot (Corr1_list, label = "G2F-NSRDB", color = "mediumseagreen")
corr2 = sns.kdeplot (Corr2_list, label = "G2F-DayMet", color = "coral")
corr3 = sns.kdeplot (Corr3_list, label = "G2F-NWS", color = "cornflowerblue")
plt.xlabel ("Corr-DP")
plt.ylabel ("Density")
plt.legend () 
# plt.title ("Correlation")
plt.savefig (os.path.abspath(os.path.join(Output_dir2,  "0PDF Correlation.png")), dpi = 400)
plt.close ()
  
# MAE
MAE1 = sns.kdeplot (MAE1_list, label = "G2F-NSRDB", color = "mediumseagreen")
MAE2 = sns.kdeplot (MAE2_list, label = "G2F-DayMet", color = "coral")
MAE3 = sns.kdeplot (MAE3_list, label = "G2F-NWS", color = "cornflowerblue")
plt.xlabel ("MAE-DP")
plt.ylabel ("Density")
plt.legend () 
# plt.title ("MAE")
plt.savefig(os.path.abspath(os.path.join(Output_dir2, "0PDF Mean Absolute Error.png")), dpi = 400)
plt.close ()

# MSE
plt.style.use ("seaborn")  
sns.set (font_scale = 1.5)              
MSE1 = sns.kdeplot (MSE1_list, label = "G2F-NSRDB", color = "mediumseagreen")
MSE2 = sns.kdeplot (MSE2_list, label = "G2F-DayMet", color = "coral")
MSE3 = sns.kdeplot (MSE3_list, label = "G2F-NWS", color = "cornflowerblue")
plt.xlabel ("MSE-DP")
plt.ylabel ("Density")
plt.legend () 
# plt.title ("MSE")
plt.savefig (os.path.abspath(os.path.join(Output_dir2, "0PDF Mean Squared Error.png")), dpi = 400)
plt.close ()

# RMSE
RMSE1 = sns.kdeplot (RMSE1_list,  label = "G2F-NSRDB", color = "mediumseagreen")
RMSE2 = sns.kdeplot (RMSE2_list,  label = "G2F-DayMet", color = "coral")
RMSE3 = sns.kdeplot (RMSE3_list,  label = "G2F-NWS", color = "cornflowerblue")
plt.xlabel ("RMSE-DP")
plt.ylabel ("Density")
plt.legend () 
#plt.title ("RMSE")
plt.savefig(os.path.abspath(os.path.join(Output_dir2,"0PDF Root Mean Squared Error.png")), dpi = 400)
plt.close () 

# =============================================================================
# Variable Plots
# =============================================================================
Files = glob.glob(os.path.abspath(os.path.join(Output_dir1, '*.csv')))

for filename in Files:
    df = pd.read_csv (filename)
    
    if variable in df.columns:
        ax = df.plot.line (x = "Day of Year [Local]", y = variable, color = "black", label = "G2F" )
    
    if "NSRDB " + variable in df.columns:    
        df.plot.line (x = "Day of Year [Local]", y = "NSRDB " + variable, color = "mediumseagreen", label = "NSRDB", ax = ax)
        
    if "DayMet " + variable in df.columns:
        df.plot.line (x = "Day of Year [Local]", y = "DayMet " + variable, color = "coral", label = "DayMet", ax = ax)
        
    if "NWS " + variable in df.columns:
        df.plot.line (x = "Day of Year [Local]", y = "NWS " + variable, color = "cornflowerblue", label = "NWS", ax = ax)
        
    ax.set_xlabel ("Day of Year")
    ax.set_ylabel (variable)
    ax.set_title (os.path.basename(filename)[1:-4])
    plt.savefig (os.path.abspath(os.path.join(Output_dir2 , os.path.basename(filename)[:-4] + ".jpg")), bbox_inches = "tight", dpi = 600)
    plt.close () 

# =============================================================================
# Selected Dataframe
# =============================================================================
Complete = []
Empty = []
Missing = []
Missing_Enough = []
Missing_Not_Enough = []
Missing_Enough_less = []
Missing_Enough_ANN = []
No_lat_lon = []

files = glob.glob(os.path.abspath(os.path.join(Output_dir1, '*.csv')))
for file in files:
    df = pd.read_csv(file)
    
    days = df.shape[0]
    empty_cells = df [variable].isnull().sum()
    filled_cells = df [variable].notnull().sum()

# =============================================================================
# Complete     
# =============================================================================
    if empty_cells == 0:
        'Complete'
        Complete.append(os.path.basename(file))
        df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]]
        df_new.to_csv(os.path.abspath(os.path.join(Output_dir3 , os.path.basename(file))), index = None)

# =============================================================================
# Empty     
# =============================================================================  
    elif empty_cells == days:
        'Empty'
        Empty.append (os.path.basename(file))
        CS = ["NSRDB ", "DayMet ", "NWS "]
        if CS [0] + variable in df:
            df_new = df [["Day of Year [Local]", CS [0] + variable, "Min " + CS [0] + variable, "Max " + CS [0] + variable]]
            df_new.to_csv(os.path.abspath(os.path.join(Output_dir4 , os.path.basename(file))), index = None)
            
        elif CS [1] + variable in df:
            df_new = df [["Day of Year [Local]", CS [1] + variable, "Min " + CS [1] + variable, "Max " + CS [1] + variable]]
            df_new.to_csv(os.path.abspath(os.path.join(Output_dir4 , os.path.basename(file))), index = None)
                        
        elif CS [2] + variable in df:
            df_new = df [["Day of Year [Local]", CS [2] + variable, "Min " + CS [2] + variable, "Max " + CS [2] + variable]]
            df_new.to_csv(os.path.abspath(os.path.join(Output_dir4 , os.path.basename(file))), index = None)
                    
        else:
            No_lat_lon.append (os.path.basename(file))
            df.to_csv(os.path.abspath(os.path.join(Output_dir9 , os.path.basename(file))), index = None)

# =============================================================================
# Missing     
# =============================================================================             
    else:
        'Missing'
        Missing.append (os.path.basename(file))
        
        if empty_cells < 0.25*days:
            'Missing_Enough'
            Missing_Enough.append(os.path.basename(file))
            if empty_cells < 5:
                'Missing_Enough_Less'
                Missing_Enough_less.append(os.path.basename(file))
                df = pd.read_csv (file)
                df.dropna (inplace = True, how = "any")
                y = df [variable]
                RMSE_Selection = []
                CS = ["NSRDB ", "DayMet ", "NWS "]
                if CS [0] + variable in df:
                   y1 = df [CS [0] + variable]
                   MSE1 = mean_squared_error (y, y1)
                   RMSE1 = np.sqrt (MSE1)
                   RMSE_Selection.append (RMSE1)
                if CS [1] + variable in df:
                   y2 = df [CS [1] + variable]
                   MSE2 = mean_squared_error (y, y2)
                   RMSE2 = np.sqrt (MSE2)
                   RMSE_Selection.append (RMSE2)                    
                if CS [2] + variable in df:
                   y3 = df [CS [2] + variable]
                   MSE3 = mean_squared_error (y, y3)
                   RMSE3 = np.sqrt (MSE3)
                   RMSE_Selection.append (RMSE3)
                if len (RMSE_Selection) > 0:
                  Min_RMSE = min (RMSE_Selection)
                  if Min_RMSE == RMSE1:
                      'NSRDB'
                      df = pd.read_csv (file)
                      df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                      df_new [variable].fillna (df [CS [0] + variable], inplace = True)
                      df_new ["Min " + variable].fillna (df ["Min " + CS [0] + variable], inplace = True)
                      df_new ["Max " + variable].fillna (df ["Max " + CS [0] + variable], inplace = True)
                      df_new.to_csv (os.path.abspath(os.path.join(Output_dir7 , os.path.basename(file))), index = None)
                  if Min_RMSE == RMSE2:
                      'DayMet'
                      df = pd.read_csv (file)
                      df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                      df_new [variable].fillna (df [CS [1] + variable], inplace = True)
                      df_new ["Min " + variable].fillna (df ["Min " + CS [1] + variable], inplace = True)
                      df_new ["Max " + variable].fillna (df ["Max " + CS [1] + variable], inplace = True)
                      df_new.to_csv (os.path.abspath(os.path.join(Output_dir9 , os.path.basename(file))), index = None)
                  if Min_RMSE == RMSE3:
                      'NWS'
                      df = pd.read_csv (file)
                      df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                      df_new [variable].fillna (df [CS [2] + variable], inplace = True)
                      df_new ["Min " + variable].fillna (df ["Min " + CS [2] + variable], inplace = True)
                      df_new ["Max " + variable].fillna (df ["Max " + CS [2] + variable], inplace = True)
                      df_new.to_csv (os.path.abspath(os.path.join(Output_dir7 , os.path.basename(file))), index = None)
  
                else:
                   No_lat_lon.append (file)
                   df.to_csv(os.path.abspath(os.path.join(Output_dir9 , os.path.basename(file))), index = None)
              
            else:
                'Missing_Enough_ANN'
                Missing_Enough_ANN.append (os.path.basename(file))
                df = pd.read_csv (file)
                df.dropna (inplace = True, how = "any")
                y = df [variable]
                RMSE_Selection = []
                CS = ["NSRDB ", "DayMet ", "NWS "]
                if CS [0] + variable in df:
                    y1 = df [CS [0] + variable]
                    MSE1 = mean_squared_error (y, y1)
                    RMSE1 = np.sqrt (MSE1)
                    RMSE_Selection.append (RMSE1)
                if CS [1] + variable in df:
                    y2 = df [CS [1] + variable]
                    MSE2 = mean_squared_error (y, y2)
                    RMSE2 = np.sqrt (MSE2)
                    RMSE_Selection.append (RMSE2)
                if CS [2] + variable in df:
                    y3 = df [CS [2] + variable]
                    MSE3 = mean_squared_error (y, y3)
                    RMSE3 = np.sqrt (MSE3)
                    RMSE_Selection.append (RMSE3)
                if len (RMSE_Selection) > 0:
                    Min_RMSE = min (RMSE_Selection)
                    if Min_RMSE == RMSE1:
                        df_new = pd.read_csv (file, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable,
                                                                            CS [0] + variable, "Min " + CS [0] + variable, "Max " + CS [0] + variable])                            
                        df_new.to_csv (os.path.abspath(os.path.join(Output_dir8 , os.path.basename(file))), index = None)
                    if Min_RMSE == RMSE2:
                        df_new = pd.read_csv (file, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable,
                                                                            CS [1] + variable, "Min " + CS [1] + variable, "Max " + CS [1] + variable])
                        df_new.to_csv (os.path.abspath(os.path.join(Output_dir8 , os.path.basename(file))), index = None)
                    if Min_RMSE == RMSE3:
                        df_new = pd.read_csv (file, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable,
                                                                            CS [2] + variable, "Min " + CS [2] + variable, "Max " + CS [2] + variable]) 
                        df_new.to_csv (os.path.abspath(os.path.join(Output_dir8 , os.path.basename(file))), index = None)
   
                else:
                   No_lat_lon.append (file)
                   df.to_csv (os.path.abspath(os.path.join(Output_dir9 , os.path.basename(file))), index = None)
                     
            
        else:
            'Missing and not Enough'
            Missing_Not_Enough.append (os.path.basename(file))
            df = pd.read_csv (file)
            df.dropna (inplace = True, how = "any")
            y = df [variable]
            RMSE_Selection = []
            CS = ["NSRDB ", "DayMet ", "NWS "]
            if CS [0] + variable in df:
                y1 = df [CS [0] + variable]
                MSE1 = mean_squared_error (y, y1)
                RMSE1 = np.sqrt (MSE1)
                RMSE_Selection.append (RMSE1)
            if CS [1] + variable in df:
                y2 = df [CS [1] + variable]
                MSE2 = mean_squared_error (y, y2)
                RMSE2 = np.sqrt (MSE2)
                RMSE_Selection.append (RMSE2)
            if CS [2] + variable in df:
                y3 = df [CS [2] + variable]
                MSE3 = mean_squared_error (y, y3)
                RMSE3 = np.sqrt (MSE3)
                RMSE_Selection.append (RMSE3)
            if len (RMSE_Selection) > 0:
                Min_RMSE = min (RMSE_Selection)
                if Min_RMSE == RMSE1:
                    'NSRDB'
                    df = pd.read_csv (file)
                    df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                    df_new [variable].fillna (df [CS [0] + variable], inplace = True)
                    df_new ["Min " + variable].fillna (df ["Min " + CS [0] + variable], inplace = True)
                    df_new ["Max " + variable].fillna (df ["Max " + CS [0] + variable], inplace = True)
                    df_new.to_csv (os.path.abspath(os.path.join(Output_dir6 , os.path.basename(file))), index = None)
                if Min_RMSE == RMSE2:
                    'DayMet'
                    df = pd.read_csv (file)
                    df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                    df_new [variable].fillna (df [CS [1] + variable], inplace = True)
                    df_new ["Min " + variable].fillna (df ["Min " + CS [1] + variable], inplace = True)
                    df_new ["Max " + variable].fillna (df ["Max " + CS [1] + variable], inplace = True)
                    df_new.to_csv (os.path.abspath(os.path.join(Output_dir6 , os.path.basename(file))), index = None)
                if Min_RMSE == RMSE3:
                    'NWS'
                    df = pd.read_csv (file)
                    df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                    df_new [variable].fillna (df [CS [2] + variable], inplace = True)
                    df_new ["Min " + variable].fillna (df ["Min " + CS [2] + variable], inplace = True)
                    df_new ["Max " + variable].fillna (df ["Max " + CS [2] + variable], inplace = True)
                    df_new.to_csv (os.path.abspath(os.path.join(Output_dir6 , os.path.basename(file))), index = None)
                        
            else:                    
                No_lat_lon.append (os.path.basename(file))
                df.to_csv (os.path.abspath(os.path.join(Output_dir9 , os.path.basename(file))), index = None)
                    
                            
#print ("Complete =", len(Complete),
#       "Empty = ", len(Empty), 
#       "Missing =", len(Missing), 
#       "Enough =", len(Missing_Enough), 
#       "Not Enough =", len(Missing_Not_Enough),
#       "Less =", len(Missing_Enough_less),
#       "ANN =", len (Missing_Enough_ANN),
#       "No lat lon =", len (No_lat_lon))

for file in glob.glob(os.path.abspath(os.path.join(Output_dir3, '*.csv'))):
    df = pd.read_csv (file)
    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
    df.to_csv (os.path.abspath(os.path.join(Output_dir10 , os.path.basename(file))), index = None)
    
for file in glob.glob(os.path.abspath(os.path.join(Output_dir4, '*.csv'))):
    df = pd.read_csv (file)
    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
    df.to_csv (os.path.abspath(os.path.join(Output_dir10 , os.path.basename(file))), index = None)

for file in glob.glob(os.path.abspath(os.path.join(Output_dir6, '*.csv'))):
    df = pd.read_csv (file)
    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
    df.to_csv (os.path.abspath(os.path.join(Output_dir10 , os.path.basename(file))), index = None)
    
for file in glob.glob(os.path.abspath(os.path.join(Output_dir7, '*.csv'))):
    df = pd.read_csv (file)
    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
    df.to_csv (os.path.abspath(os.path.join(Output_dir10 , os.path.basename(file))), index = None)

#for file in os.listdir (Output_dir8):
#    df = pd.read_csv (Output_dir8 + file)
#    df.drop ([df.columns [4], df.columns [5], df.columns [6]], axis = "columns", inplace = True)
#    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
#    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
#    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
#    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
#    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
#    df.to_csv (Output_dir10 + file, index = None)

for file in glob.glob(os.path.abspath(os.path.join(Output_dir9, '*.csv'))):
    df = pd.read_csv (file)
    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
    df.to_csv (os.path.abspath(os.path.join(Output_dir10 , os.path.basename(file))), index = None)

# =============================================================================
# Check
# =============================================================================
#List1 = os.listdir (Output_dir1)
#List2 = os.listdir (Output_dir10)
#check = all (item in List2 for item in List1)
#if check is False:
#    for file in List1:
#        if file not in List2:
#            copyfile (Output_dir1 + file, Output_dir10 + file)
        
            
    