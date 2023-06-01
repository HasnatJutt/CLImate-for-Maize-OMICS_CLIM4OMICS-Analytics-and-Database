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
import sys
import argparse
import pathlib
import numpy as np
from functools import reduce
import glob
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# Input and Output directories
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory from Current Path', required=False)
parser.add_argument('-o', '--output', help='Path of Output Directory from Current Path', required=False)
parser.add_argument('-m', '--meta', help='Path of Meta Files Input Directory1 from Current Path', required=False)
parser.add_argument('-y', '--years', help='Selected Years to process data in the form of list', required=False)
parser.add_argument('-v', '--var', help='Selected Variales to process data in the form of list', required=False)
parser.add_argument('-s', '--state', help='Selected States to process data in the form of list', required=False)
parser.add_argument('-e', '--experiment', help='Selected Experiment to process data in the form of list', required=False)
parser.add_argument('-sd', '--startday', help='Selected Start Day to process data in the form of list', required=False)
parser.add_argument('-ed', '--endday', help='Selected End Day to process data in the form of list', required=False)
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
            Output_path = os.path.join(Input_path, '../../Selection/output/Selected_Files')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../Database/output/All_Files"):
    Input_dir = "../../Database/output/All_Files"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../Selection/output/Selected_Files'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("Database/output/All_Files"):
    Input_dir = "Database/output/All_Files"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'Selection/output/Selected_Files'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../Database/output/All_Files"):
    Input_dir = "../Database/output/All_Files"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../Selection/output/Selected_Files'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()
print("Input directory = ", Input_dir)
print("Output directory ", Output_dir)

if args.meta is not None:
    Input_path1 = os.path.abspath(args.meta)
    if os.path.exists(Input_path1):
        Input_dir1 = Input_path1
    else:
        print(
            f'The input directory {args.meta} does not exists on system path. Correct the Input directory, provided directory has {Input_path1} path')

elif os.path.exists("../../G2F data preprocessing/Meta/output"):
    Input_dir1 = "../../G2F data preprocessing/Meta/output"

elif os.path.exists("G2F data preprocessing/Meta/output"):
    Input_dir1 = "G2F data preprocessing/Meta/output"

elif os.path.exists("../G2F data preprocessing/Meta/output"):
    Input_dir1 = "../G2F data preprocessing/Meta/output"
elif os.path.exists("../G2F data preprocessing/Meta/output"):
    Input_dir1 = "../G2F data preprocessing/Meta/output"
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()
# =============================================================================    
# Selection of Variables, Experiments, and period of Time
# =============================================================================
# Option (1)###################################################################
# Selection by Filtering
files = glob.glob(os.path.abspath(os.path.join(Output_dir, '*.csv')))
for file in files:
    os.remove(file)
        
files = glob.glob(os.path.abspath(os.path.join(Output_dir, '*.csv')))
all_files = []
for filename in files:
    file = os.path.basename(filename)
#    H means Hybrid Experiments
    if file[7] == "H":
        all_files.append(file)
        all_files = pd.Series(all_files).drop_duplicates().tolist()


# Select the desired variables; "T" as Temperature, "D" as Dew Point, "H" as Relative Humidity, "S" as Solar Radiation, 
# "R" as Rainfall, "W" as Wind Speed, "I" as Wind Direction, "P" as Pressure, "C" as Precipitable Water.
all_variables = []
for file in all_files:
    variable = file[0]
    all_variables.append (variable)
    all_variables = pd.Series(all_variables).drop_duplicates().tolist()
print ("Variable Options: ", all_variables)
if args.var is not None:
    selected_variables = args.var
    if type(selected_variables) == list:
        pass
    else:
        selected_variables = list(set(list(selected_variables)))
else:
    if len(all_variables) > 0:
        selected_variables = all_variables
        # selected_variables = ["T", "D", "H", "S", "R", "W", "I"]
    else:
        print("Files in Input directory do not have any variable")
                          # Variable Options
# selected_variables = ["T"]                                                    # User
print ("Selected Variables: ", selected_variables) 

selection_V = []    
for file in all_files:
    for i in selected_variables:
        if file[0] == i:
            selection_V.append(file)
#print(selection_V)
Options_Y = []
for file in selection_V:
    Y = file[1:5]
    Options_Y.append (Y)
    Options_Y = pd.Series(Options_Y).drop_duplicates().tolist()
print ("Year Options = ", Options_Y)
if args.years is not None:
    selected_years = args.years
    if type(selected_years) == list:
        pass
    else:
        selected_years = list(set(list(selected_years)))
else:
    if len(Options_Y) > 1:
        selected_years = Options_Y                              # Year Options
    else:
        print("Files in Input directory do not have any files")
# selected_years = ["2014", "2015", "2016"]                                     # User
print ("Selected Years: ", selected_years)

selection_Y = []
for file in selection_V:
    for j in selected_years:
        if file[1:5] == j:
            selection_Y.append(file)
#print (selection_Y)
Options_S = []
for file in selection_Y:
    S = file[5:7]
    Options_S.append(S)
    Options_S = pd.Series(Options_S).drop_duplicates().tolist()
print ("State Options = ", Options_S)
if args.state is not None:
    selected_states = args.state
    if type(selected_states) == list:
        pass
    else:
        selected_states = list(set(list(selected_states)))
else:
    if len(Options_S) > 0:
        selected_states = Options_S
    else:
        print("Files in Input directory do not have any files")
# selected_states = ['DE', 'GA', 'IA', 'IL', 'IN', 'MN', 'MO', 'NC', 'NE', 'NY',
#                    'ON', 'TX', 'WI', 'KS', 'OH', 'AR', 'MI', 'CO', 'SC']        # State Options
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
if args.experiment is not None:
    selected_experiments = args.experiment
    if type(selected_experiments) == list:
        pass
    else:
        selected_experiments = list(set(list(selected_experiments)))
else:
    if len(Options_E) > 0:
        selected_experiments = Options_E
    else:
        print("Files in Input directory do not have any files")
#selected_experiments = ["H1", "H2", "H3", "H4"]                                 # Experiment Options
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
if args.startday is not None:
    start_day = args.startday
    start_day = int(start_day)
else:
    start_day = 1                                                                   # User
#end_day = 80 # end_day should not be lager than Range.                          # User (or Range)
if args.endday is not None:
    end_day = args.endday
    end_day = int(end_day)
else:
    if Range is not None:
        end_day = Range
    else:
        print("No End day is provided")

print ("Start day = ", start_day, ", End day = ", end_day)

# =============================================================================
# Creating file for each experiment
# =============================================================================
for f in Selected_files:
    lst = [f[1:] for f in Selected_files]
Experiments = list(dict.fromkeys(lst))

merge_list = []
read_list = []
for Exp in Experiments:
    for f in Selected_files:
        if f[1:] == Exp:
            merge_list.append(f)
            
    for i in merge_list:
        df = pd.read_csv(os.path.join(Input_dir, i))
        df.drop (["Day"], axis = 1)
        read_list.append (df)
        merge = reduce (lambda left,right: pd.merge(left, right, on = ["Day"], how = "outer"), read_list)
    merge.to_csv(os.path.join(Output_dir, Exp), index = None)
    
    read_list = []
    merge_list = []

# =============================================================================
# Creating Matrix and Wall.csv file
# =============================================================================
Experiments = glob.glob(os.path.abspath(os.path.join(Output_dir, '*.csv')))
for exp in Experiments:
    df = pd.read_csv(exp)
    No_of_Days = df["Day"].count()
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
    data = pd.DataFrame(Matrix_Final, index = ["Day", str(exp) [:-4]])
    data.to_csv(exp)

all_filenames = glob.glob(os.path.abspath(os.path.join(Output_dir, '*.csv')))
combined_csv = pd.concat ([pd.read_csv (f) for f in all_filenames], sort = False)
combined_csv.rename (columns = {"Unnamed: 0":"Experiment"}, inplace = True)
indexnames = combined_csv [combined_csv ["Experiment"] == "Day"].index
combined_csv ["Experiment"] = combined_csv ["Experiment"].str [:-4] + "_" + combined_csv ["Experiment"].str [4:]
combined_csv.drop (indexnames, inplace = True)
combined_csv.to_csv (os.path.join(Output_dir, "Wall.csv"), index = False, encoding = "utf-8-sig")

Wall_transpose = combined_csv.set_index ("Experiment").T
Wall_transpose.to_csv(os.path.join(Output_dir, "Wall.Transpose.csv"), index = False, encoding = "utf-8-sig")