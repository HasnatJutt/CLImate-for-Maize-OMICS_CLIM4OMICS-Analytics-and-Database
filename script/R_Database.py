# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 09:12:58 2020

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

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../../G2F data preprocessing/Environment/output/G2F Separating/")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"

Input_dir1 = os.chdir ("../../../../APIs/NSRDB/output/NSRDB/")
Input_dir1 = os.getcwd ().replace ("\\", "/")
Input_dir1 = Input_dir1 + "/"

Input_dir2 = os.chdir ("../../../DayMet/output/DayMet/")
Input_dir2 = os.getcwd ().replace ("\\", "/")
Input_dir2 = Input_dir2 + "/"

Input_dir3 = os.chdir ("../../../NWS/output/NWS/")
Input_dir3 = os.getcwd ().replace ("\\", "/")
Input_dir3 = Input_dir3 + "/"

Output_dir1 = os.chdir ("../../../../Database/output/R/output/")
Output_dir1 = os.getcwd ().replace ("\\", "/")
Output_dir1 = Output_dir1 + "/"

Output_dir2 = os.chdir ("../plots")
Output_dir2 = os.getcwd ().replace ("\\", "/")
Output_dir2 = Output_dir2 + "/"

Output_dir3 = os.chdir ("../complete")
Output_dir3 = os.getcwd ().replace ("\\", "/")
Output_dir3 = Output_dir3 + "/"

Output_dir4 = os.chdir ("../empty")
Output_dir4 = os.getcwd ().replace ("\\", "/")
Output_dir4 = Output_dir4 + "/"

# Output_dir5 = os.chdir ("../enough")
# Output_dir5 = os.getcwd ().replace ("\\", "/")
# Output_dir5 = Output_dir5 + "/"

Output_dir6 = os.chdir ("../not_enough")
Output_dir6 = os.getcwd ().replace ("\\", "/")
Output_dir6 = Output_dir6 + "/"

Output_dir7 = os.chdir ("../less")
Output_dir7 = os.getcwd ().replace ("\\", "/")
Output_dir7 = Output_dir7 + "/"

Output_dir8 = os.chdir ("../more")
Output_dir8 = os.getcwd ().replace ("\\", "/")
Output_dir8 = Output_dir8 + "/"

Output_dir9 = os.chdir ("../no_lat_lon")
Output_dir9 = os.getcwd ().replace ("\\", "/")
Output_dir9 = Output_dir9 + "/"

Output_dir10 = os.chdir ("../../All_Files")
Output_dir10 = os.getcwd ().replace ("\\", "/")
Output_dir10 = Output_dir10 + "/"

print("Input directory = ", Input_dir)
print ("Output directory = ", Output_dir1)
        
# =============================================================================
# Creating dataframes
# =============================================================================
for root, dirs, files in os.walk (Output_dir8):
    for file in files:
        os.remove (os.path.join (root, file))
        
G2F_files = os.listdir (Input_dir)

SC1 = os.listdir (Input_dir1)
SC2 = os.listdir (Input_dir2)
SC3 = os.listdir (Input_dir3)

# =============================================================================
# Rainfall
Abb = "R"
variable = "Rainfall [mm]"
for filename in G2F_files:
    if filename [0] == Abb:
        G2F = pd.read_csv (Input_dir + filename)
        dfs = [G2F]
        
        for i in SC1:
            if i == filename:
                
                data1 = pd.read_csv (Input_dir1 + i, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
                data1.rename (columns = {variable:"NSRDB " + variable,
                                         "Min " + variable:"Min NSRDB " + variable,
                                         "Max " + variable:"Max NSRDB " + variable}, inplace = True)
                dfs.append (data1)
    
        for j in SC2:
            if j == filename:
                
                data2 = pd.read_csv (Input_dir2 + j, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
                data2.rename (columns = {variable:"DayMet " + variable,
                                         "Min " + variable:"Min DayMet " + variable,
                                         "Max " + variable:"Max DayMet " + variable}, inplace = True)
    
                dfs.append (data2)
                
        for k in SC3:
            if k == filename:
                                        
                data3 = pd.read_csv (Input_dir3 + k, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable])
                data3.rename (columns = {variable:"NWS " + variable,
                                         "Min " + variable:"Min NWS " + variable,
                                         "Max " + variable:"Max NWS " + variable}, inplace = True)      
                dfs.append (data3)
                    
                        
        df_merged = reduce (lambda left, right: pd.merge (left, right, on = ["Day of Year [Local]"], how = "inner"), dfs)
                            
        df_merged.to_csv (Output_dir1 + filename, index = None) 
  
# =============================================================================
# Performance Metrics
# =============================================================================
files = os.listdir (Output_dir1)

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
    df = pd.read_csv (Output_dir1 + file)
    No_of_Days = df.shape [0]
    No_of_Days_with_empty_data = df.iloc [:,1].isnull().sum()  
    
    if No_of_Days - No_of_Days_with_empty_data > 10:
        df.dropna (inplace = True, how = "any")
     
        if variable in df:
            y = df [variable]        
    
            CS = ["NSRDB ", "DayMet ", "NWS "]
            if CS [0] + variable in df:
                y1 = df [CS [0] + variable]
                    
                Corr1 = r2_score (y, y1)
                MAE1 = mean_absolute_error (y, y1)
                MSE1 = mean_squared_error (y, y1)
                RMSE1 = np.sqrt (MSE1)
                
                Corr1_list.append (Corr1)
                MAE1_list.append (MAE1)
                MSE1_list.append (MSE1)
                RMSE1_list.append (RMSE1)
                
            
            if CS [1] + variable in df:
                y2 = df [CS [1] + variable]
                    
                Corr2 = r2_score (y, y2)
                MAE2 = mean_absolute_error (y, y2)
                MSE2 = mean_squared_error (y, y2)
                RMSE2 = np.sqrt (MSE2)
                
                Corr2_list.append (Corr2)
                MAE2_list.append (MAE2)
                MSE2_list.append (MSE2)
                RMSE2_list.append (RMSE2)
                
                
            if CS [2] + variable in df:
                y3 = df [CS [2] + variable]
                    
                Corr3 = r2_score (y, y3)
                MAE3 = mean_absolute_error (y, y3)
                MSE3 = mean_squared_error (y, y3)
                RMSE3 = np.sqrt (MSE3)
                
                Corr3_list.append (Corr3)
                MAE3_list.append (MAE3)
                MSE3_list.append (MSE3)
                RMSE3_list.append (RMSE3)
                
df_performance = pd.DataFrame ({"Experiment": pd.Series (files),
                "Corr_NSRDB": pd.Series (Corr1_list), "MAE_NSRDB": pd.Series (MAE1_list), "MSE_NSRDB": pd.Series (MSE1_list), "RMSE_NSRDB": pd.Series (RMSE1_list),
                "Corr_DayMet": pd.Series (Corr2_list), "MAE_DayMet": pd.Series (MAE2_list), "MSE_DayMet": pd.Series (MSE2_list), "RMSE_DayMet": pd.Series (RMSE2_list),
                "Corr_NWS": pd.Series (Corr3_list), "MAE_NWS": pd.Series (MAE3_list), "MSE_NWS": pd.Series (MSE3_list), "RMSE_NWS": pd.Series (RMSE3_list)})

path = os.chdir ("../" + Abb)
df_performance.to_csv (Abb + "_" + "performance.csv")
            
# =============================================================================
# Plotting PDFs of Performance Metrics
# =============================================================================
# Correlation
corr1 = sns.displot (Corr1_list, label = "G2F-NSRDB", color = "mediumseagreen")
corr2 = sns.displot (Corr2_list, label = "G2F-DayMet", color = "coral")
corr3 = sns.displot (Corr3_list, label = "G2F-NWS", color = "cornflowerblue")
plt.xlabel ("Corr-R")
plt.ylabel ("Density")
plt.legend () 
# plt.title ("Correlation")
plt.savefig (Output_dir2 + "0PDF " + "Correlation" + ".png", dpi = 400) 
plt.close ()
  
# MAE
MAE1 = sns.displot (MAE1_list, label = "G2F-NSRDB", color = "mediumseagreen")
MAE2 = sns.displot (MAE2_list, label = "DayMet", color = "coral")
MAE3 = sns.displot (MAE3_list, label = "NWS", color = "cornflowerblue")
plt.xlabel ("MAE-R")
plt.ylabel ("Density")
plt.legend () 
# plt.title ("MAE")
plt.savefig (Output_dir2 + "0PDF " + "Mean Absolute Error" + ".png", dpi = 400) 
plt.close ()

# MSE
plt.style.use ("seaborn")
sns.set (font_scale = 1.5)
MSE1 = sns.displot (MSE1_list, label = "G2F-NSRDB", color = "mediumseagreen")
MSE2 = sns.displot (MSE2_list, label = "G2F-DayMet", color = "coral")
MSE3 = sns.displot (MSE3_list, label = "G2F-NWS", color = "cornflowerblue")
plt.xlabel ("MSE-R")
plt.ylabel ("Density")
plt.legend () 
# plt.title ("MSE")
plt.savefig (Output_dir2 + "0PDF " + "Mean Squared Error" + ".png", dpi = 400) 
plt.close ()

# RMSE
RMSE1 = sns.displot (RMSE1_list,  label = "G2F-NSRDB", color = "mediumseagreen")
RMSE2 = sns.displot (RMSE2_list,  label = "G2F-DayMet", color = "coral")
RMSE3 = sns.displot (RMSE3_list,  label = "G2F-NWS", color = "cornflowerblue")
plt.xlabel ("RMSE-R")
plt.ylabel ("Density")
plt.legend () 
#plt.title ("RMSE")
plt.savefig (Output_dir2 + "0PDF " + "Root Mean Squared Error" + ".png", dpi = 400) 
plt.close () 

# =============================================================================
# Variable Plots
# =============================================================================
Files = os.listdir (Output_dir1)

for filename in Files:
    df = pd.read_csv (Output_dir1 + filename)
    
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
    ax.set_title (filename [1:-4])
    plt.savefig (Output_dir2 + filename [:-4] + ".jpg", bbox_inches = "tight", dpi = 600)
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

files = os.listdir (Output_dir1)
for file in files:
    df = pd.read_csv (Output_dir1 + file)
    
    days = df.shape [0]
    empty_cells = df [variable].isnull().sum()
    filled_cells = df [variable].notnull().sum()

# =============================================================================
# Complete     
# =============================================================================
    if empty_cells == 0:
        'Complete'
        Complete.append (file)
        df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]]
        df_new.to_csv (Output_dir3 + file, index = None)

# =============================================================================
# Empty     
# =============================================================================  
    elif empty_cells == days:
        'Empty'
        Empty.append (file)
        CS = ["NSRDB ", "DayMet ", "NWS "]
        if CS [0] + variable in df:
            df_new = df [["Day of Year [Local]", CS [0] + variable, "Min " + CS [0] + variable, "Max " + CS [0] + variable]]
            df_new.to_csv (Output_dir4 + file, index = None)
            
        elif CS [1] + variable in df:
            df_new = df [["Day of Year [Local]", CS [1] + variable, "Min " + CS [1] + variable, "Max " + CS [1] + variable]]
            df_new.to_csv (Output_dir4 + file, index = None)
                        
        elif CS [2] + variable in df:
            df_new = df [["Day of Year [Local]", CS [2] + variable, "Min " + CS [2] + variable, "Max " + CS [2] + variable]]
            df_new.to_csv (Output_dir4 + file, index = None)
                    
        else:
            No_lat_lon.append (file)
            df.to_csv (Output_dir9 + file, index = None)

# =============================================================================
# Missing     
# =============================================================================             
    else:
        'Missing'
        Missing.append (file)
        
        if empty_cells < 0.25*days:
            'Missing_Enough'
            Missing_Enough.append (file)
            if empty_cells < 5:
                'Missing_Enough_Less'
                Missing_Enough_less.append (file)
                df = pd.read_csv (Output_dir1 + file)
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
                      df = pd.read_csv (Output_dir1 + file)
                      df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                      df_new [variable].fillna (df [CS [0] + variable], inplace = True)
                      df_new ["Min " + variable].fillna (df ["Min " + CS [0] + variable], inplace = True)
                      df_new ["Max " + variable].fillna (df ["Max " + CS [0] + variable], inplace = True)
                      df_new.to_csv (Output_dir7 + file, index = None)
                  if Min_RMSE == RMSE2:
                      'DayMet'
                      df = pd.read_csv (Output_dir1 + file)
                      df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                      df_new [variable].fillna (df [CS [1] + variable], inplace = True)
                      df_new ["Min " + variable].fillna (df ["Min " + CS [1] + variable], inplace = True)
                      df_new ["Max " + variable].fillna (df ["Max " + CS [1] + variable], inplace = True)
                      df_new.to_csv (Output_dir7 + file, index = None)
                  if Min_RMSE == RMSE3:
                      'NWS'
                      df = pd.read_csv (Output_dir1 + file)
                      df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                      df_new [variable].fillna (df [CS [2] + variable], inplace = True)
                      df_new ["Min " + variable].fillna (df ["Min " + CS [2] + variable], inplace = True)
                      df_new ["Max " + variable].fillna (df ["Max " + CS [2] + variable], inplace = True)
                      df_new.to_csv (Output_dir7 + file, index = None)
  
                else:
                   No_lat_lon.append (file)
                   df.to_csv (Output_dir9 + file, index = None)
              
            else:
                'Missing_Enough_ANN'
                Missing_Enough_ANN.append (file)
                df = pd.read_csv (Output_dir1 + file)
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
                        df_new = pd.read_csv (Output_dir1 + file, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable,
                                                                            CS [0] + variable, "Min " + CS [0] + variable, "Max " + CS [0] + variable])                            
                        df_new.to_csv (Output_dir8 + file, index = None)
                    if Min_RMSE == RMSE2:
                        df_new = pd.read_csv (Output_dir1 + file, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable,
                                                                            CS [1] + variable, "Min " + CS [1] + variable, "Max " + CS [1] + variable])
                        df_new.to_csv (Output_dir8 + file, index = None)
                    if Min_RMSE == RMSE3:
                        df_new = pd.read_csv (Output_dir1 + file, usecols = ["Day of Year [Local]", variable, "Min " + variable, "Max " + variable,
                                                                            CS [2] + variable, "Min " + CS [2] + variable, "Max " + CS [2] + variable]) 
                        df_new.to_csv (Output_dir8 + file, index = None)
   
                else:
                   No_lat_lon.append (file)
                   df.to_csv (Output_dir9 + file, index = None)
                     
            
        else:
            'Missing and not Enough'
            Missing_Not_Enough.append (file)
            df = pd.read_csv (Output_dir1 + file)
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
                    df = pd.read_csv (Output_dir1 + file)
                    df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                    df_new [variable].fillna (df [CS [0] + variable], inplace = True)
                    df_new ["Min " + variable].fillna (df ["Min " + CS [0] + variable], inplace = True)
                    df_new ["Max " + variable].fillna (df ["Max " + CS [0] + variable], inplace = True)
                    df_new.to_csv (Output_dir6 + file, index = None)
                if Min_RMSE == RMSE2:
                    'DayMet'
                    df = pd.read_csv (Output_dir1 + file)
                    df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                    df_new [variable].fillna (df [CS [1] + variable], inplace = True)
                    df_new ["Min " + variable].fillna (df ["Min " + CS [1] + variable], inplace = True)
                    df_new ["Max " + variable].fillna (df ["Max " + CS [1] + variable], inplace = True)
                    df_new.to_csv (Output_dir6 + file, index = None)
                if Min_RMSE == RMSE3:
                    'NWS'
                    df = pd.read_csv (Output_dir1 + file)
                    df_new = df [["Day of Year [Local]", variable, "Min " + variable, "Max " + variable]].copy ()
                    df_new [variable].fillna (df [CS [2] + variable], inplace = True)
                    df_new ["Min " + variable].fillna (df ["Min " + CS [2] + variable], inplace = True)
                    df_new ["Max " + variable].fillna (df ["Max " + CS [2] + variable], inplace = True)
                    df_new.to_csv (Output_dir6 + file, index = None)
                        
            else:                    
                No_lat_lon.append (file)
                df.to_csv (Output_dir9 + file, index = None)
                    
                            
#print ("Complete =", len(Complete),
#       "Empty = ", len(Empty), 
#       "Missing =", len(Missing), 
#       "Enough =", len(Missing_Enough), 
#       "Not Enough =", len(Missing_Not_Enough),
#       "Less =", len(Missing_Enough_less),
#       "ANN =", len (Missing_Enough_ANN),
#       "No lat lon =", len (No_lat_lon))

for file in os.listdir (Output_dir3):
    df = pd.read_csv (Output_dir3 + file)
    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
#    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
    df = df [["Day", Abb + "M", Abb + "M_Day"]]
    df.to_csv (Output_dir10 + file, index = None)
    
for file in os.listdir (Output_dir4):
    df = pd.read_csv (Output_dir4 + file)
    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
#    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
    df = df [["Day", Abb + "M", Abb + "M_Day"]]
    df.to_csv (Output_dir10 + file, index = None)

for file in os.listdir (Output_dir6):
    df = pd.read_csv (Output_dir6 + file)
    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
#    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
    df = df [["Day", Abb + "M", Abb + "M_Day"]]
    df.to_csv (Output_dir10 + file, index = None)
    
for file in os.listdir (Output_dir7):
    df = pd.read_csv (Output_dir7 + file)
    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
#    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
    df = df [["Day", Abb + "M", Abb + "M_Day"]]
    df.to_csv (Output_dir10 + file, index = None)

#for file in os.listdir (Output_dir8):
#    df = pd.read_csv (Output_dir8 + file)
#    df.drop ([df.columns [4], df.columns [5], df.columns [6]], axis = "columns", inplace = True)
#    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
#    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
#    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
#    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
##    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
#    df = df [["Day", Abb + "M", Abb + "M_Day"]]
#    df.to_csv (Output_dir10 + file, index = None)

for file in os.listdir (Output_dir9):
    df = pd.read_csv (Output_dir9 + file)
    df.columns = ["Day", Abb + "M", Abb + "I", Abb + "A"]
    df [Abb + "M_Day"] = Abb + "M" + df ["Day"].astype (str)
    df [Abb + "I_Day"] = Abb + "I" + df ["Day"].astype (str)
    df [Abb + "A_Day"] = Abb + "A" + df ["Day"].astype (str)
#    df = df [["Day", Abb + "I", Abb + "I_Day", Abb + "M", Abb + "M_Day", Abb + "A", Abb + "A_Day"]]
    df = df [["Day", Abb + "M", Abb + "M_Day"]]
    df.to_csv (Output_dir10 + file, index = None)

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
        
            
    