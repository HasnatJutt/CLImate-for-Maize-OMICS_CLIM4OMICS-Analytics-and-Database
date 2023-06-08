# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 11:40:36 2022

@author: psarzaeim2
"""

## Reading data from data sources  
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd
import numpy as np
from functools import reduce
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import math

# =============================================================================
# Input and Output directories
# =============================================================================
Input_dir1 = os.chdir ("../../APIs/NSRDB/output/NSRDB/")
Input_dir1 = os.getcwd ().replace ("\\", "/")
Input_dir1 = Input_dir1 + "/"

Input_dir2 = os.chdir ("../../../DayMet/output/DayMet/")
Input_dir2 = os.getcwd ().replace ("\\", "/")
Input_dir2 = Input_dir2 + "/"

Input_dir3 = os.chdir ("../../../NWS/output/NWS/")
Input_dir3 = os.getcwd ().replace ("\\", "/")
Input_dir3 = Input_dir3 + "/"

Output_dir4 = os.chdir ("../../../../Database/output/All_Files")
Output_dir4 = os.getcwd ().replace ("\\", "/")
Output_dir4 = Output_dir4 + "/"

Output_dir1 = os.chdir ("../Uncertainty/")
Output_dir1 = os.getcwd ().replace ("\\", "/")
Output_dir1 = Output_dir1 + "/"

# =============================================================================
# Creating dataframes
# =============================================================================
SC1 = os.listdir (Input_dir1)
SC2 = os.listdir (Input_dir2)
SC3 = os.listdir (Input_dir3)

Abb = "I"
variable = "Wind Direction [degrees]"
files = os.listdir (Output_dir4)
for file in files:
    if file [0] == Abb:
        df = pd.read_csv (Output_dir4 + file)
        df.rename(columns={'Day': 'Day of Year [Local]'}, inplace=True)
        dfs = [df]
        
        for i in SC1:
            if i == file:
                
                data1 = pd.read_csv (Input_dir1 + i, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
                data1.rename (columns = {variable:"NSRDB " + variable,
                                          "Min " + variable:"Min NSRDB " + variable,
                                          "Max " + variable:"Max NSRDB " + variable}, inplace = True)
                dfs.append (data1)
    
        # for j in SC2:
        #     if j == file:
                
        #         data2 = pd.read_csv (Input_dir2 + j, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
        #         data2.rename (columns = {variable:"DayMet " + variable,
        #                                   "Min " + variable:"Min DayMet " + variable,
        #                                   "Max " + variable:"Max DayMet " + variable}, inplace = True)
        #         dfs.append (data2)
                
        for k in SC3:
            if k == file:
                                        
                data3 = pd.read_csv (Input_dir3 + k, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
                data3.rename (columns = {variable:"NWS " + variable,
                                          "Min " + variable:"Min NWS " + variable,
                                          "Max " + variable:"Max NWS " + variable}, inplace = True)      
                dfs.append (data3)
                    
                        
        df_merged = reduce (lambda left, right: pd.merge (left, right, on = ["Day of Year [Local]"], how = "inner"), dfs)
                            
        df_merged.to_csv (Output_dir1 + file, index = None) 
        
# =============================================================================
# Error
# =============================================================================
Err1_list = []
Err2_list = []
Err3_list = []

files = os.listdir (Output_dir1)
for file in files:
    if file [0] == Abb:
        df = pd.read_csv (Output_dir1 + file)
        
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

    df.to_csv (Output_dir1 + file, index = None)
    
Err1_list_flat = [item for sublist in Err1_list for item in sublist] 
# Err2_list_flat = [item for sublist in Err2_list for item in sublist]
Err3_list_flat = [item for sublist in Err3_list for item in sublist]  
    
# =============================================================================
# Plotting PDFs of Errors
# =============================================================================
Err1 = sns.displot (Err1_list_flat, label = "G2F-NSRDB", color = "mediumseagreen")
Err1_list_flat = [x for x in Err1_list_flat if math.isnan(x) == False]
SD_1 = statistics.pstdev (Err1_list_flat)
plt.text (-350, 0.0097, '$SD_{G2F-NSRDB}$' + " = " + str (round (SD_1, 2)), fontsize = 10) 

# Err2 = sns.displot (Err2_list_flat, label = "G2F-DayMet", color = "coral")
# SD_2 = statistics.pstdev (Err2_list_flat)
# plt.text (-1500, 0.176, '$SD_{G2F-DayMet}$' + " = " + str (round (SD_2, 2)), fontsize = 10)

Err3 = sns.displot (Err3_list_flat, label = "G2F-NWS", color = "cornflowerblue")
Err3_list_flat = [x for x in Err3_list_flat if math.isnan(x) == False]
SD_3 = statistics.pstdev (Err3_list_flat)
plt.text (-350, 0.0090, '$SD_{G2F-NWS}$' + " = " + str (round (SD_3, 2)), fontsize = 10)

plt.xlabel ("Err-I")
plt.ylabel ("Density")
plt.legend () 
#plt.title ("Error")
plt.xticks(fontsize = 10)
plt.legend (fontsize = 8)

Output_dir2 = os.chdir ("../" + Abb + "/uncertainty_plots")
Output_dir2 = os.getcwd ().replace ("\\", "/")
Output_dir2 = Output_dir2 + "/"

plt.savefig (Output_dir2 + "PDF " + "Error" + ".png", dpi = 400) 
plt.close ()