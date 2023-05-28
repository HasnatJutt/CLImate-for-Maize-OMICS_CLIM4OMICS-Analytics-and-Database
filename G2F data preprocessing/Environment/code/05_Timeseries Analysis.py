# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:58:43 2020

@author: psarzaeim2, Hasnat

Updated on May 2023 
"""

## Ploting the Piecharts to Show the Portions of "Complete", "Empty", and "Incomplete" Datasets for each Variable   
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
import pathlib
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
            Output_path = os.path.join(Input_path,'../../../G2F data preprocessing/Environment/output/Timeseries Analysis')
            Output_dir = output_fdir(Output_path)
    else:
        print(f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../G2F data preprocessing/Environment/output/G2F Separating"):
    Input_dir = "../../../G2F data preprocessing/Environment/output/G2F Separating"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../G2F data preprocessing/Environment/output/Timeseries Analysis'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("G2F data preprocessing/Environment/output/G2F Separating"):
    Input_dir = "G2F data preprocessing/Environment/output/G2F Separating"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'G2F data preprocessing/Environment/output/Timeseries Analysis'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("../G2F data preprocessing/Environment/output/G2F Separating"):
    Input_dir = "../G2F data preprocessing/Environment/output/G2F Separating"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../G2F data preprocessing/Environment/output/Timeseries Analysis'
        Output_dir = output_fdir(Output_path)
else:
    print("No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

    
# =============================================================================
# Creating dataframes
# =============================================================================
# Temperature
files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))

Complete_T = []
Missing_T = []
Empty_T = []

for file in files:
    if os.path.basename(file)[0] == "T":
            df = pd.read_csv (file, index_col = "Day of Year [Local]")
            
            No_of_Days = df.shape [0]
            No_of_Days_with_empty_data = df.iloc [:,1].isnull().sum()
        
            if No_of_Days_with_empty_data == No_of_Days:
                Empty_T.append (file)
            elif No_of_Days_with_empty_data == 0:
                Complete_T.append (file)
            else:
                Missing_T.append (file)
                
Complete_T = len (Complete_T)
Missing_T = len (Missing_T)
Empty_T = len (Empty_T)

print ("T_complete = ", Complete_T)
print ("T_missing = ", Missing_T)
print ("T_empty = ", Empty_T)

#Plotting 
#plt.style.use ("ggplot")
plt.style.use ("seaborn")
sns.set (font_scale = 1.5)
labels = "Complete", "Missing", "Empty"
sizes = [Complete_T, Missing_T, Empty_T]
plt.pie (sizes, labels = labels, startangle = 90, autopct = "%1.1f%%")
plt.get_cmap ("copper")
plt.title ("Temperature")
plt.savefig (os.path.abspath(os.path.join(Output_dir ,"Temperature.jpg")), bbox_inches = "tight", dpi = 400)
plt.close ()

# =============================================================================
# Dew Point

Complete_D = []
Missing_D = []
Empty_D = []

for file in files:
    if os.path.basename(file)[0] == "D":
            df = pd.read_csv (file, index_col = "Day of Year [Local]")
            
            No_of_Days = df.shape [0]
            No_of_Days_with_empty_data = df.iloc [:,1].isnull().sum()
        
            if No_of_Days_with_empty_data == No_of_Days:
                Empty_D.append (file)
            elif No_of_Days_with_empty_data == 0:
                Complete_D.append (file)
            else:
                Missing_D.append (file)
                
Complete_D = len (Complete_D)
Missing_D = len (Missing_D)
Empty_D = len (Empty_D)

print ("D_complete = ", Complete_D)
print ("D_missing = ", Missing_D)
print ("D_empty = ", Empty_D)

#Plotting 
labels = "Complete", "Missing", "Empty"
sizes = [Complete_D, Missing_D, Empty_D]
plt.pie (sizes, labels = labels, startangle = 90, autopct = "%1.1f%%")
plt.title ("Dew Point")
plt.savefig (os.path.abspath(os.path.join(Output_dir ,"Dew Point.jpg")), bbox_inches = "tight", dpi = 400)
plt.close ()

# =============================================================================
# Relative Humidity

Complete_H = []
Missing_H = []
Empty_H = []

for file in files:
    if os.path.basename(file)[0] == "H":
            df = pd.read_csv (file, index_col = "Day of Year [Local]")
            
            No_of_Days = df.shape [0]
            No_of_Days_with_empty_data = df.iloc [:,1].isnull().sum()
        
            if No_of_Days_with_empty_data == No_of_Days:
                Empty_H.append (file)
            elif No_of_Days_with_empty_data == 0:
                Complete_H.append (file)
            else:
                Missing_H.append (file)
                
Complete_H = len (Complete_H)
Missing_H = len (Missing_H)
Empty_H = len (Empty_H)

print ("H_complete = ", Complete_H)
print ("H_missing = ", Missing_H)
print ("H_empty = ", Empty_H)

#Plotting 
labels = "Complete", "Missing", "Empty"
sizes = [Complete_H, Missing_H, Empty_H]
plt.pie (sizes, labels = labels, startangle = 90, autopct = "%1.1f%%")
plt.title ("Relative Humidity")
plt.savefig (os.path.abspath(os.path.join(Output_dir ,"Relative Humidity.jpg")), bbox_inches = "tight", dpi = 400)
plt.close ()

# =============================================================================    
# Solar Radiation

Complete_S = []
Missing_S = []
Empty_S = []

for file in files:
    if os.path.basename(file)[0] == "S":
            df = pd.read_csv (file, index_col = "Day of Year [Local]")
            
            No_of_Days = df.shape [0]
            No_of_Days_with_empty_data = df.iloc [:,1].isnull().sum()
        
            if No_of_Days_with_empty_data == No_of_Days:
                Empty_S.append (file)
            elif No_of_Days_with_empty_data == 0:
                Complete_S.append (file)
            else:
                Missing_S.append (file)
                
Complete_S = len (Complete_S)
Missing_S = len (Missing_S)
Empty_S = len (Empty_S)

print ("S_complete = ", Complete_S)
print ("S_missing = ", Missing_S)
print ("S_empty = ", Empty_S)

#Plotting 
labels = "Complete", "Missing", "Empty"
sizes = [Complete_S, Missing_S, Empty_S]
plt.pie (sizes, labels = labels, startangle = 90, autopct = "%1.1f%%")
plt.title ("Solar Radiation")
plt.savefig (os.path.abspath(os.path.join(Output_dir ,"Solar Radiation.jpg")), bbox_inches = "tight", dpi = 400)
plt.close ()

# =============================================================================    
# Rainfall

Complete_R = []
Missing_R = []
Empty_R = []

for file in files:
    if os.path.basename(file)[0] == "R":
            df = pd.read_csv (file, index_col = "Day of Year [Local]")
            
            No_of_Days = df.shape [0]
            No_of_Days_with_empty_data = df.iloc [:,1].isnull().sum()
        
            if No_of_Days_with_empty_data == No_of_Days:
                Empty_R.append (file)
            elif No_of_Days_with_empty_data == 0:
                Complete_R.append (file)
            else:
                Missing_R.append (file)
                
Complete_R = len (Complete_R)
Missing_R = len (Missing_R)
Empty_R = len (Empty_R)

print ("R_complete = ", Complete_R)
print ("R_missing = ", Missing_R)
print ("R_empty = ", Empty_R)

#Plotting 
labels = "Complete", "Missing", "Empty"
sizes = [Complete_R, Missing_R, Empty_R]
plt.pie (sizes, labels = labels, startangle = 90, autopct = "%1.1f%%")
plt.title ("Rainfall")
plt.savefig (os.path.abspath(os.path.join(Output_dir ,"Rainfall.jpg")), bbox_inches = "tight", dpi = 400)
plt.close ()

# =============================================================================    
# Wind Speed

Complete_W = []
Missing_W = []
Empty_W = []

for file in files:
    if os.path.basename(file)[0] == "W":
            df = pd.read_csv ( file, index_col = "Day of Year [Local]")
            
            No_of_Days = df.shape [0]
            No_of_Days_with_empty_data = df.iloc [:,1].isnull().sum()
        
            if No_of_Days_with_empty_data == No_of_Days:
                Empty_W.append (file)
            elif No_of_Days_with_empty_data == 0:
                Complete_W.append (file)
            else:
                Missing_W.append (file)
                
Complete_W = len (Complete_W)
Missing_W = len (Missing_W)
Empty_W = len (Empty_W)

print ("W_complete = ", Complete_W)
print ("W_missing = ", Missing_W)
print ("W_empty = ", Empty_W)

#Plotting 
labels = "Complete", "Missing", "Empty"
sizes = [Complete_W, Missing_W, Empty_W]
plt.pie (sizes, labels = labels, startangle = 90, autopct = "%1.1f%%")
plt.title ("Wind Speed")
plt.savefig (os.path.abspath(os.path.join(Output_dir ,"Wind Speed.jpg")), bbox_inches = "tight", dpi = 400)
plt.close ()

# =============================================================================    
# Wind Direction

Complete_I = []
Missing_I = []
Empty_I = []

for file in files:
    if os.path.basename(file)[0] == "I":
            df = pd.read_csv (file, index_col = "Day of Year [Local]")
            for file1 in files:
                if os.path.basename(file1)[0] == "W":
                    df1 = pd.read_csv (file1, index_col = "Day of Year [Local]")
                    if os.path.basename(file)[1:] == os.path.basename(file1)[1:]:
                        data = df.merge (df1, how = "outer", on = ["Day of Year [Local]"])
                        data.loc [(data ["Wind Speed [m/s]"] == 0) & (data ["Wind Direction [degrees]"].isnull ()), "Wind Direction [degrees]"] = 'No_Wind'
                        data.loc [(data ["Wind Speed [m/s]"] == 0) & (data ["Min Wind Direction [degrees]"].isnull ()), "Min Wind Direction [degrees]"] = 'No_Wind'
                        data.loc [(data ["Wind Speed [m/s]"] == 0) & (data ["Max Wind Direction [degrees]"].isnull ()), "Max Wind Direction [degrees]"] = 'No_Wind'
                        
                        data = data [["Wind Direction [degrees]", "Min Wind Direction [degrees]", "Max Wind Direction [degrees]"]]
    
                        data.to_csv (os.path.join(Input_dir,os.path.basename(file)))
            
                        No_of_Days = data.shape [0]
                        No_of_Days_with_empty_data = data.iloc [:,1].isnull().sum()
        
                        if No_of_Days_with_empty_data == No_of_Days:
                            Empty_I.append (file)
                        elif No_of_Days_with_empty_data == 0:
                            Complete_I.append (file)
                        else:
                            Missing_I.append (file)
                
Complete_I = len (Complete_I)
Missing_I = len (Missing_I)
Empty_I = len (Empty_I)

print ("I_complete = ", Complete_I)
print ("I_missing = ", Missing_I)
print ("I_empty = ", Empty_I)

#Plotting 
labels = "Complete", "Missing", "Empty"
sizes = [Complete_I, Missing_I, Empty_I]
plt.pie (sizes, labels = labels, startangle = 90, autopct = "%1.1f%%")
plt.title ("Wind Direction")
plt.savefig (os.path.abspath(os.path.join(Output_dir ,"Wind Direction.jpg")), bbox_inches = "tight", dpi = 400)
plt.close ()

# =============================================================================    
# Wind Gust

Complete_G = []
Missing_G = []
Empty_G = []

for file in files:
    if os.path.basename(file)[0] == "G":
            df = pd.read_csv (file, index_col = "Day of Year [Local]")
            No_of_Days = df.shape [0]
            No_of_Days_with_empty_data = df.iloc [:,1].isnull().sum()
        
            if No_of_Days_with_empty_data == No_of_Days:
                Empty_G.append (file)
            elif No_of_Days_with_empty_data == 0:
                Complete_G.append (file)
            else:
                Missing_G.append (file)
                
Complete_G = len (Complete_G)
Missing_G = len (Missing_G)
Empty_G = len (Empty_G)

print ("G_complete = ", Complete_G)
print ("G_missing = ", Missing_G)
print ("G_empty = ", Empty_G)

#Plotting 
labels = "Complete", "Missing", "Empty"
sizes = [Complete_G, Missing_G, Empty_G]
plt.pie (sizes, labels = labels, startangle = 90, autopct = "%1.1f%%")
plt.title ("Wind Gust")
plt.savefig (os.path.abspath(os.path.join(Output_dir ,"Wind Gust.jpg")), bbox_inches = "tight", dpi = 400)
plt.close ()

# =============================================================================  