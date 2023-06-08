# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 08:42:25 2019

@author: psarzaeim2
"""

## Creating Pivot Tables for G2F Environmental Data
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd
import numpy as np

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../output/Name Fixing")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../G2F Separating")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"

print ("Input directory = ", Input_dir)
print ("Output directory = ", Output_dir)

# =============================================================================   
# Control
# ============================================================================= 
path = os.chdir ("../../../Meta/output")
Input_dir1 = os.getcwd ().replace ("\\", "/")
Input_dir1 = Input_dir1 + "/" 
path = os.chdir ("../../Phenotype/output")
Input_dir2 = os.getcwd ().replace ("\\", "/")
Input_dir2 = Input_dir2 + "/" 

Env_list = []
Env_Experiments = os.listdir (Input_dir)
for file in Env_Experiments:
    file = file [:-4]
    Env_list.append (file)
# print (Env_list)

Meta = pd.read_csv (Input_dir1 + "0lat_lon.csv")
Meta_list = Meta ["Experiment_ID"].tolist ()

Pheno = pd.read_csv (Input_dir2 + "0YP1P2.csv")
Pheno_list = Pheno ["Experiment_ID"].tolist ()

#Y = pd.read_csv (Input_dir2 + "Y.csv")
#Y_list = Y ["Experiment_ID"].tolist ()

#Shared = list (set (Env_list) & set (Meta_list) & set (Pheno_list) & set (Y_list))
Shared = list (set (Env_list) & set (Meta_list) & set (Pheno_list))
print("Number of Hybrid Experiments = ", len(Shared))

# Controlled Files
for filename in os.listdir (Input_dir):
    if filename [:-4] not in (Shared):
        os.remove (Input_dir + filename)

Meta_new = Meta [Meta ["Experiment_ID"].isin (Shared)]
Meta_new.to_csv (Input_dir1 + "lat_lon.csv", index = None)

Pheno_new = Pheno [Pheno ["Experiment_ID"].isin (Shared)]
Pheno_new.drop (["Experiment_ID"], axis = 1, inplace = True)
Pheno_new.to_csv (Input_dir2 + "YP1P2.csv", index = None)

# Y_new = Y [Y ["Experiment_ID"].isin (Shared)]
# Y_new.drop (["Experiment_ID"], axis = 1, inplace = True)
# Y_new.to_csv (Input_dir2 + "Y.csv", index = None)

# =============================================================================
# Reading each experiment file as data frame
# =============================================================================
for filename in os.listdir (Input_dir):
    if filename [6] == "H":
    #    print(filename)
    #    print (Output_dir + filename)
        df = pd.read_csv (Input_dir + filename)
        
    #    print ("The experiment has {0} rows and {1} columns".format (df.shape [0],
    #           df.shape [1]))
    #    
    #    print ("Are there missing values? {}".format(df.isnull().any().any()))
        
# =============================================================================
# Creating pivot tables for each variable in each experiment
# =============================================================================
        "Temperature pivot table"
        Temperature = df.pivot_table ("Temperature [C]", index = ["Day of Year [Local]"], dropna = False) 
        Temperature ["Min Temperature [C]"] = df.pivot_table ("Temperature [C]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False) 
        Temperature ["Max Temperature [C]"] = df.pivot_table ("Temperature [C]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
        
        MAX = Temperature.index.max()
        MIN = Temperature.index.min()
        lst = list (range (MIN, MAX + 1))
        Df = pd.DataFrame (lst)
        Df.rename (columns = {Df.columns [0]: "Day of Year [Local]"}, inplace = True)
        
        common = Temperature.merge (Df, how = "outer", on = ["Day of Year [Local]"])
        common.sort_values (by = "Day of Year [Local]", inplace = True)  
    
        common.to_csv (Output_dir + "T" + filename, index = None)
        
# =============================================================================    
        "Dew Point pivot table"
        Dew_Point = df.pivot_table ("Dew Point [C]", index = ["Day of Year [Local]"], dropna = False)
        Dew_Point ["Min Dew Point [C]"] = df.pivot_table ("Dew Point [C]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False) 
        Dew_Point ["Max Dew Point [C]"] = df.pivot_table ("Dew Point [C]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
    
        MAX = Dew_Point.index.max()
        MIN = Dew_Point.index.min()
        lst = list (range (MIN, MAX + 1))
        Df = pd.DataFrame (lst)
        Df.rename (columns = {Df.columns [0]: "Day of Year [Local]"}, inplace = True)
        
        common = Dew_Point.merge (Df, how = "outer", on = ["Day of Year [Local]"])
        common.sort_values (by = "Day of Year [Local]", inplace = True)  
    
        common.to_csv (Output_dir + "D" + filename, index = None)
    
# =============================================================================       
        "Relative Humidity pivot table"
        Relative_Humidity = df.pivot_table ("Relative Humidity [%]", index = ["Day of Year [Local]"], dropna = False)
        Relative_Humidity ["Min Relative Humidity [%]"] = df.pivot_table ("Relative Humidity [%]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False) 
        Relative_Humidity ["Max Relative Humidity [%]"] = df.pivot_table ("Relative Humidity [%]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False) 
    
        MAX = Relative_Humidity.index.max()
        MIN = Relative_Humidity.index.min()
        lst = list (range (MIN, MAX + 1))
        Df = pd.DataFrame (lst)
        Df.rename (columns = {Df.columns [0]: "Day of Year [Local]"}, inplace = True)
        
        common = Relative_Humidity.merge (Df, how = "outer", on = ["Day of Year [Local]"])
        common.sort_values (by = "Day of Year [Local]", inplace = True)  
    
        common.to_csv (Output_dir + "H" + filename, index = None)
        
# =============================================================================   
        "Solar Radiation pivot table"
        Solar_Radiation = df.pivot_table ("Solar Radiation [W/m2]", index = ["Day of Year [Local]"], dropna = False)
        Solar_Radiation ["Min Solar Radiation [W/m2]"] = df.pivot_table ("Solar Radiation [W/m2]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False) 
        Solar_Radiation ["Max Solar Radiation [W/m2]"] = df.pivot_table ("Solar Radiation [W/m2]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False) 
        
        MAX = Solar_Radiation.index.max()
        MIN = Solar_Radiation.index.min()
        lst = list (range (MIN, MAX + 1))
        Df = pd.DataFrame (lst)
        Df.rename (columns = {Df.columns [0]: "Day of Year [Local]"}, inplace = True)
        
        common = Solar_Radiation.merge (Df, how = "outer", on = ["Day of Year [Local]"])
        common.sort_values (by = "Day of Year [Local]", inplace = True)  
    
        common.to_csv (Output_dir + "S" + filename, index = None)
    
# =============================================================================      
        "Rainfall pivot table"
        Rainfall_G = df.groupby ("Day of Year [Local]")["Rainfall [mm]"].sum(min_count = 1)
        Rainfall = Rainfall_G.to_frame ()
        Rainfall ["Min Rainfall [mm]"] = df.pivot_table ("Rainfall [mm]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)
        Rainfall ["Max Rainfall [mm]"] = df.pivot_table ("Rainfall [mm]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
        
        MAX = Rainfall.index.max()
        MIN = Rainfall.index.min()
        lst = list (range (MIN, MAX + 1))
        Df = pd.DataFrame (lst)
        Df.rename (columns = {Df.columns [0]: "Day of Year [Local]"}, inplace = True)
        
        common = Rainfall.merge (Df, how = "outer", on = ["Day of Year [Local]"])
        common.sort_values (by = "Day of Year [Local]", inplace = True)  
    
        common.to_csv (Output_dir + "R" + filename, index = None)
        
# =============================================================================    
        "Wind Speed pivot table"
        Wind_Speed = df.pivot_table ("Wind Speed [m/s]", index = ["Day of Year [Local]"], dropna = False)
        Wind_Speed ["Min Wind Speed [m/s]"] = df.pivot_table ("Wind Speed [m/s]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)
        Wind_Speed ["Max Wind Speed [m/s]"] = df.pivot_table ("Wind Speed [m/s]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
    
        MAX = Wind_Speed.index.max()
        MIN = Wind_Speed.index.min()
        lst = list (range (MIN, MAX + 1))
        Df = pd.DataFrame (lst)
        Df.rename (columns = {Df.columns [0]: "Day of Year [Local]"}, inplace = True)
        
        common_W = Wind_Speed.merge (Df, how = "outer", on = ["Day of Year [Local]"])
        common_W.sort_values (by = "Day of Year [Local]", inplace = True)  
    
        common_W.to_csv (Output_dir + "W" + filename, index = None)
        
# =============================================================================        
        "Wind Direction pivot table"
    #    df.drop (df[df["Wind Direction [degrees]"] == "No Wind"].index, inplace = True)
        Wind_Direction = df.pivot_table ("Wind Direction [degrees]", index = ["Day of Year [Local]"], aggfunc = np.mean, dropna = False)
        Wind_Direction ["Min Wind Direction [degrees]"] = df.pivot_table ("Wind Direction [degrees]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)  
        Wind_Direction ["Max Wind Direction [degrees]"] = df.pivot_table ("Wind Direction [degrees]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
        
        MAX = Wind_Direction.index.max()
        MIN = Wind_Direction.index.min()
        lst = list (range (MIN, MAX + 1))
        Df = pd.DataFrame (lst)
        Df.rename (columns = {Df.columns [0]: "Day of Year [Local]"}, inplace = True)
        
        common_I = Wind_Direction.merge (Df, how = "outer", on = ["Day of Year [Local]"])
        common_I.sort_values (by = "Day of Year [Local]", inplace = True)  
    
        common_I.to_csv (Output_dir + "I" + filename, index = None)
        
# =============================================================================       
        "Wind Gust pivot table"
        Wind_Gust = df.pivot_table ("Wind Gust [m/s]", index = ["Day of Year [Local]"], dropna = False)
        Wind_Gust ["Min Wind Gust [m/s]"] = df.pivot_table ("Wind Gust [m/s]", index = ["Day of Year [Local]"], aggfunc = "min", dropna = False)  
        Wind_Gust ["Max Wind Gust [m/s]"] = df.pivot_table ("Wind Gust [m/s]", index = ["Day of Year [Local]"], aggfunc = "max", dropna = False)
        
        MAX = Wind_Gust.index.max()
        MIN = Wind_Gust.index.min()
        lst = list (range (MIN, MAX + 1))
        Df = pd.DataFrame (lst)
        Df.rename (columns = {Df.columns [0]: "Day of Year [Local]"}, inplace = True)
        
        common = Wind_Gust.merge (Df, how = "outer", on = ["Day of Year [Local]"])
        common.sort_values (by = "Day of Year [Local]", inplace = True)  
    
        common.to_csv (Output_dir + "G" + filename, index = None)
        
