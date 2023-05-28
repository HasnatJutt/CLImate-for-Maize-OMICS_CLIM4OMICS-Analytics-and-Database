# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 12:07:22 2021

@author: psarzaeim2
"""

# Creating Wall.csv file based on selection
# =============================================================================
# Import necessary libraries
# =============================================================================
import os, re, os.path
import pandas as pd
import numpy as np
from functools import reduce
import glob
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../../Database/output/All_Files/")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
path = os.chdir ("../../../G2F data preprocessing/Meta/output/")
Input_dir1 = os.getcwd ().replace ("\\", "/")
Input_dir1 = Input_dir1 + "/"
Output_dir = os.chdir ("../../../Selection/output/Selected_Files/")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"

print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
    
# =============================================================================    
# Selection of Variables, Experiments, and period of Time
# =============================================================================
# Option (1)###################################################################
# Selection by Filtering
for root, dirs, files in os.walk (Output_dir):
    for file in files:
        os.remove (os.path.join (root, file))
        
files = os.listdir (Input_dir)
all_files = []
for file in files:
    'H means Hybrid Experiments'
    if file [7] == "H":
        all_files.append (file)
        all_files = pd.Series (all_files).drop_duplicates ().tolist ()


# Select the desired variables; "T" as Temperature, "D" as Dew Point, "H" as Relative Humidity, "S" as Solar Radiation, 
# "R" as Rainfall, "W" as Wind Speed, "I" as Wind Direction, "P" as Pressure, "C" as Precipitable Water.
all_variables = []
for file in all_files:
    variable = file [0]
    all_variables.append (variable)
    all_variables = pd.Series (all_variables).drop_duplicates ().tolist ()
print ("Variable Options: ", all_variables)                                    
selected_variables = ["T", "D", "H", "S", "R", "W", "I"]                        # Variable Options
# selected_variables = ["T"]                                                    # User
print ("Selected Variables: ", selected_variables) 

selection_V = []    
for file in all_files:
    for i in selected_variables:
        if file [0] == i:
            selection_V.append (file)
#print(selection_V)
Options_Y = []
for file in selection_V:
    Y = file [1:5]
    Options_Y.append (Y)
    Options_Y = pd.Series (Options_Y).drop_duplicates ().tolist ()
print ("Year Options = ", Options_Y)                                            
selected_years = ["2014", "2015", "2016", "2017"]                               # Year Options
# selected_years = ["2014", "2015", "2016"]                                     # User
print ("Selected Years: ", selected_years)

selection_Y = []
for file in selection_V:
    for j in selected_years:
        if file [1:5] == j:
            selection_Y.append (file)
#print (selection_Y)
Options_S = []
for file in selection_Y:
    S = file [5:7]
    Options_S.append (S)
    Options_S = pd.Series (Options_S).drop_duplicates ().tolist ()
print ("State Options = ", Options_S)                                           
selected_states = ['DE', 'GA', 'IA', 'IL', 'IN', 'MN', 'MO', 'NC', 'NE', 'NY',
                   'ON', 'TX', 'WI', 'KS', 'OH', 'AR', 'MI', 'CO', 'SC']        # State Options
# selected_states = ['DE', 'GA', 'IA', 'IL', 'IN', 'MN', 'MO', 'NC']            # User
print ("Selected States: ", selected_states)

selection_S = []
for file in selection_Y:
    for k in selected_states:
        if file [5:7] == k:
            selection_S.append (file)
#print (selection_S)
Options_E = []
for file in selection_S:
    E = file [7:9]
    Options_E.append (E)
    Options_E = pd.Series (Options_E).drop_duplicates ().tolist ()
print ("Experiment Options = ", Options_E)                                      
selected_experiments = ["H1", "H2", "H3", "H4"]                                 # Experiment Options
# selected_experiments = ["H1", "H2", "H3", "H4"]                               # User
print ("Selected Experiments: ", selected_experiments)

selection_E = []
for file in selection_S:
    for l in selected_experiments:
        if file [7:9] == l:
            selection_E.append (file)
#print (selection_E)

Selected_files = selection_E           
length = []
for file in selection_E:
    df = pd.read_csv (Input_dir + file)
    days = len (df ["Day"].tolist ())
    length.append (days)

#print ("Selected file(s): ", Selected_files)
print ("No. of selected experiment(s): ", len(Selected_files)/len(selected_variables))
Range = min (length)
print ("Available Range Days = 1 -", Range)

# Select the desired start and end day in the growing season.
start_day = 1                                                                   # User
#end_day = 80 # end_day should not be lager than Range.                          # User (or Range)
end_day = Range
print ("Start day = ", start_day, ", End day = ", end_day)

# =============================================================================
# Creating file for each experiment
# =============================================================================
for f in Selected_files:
    lst = [f[1:] for f in Selected_files]
Experiments = list (dict.fromkeys (lst))

merge_list = []
read_list = []
for Exp in Experiments:
    for f in Selected_files:
        if f[1:] == Exp:
            merge_list.append (f)
            
    for i in merge_list:
        df = pd.read_csv (Input_dir + i)
        df.drop (["Day"], axis = 1)
        read_list.append (df)
        merge = reduce (lambda left,right: pd.merge(left, right, on = ["Day"], how = "outer"), read_list)
    merge.to_csv (Output_dir + Exp, index = None)
    
    read_list = []
    merge_list = []

# =============================================================================
# Creating Matrix and Wall.csv file
# =============================================================================
Experiments = os.listdir (Output_dir)
for exp in Experiments:
    df = pd.read_csv (Output_dir + exp)
    No_of_Days = df ["Day"].count ()
    
    # Convert to matrix
    Matrix1 = df.values
    # Extract the data in the desired time span
    Matrix2 = Matrix1 [start_day:end_day, 1:]   
    # Transpose the desired data
    Matrix3 = Matrix2.transpose ()
    # Create a matrix for "day" data
    Matrix4 = Matrix3 [::2]   
    Matrix5 = Matrix4.reshape (1, -1)
    # Create a matrix for variable measurements data  
    Matrix6 = Matrix3 [1::2]
    Matrix7 = Matrix6.reshape (1, -1)
    # Concatenate the matrix5 and matrix7 
    Matrix_Final = np.concatenate ((Matrix7, Matrix5), axis = 0)
    data = pd.DataFrame (Matrix_Final, index = ["Day", str(exp) [:-4]])
    data.to_csv (Output_dir + exp)


os.chdir (Output_dir)
extension = "csv"
all_filenames = [i for i in glob.glob ("*.{}".format (extension))]
combined_csv = pd.concat ([pd.read_csv (f) for f in all_filenames], sort = False)
combined_csv.rename (columns = {"Unnamed: 0":"Experiment"}, inplace = True)
indexnames = combined_csv [combined_csv ["Experiment"] == "Day"].index
combined_csv ["Experiment"] = combined_csv ["Experiment"].str [:-4] + "_" + combined_csv ["Experiment"].str [4:]
combined_csv.drop (indexnames, inplace = True)
combined_csv.to_csv (Output_dir + "Wall.csv", index = False, encoding = "utf-8-sig")

Wall_transpose = combined_csv.set_index ("Experiment").T
Wall_transpose.to_csv (Output_dir + "Wall.Transpose.csv", index = False, encoding = "utf-8-sig")