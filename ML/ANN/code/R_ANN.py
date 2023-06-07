# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 00:30:50 2020

@author: psarzaeim2, Hasnat

Updated on May 2023
"""

## Reading data from data sources  
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pathlib
import sys
import argparse
import glob
import pandas as pd
import numpy as np
from functools import reduce
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from statistics import mean
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_regression
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression

# =============================================================================
# Input and Output directories
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory from Current Path', required=False)
parser.add_argument('-o', '--output', help='Path of Output Directory from Current Path', required=False)
parser.add_argument('-m', '--meta', help='Path of Meta Files Input Directory1 from Current Path', required=False)
parser.add_argument('-o1', '--output1', help='Path of Output Directory (Predication) from Current Path', required=False)
parser.add_argument('-o2', '--output2', help='Path of Output Directory (Y_Predication) from Current Path', required=False)
parser.add_argument('-o3', '--output3', help='Path of Output Directory (Loss) from Current Path', required=False)
parser.add_argument('-o4', '--output4', help='Path of Output Directory from Current Path', required=False)
parser.add_argument('-o5', '--output5', help='Path of Output Directory (Performance) from Current Path', required=False)
parser.add_argument('-o10', '--output10', help='Path of Output Directory All files (Database/All Files) from Current Path', required=False)
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
            Output_path = os.path.join(Input_path, '../../../ML/ANN/output/R/pairplots')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../Database/output/R/more"):
    Input_dir = "../../../Database/output/R/more"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../ML/ANN/output/R/pairplots'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("Database/output/R/more"):
    Input_dir = "Database/output/R/more"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'ML/ANN/output/R/pairplots'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../Database/output/R/more"):
    Input_dir = "../Database/output/R/more"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../ML/ANN/output/R/pairplots'
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

elif os.path.exists("../../../G2F data preprocessing/Meta/output"):
    Input_dir1 = "../../../G2F data preprocessing/Meta/output"

elif os.path.exists("G2F data preprocessing/Meta/output"):
    Input_dir1 = "G2F data preprocessing/Meta/output"

elif os.path.exists("../G2F data preprocessing/Meta/output"):
    Input_dir1 = "../G2F data preprocessing/Meta/output"
elif os.path.exists("../../G2F data preprocessing/Meta/output"):
    Input_dir1 = "../../G2F data preprocessing/Meta/output"
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

if args.output1 is not None:
    Output_dir1 = output_fdir(args.output1)
else:
    if Output_dir is not None:
        Output_path1 = os.path.join(pathlib.Path(Output_dir).parent, 'predictions')
        Output_dir1 = output_fdir(Output_path1)
    else:
        print("Neither Output Directory set nor Output for Predication is provided in argument")
if args.output2 is not None:
    Output_dir2 = output_fdir(args.output2)
else:
    if Output_dir is not None:
        Output_path2 = os.path.join(pathlib.Path(Output_dir).parent, 'y_predicted')
        Output_dir2 = output_fdir(Output_path2)
    else:
        print("Neither Output Directory set nor Output for Y_Predication is provided in argument")

if args.output3 is not None:
    Output_dir3 = output_fdir(args.output3)
else:
    if Output_dir is not None:
        Output_path3 = pathlib.Path(Output_dir).parent
        Output_dir3 = output_fdir(Output_path3)
    else:
        print("Neither Output Directory set nor Output for Output is provided in argument")
if args.output4 is not None:
    Output_dir4 = output_fdir(args.output4)
else:
    if Output_dir is not None:
        Output_path4 = os.path.join(pathlib.Path(Output_dir).parent, 'loss')
        Output_dir4 = output_fdir(Output_path4)
    else:
        print("Neither Output Directory set nor Output for Loss is provided in argument")

if args.output5 is not None:
    Output_dir5 = output_fdir(args.output5)
else:
    if Output_dir is not None:
        Output_path5 = os.path.join(pathlib.Path(Output_dir).parent.parent, 'Performance')
        Output_dir5 = output_fdir(Output_path5)
    else:
        print("Neither Output Directory set nor Output for Performance is provided in argument")
if args.output10 is not None:
    Output_dir10 = output_fdir(args.output10)
else:
    if Output_dir is not None:
        Output_path10 = os.path.join(pathlib.Path(Output_dir).parent.parent, 'Performance')
        Output_dir10 = output_fdir(Output_path10)
    else:
        print("Neither Output Directory set nor Output for Performance is provided in argument")
if args.output10 is not None:
    Output_path10 = os.path.abspath(args.output10)
    if os.path.exists(Output_path10):
        Output_dir10 = Output_path10
    else:
        print(
            f'The input directory {args.output10} does not exists on system path. Correct the Input directory, provided directory has {Output_path10} path')

elif os.path.exists("../../../Database/output/All_Files"):
    Output_dir10 = "../../../Database/output/All_Files"

elif os.path.exists("Database/output/All_Files"):
    Output_dir10 = "Database/output/All_Files"

elif os.path.exists("../Database/output/All_Files"):
    Output_dir10 = "../Database/output/All_Files"
elif os.path.exists("../../Database/output/All_Files"):
    Output_dir10 = "../../Database/output/All_Files"
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")


# =============================================================================
# Artificial Neural Network Design
# =============================================================================
Experiments_list = []
RMSE_list = []
RMSE_list_Min = []
RMSE_list_Max = []
Abb = "R"
variable = "Rainfall [mm]"

# Data Preprocessing
files = glob.glob(os.path.abspath(os.path.join(Input_dir, '*.csv')))
for filename in files:
    file = os.path.basename(filename)
    Experiments_list.append (file [:-4])
    df = pd.read_csv (filename, index_col = "Day of Year [Local]")
    df_new = df [df.isnull().any(1)]
    df_new_index = df_new.index.values.tolist()
    df_index = pd.DataFrame (df_new_index, columns = ["Day of Year [Local]"])
    df.dropna (inplace = True)
    
# Pairplot
    plt.style.use ("seaborn")
    pairplot = sns.pairplot (df)
    pairplot.savefig(os.path.join (Output_dir , file [:-4] + ".png"), dpi = 400)
    plt.close ()
   
# Mean ########################################################################  
# Input and Output definition 
    X = df.iloc [:,3].values.reshape (-1, 1)
#    print(X)
    y = df.iloc [:,0].values
#    print(y)

# Train and Test Data and Scaling  
    X_train, X_test, y_train, y_test = train_test_split (X, y, test_size = 0.40)
    scaler = MinMaxScaler ()
    # scaler.fit (X_train)
    # X_train = scaler.transform (X_train)
    # X_test = scaler.transform (X_test)

# K-fold Cross Validation
    CV = KFold (n_splits = 5)
    for train, test in CV.split (X_train):
        X_train, X_test = X [train], X [test]
        y_train, y_test = y [train], y [test]
        
        scaler.fit (X_train)
        X_train = scaler.transform (X_train)
        X_test = scaler.transform (X_test)

# Create Model    
        ANN = Sequential ()
        ANN.add (Dense (15, activation = "relu"))
        # ANN.add (Dropout (0.5))
        ANN.add (Dense (10, activation = "relu"))
        # ANN.add (Dropout (0.5))
        # ANN.add (Dense (10, activation = "relu"))
        # ANN.add (Dropout (0.5))
        ANN.add (Dense (1))

# Comiple Model    
        ANN.compile (optimizer = "adam", loss = "mse")
        early_stop = EarlyStopping (monitor = "val_loss", mode = "min", verbose = 0, patience = 25)
        ANN.fit (x = X_train, y = y_train, epochs = 10000, validation_data = (X_test, y_test), callbacks = [early_stop])
        # print("Model Evaluation: ", ANN.evaluate (X_test, y_test))

# Loss Plot
        loss = pd.DataFrame (ANN.history.history)
        loss.rename (columns = {"loss":"Training Loss", "val_loss":"Test Loss"}, inplace = True)
        loss.plot ()
        plt.xlabel ("Epoch")
        plt.ylabel ("Loss")
        plt.savefig(os.path.join (Output_dir4 , "Mean" + file [:-4] + ".png"), dpi = 400)
        plt.close ()

# Predict for Test Data    
        predictions = ANN.predict (X_test)
        scatterplot = plt.scatter (y_test, predictions, c = "black", label = "$R^2$ Mean = " + str(round (r2_score (y_test, predictions), 4)))
        plt.xlabel ("Observed")
        plt.ylabel ("Predicted")
        plt.legend ()
        plt.savefig(os.path.join (Output_dir1 , "Mean" + file [:-4] + ".png"), dpi = 400)
        RMSE = np.sqrt (metrics.mean_squared_error (y_test, predictions))
        RMSE_list.append (RMSE)
        # plt.savefig(os.path.join (Output_dir1 + file [:-4] + ".png"), dpi = 400)

# Predict New Data    
    # X_new = df_new [selected_feature].values
    X_new = df_new.iloc [:,3].values.reshape (-1, 1)
    X_new = scaler.transform (X_new)
    y_new = ANN.predict (X_new)
    y_new = pd.DataFrame (y_new, columns = [variable])
    y_new = pd.concat ([df_index, y_new], axis = 1)
    y_new.to_csv(os.path.join (Output_dir2 , file [:-4] + ".csv"), index = None)
    
    plt.close ()
        
# # Train and Test Data 
#     X_train, X_test, y_train, y_test = train_test_split (X, y, test_size = 0.25)
#     scaler = MinMaxScaler ()
#     scaler.fit (X_train)
#     X_train = scaler.transform (X_train)
#     X_test = scaler.transform (X_test)
    
# # ANN Model     
#     ANN = Sequential ()
#     ANN.add (Dense (30, activation = "relu"))
# #    ANN.add (Dropout (0.5))
#     ANN.add (Dense (10, activation = "relu"))
# #    ANN.add (Dropout (0.5))
# #    ANN.add (Dense (10, activation = "relu"))
# #    ANN.add (Dropout (0.5))
#     ANN.add (Dense (1))
    
#     ANN.compile (optimizer = "adam", loss = "mse")
#     early_stop = EarlyStopping (monitor = "val_loss", mode = "min", verbose = 0, patience = 25)
#     ANN.fit (x = X_train, y = y_train, epochs = 10000, validation_data = (X_test, y_test), callbacks = [early_stop])
    
# # Loss Plot
#     loss = pd.DataFrame (ANN.history.history)
#     loss.plot ()
#     plt.savefig(os.path.join (Output_dir4 + file [:-4] + ".png"), dpi = 400)
#     plt.close ()

# # Predict for Test Data
#     predictions = ANN.predict (X_test)
#     scatterplot = plt.scatter (y_test, predictions, c = "black",  label = "$R^2$ Mean = " + str(round (r2_score (y_test, predictions), 2)))
#     RMSE = np.sqrt (metrics.mean_squared_error (y_test, predictions))
#     RMSE_list.append (RMSE)

# # Predict New Data     
#     X_new = df_new.iloc [:,3].values.reshape (-1, 1)
#     X_new = scaler.transform (X_new)
#     y_new = ANN.predict (X_new)
#     y_new = pd.DataFrame (y_new, columns = [variable])
#     y_new = pd.concat ([df_index, y_new], axis = 1)
#     y_new.to_csv (Output_dir2 + file [:-4] + ".csv", index = None)
    
# Min #########################################################################
#    # Train
#    X = df.iloc [:,3:].values
##    print(X)
#    y = df.iloc [:,1].values
##    print(y)
#
## Train and Test Data     
#    X_train, X_test, y_train, y_test = train_test_split (X, y, test_size = 0.25)
#    scaler = MinMaxScaler ()
#    scaler.fit (X_train)
#    X_train = scaler.transform (X_train)
#    X_test = scaler.transform (X_test)        
# 
## ANN Model   
#    ANN = Sequential ()
#    ANN.add (Dense (25, activation = "relu"))
##    ANN.add (Dropout (0.5))
#    ANN.add (Dense (15, activation = "relu"))
##    ANN.add (Dropout (0.5))
#    ANN.add (Dense (10, activation = "relu"))
##    ANN.add (Dropout (0.5))
#    ANN.add (Dense (1))
#    
#    ANN.compile (optimizer = "adam", loss = "mse")
#    early_stop = EarlyStopping (monitor = "val_loss", mode = "min", verbose = 0, patience = 25)
#    ANN.fit (x = X_train, y = y_train, epochs = 10000, validation_data = (X_test, y_test), callbacks = [early_stop])
#
## Predict for Test Data    
#    predictions = ANN.predict (X_test)
#    RMSE = np.sqrt (metrics.mean_squared_error (y_test, predictions))
#    RMSE_list_Min.append (RMSE)
#
## Predict New Data 
#    X_new_min = df_new.iloc [:,3:].values
#    X_new = scaler.transform (X_new)
#    y_new_min = ANN.predict (X_new_min)
#    y_new_min = pd.DataFrame (columns = ["Min " + variable])
#    y_new_min [["Min " + variable]] = 0
#    y_new_min = pd.concat ([y_new, y_new_min], axis = 1)
    
# Max #########################################################################
#    # Train
#    X = df.iloc [:,3:].values
##    print(X)
#    y = df.iloc [:,2].values
##    print(y)
#    
## Train and Test Data     
#    X_train, X_test, y_train, y_test = train_test_split (X, y, test_size = 0.25)
#    scaler = MinMaxScaler ()
#    scaler.fit (X_train)
#    X_train = scaler.transform (X_train)
#    X_test = scaler.transform (X_test)  
#
## ANN Model       
#    ANN = Sequential ()
#    ANN.add (Dense (30, activation = "relu"))
##    ANN.add (Dropout (0.5))
#    ANN.add (Dense (15, activation = "relu"))
##    ANN.add (Dropout (0.5))
#    ANN.add (Dense (10, activation = "relu"))
##    ANN.add (Dropout (0.5))
#    ANN.add (Dense (1))
#    
#    ANN.compile (optimizer = "adam", loss = "mse")
#    early_stop = EarlyStopping (monitor = "val_loss", mode = "min", verbose = 0, patience = 25)
#    ANN.fit (x = X_train, y = y_train, epochs = 10000, validation_data = (X_test, y_test), callbacks = [early_stop])
#
## Predict for Test Data 
#    predictions = ANN.predict (X_test)
#    RMSE = np.sqrt (metrics.mean_squared_error (y_test, predictions))
#    RMSE_list_Max.append (RMSE)
#
## Predict New Data 
#    X_new_max = df_new.iloc [:,3:].values
#    y_new_max = ANN.predict (X_new_max)
#    y_new_max = pd.DataFrame (y_new_max, columns = ["Max " + variable])
#    y_new_max = pd.concat ([y_new_min, y_new_max], axis = 1)
#    y_new_max.to_csv (Output_dir2 + file [:-4] + ".csv", index = None)
    
    # plt.xlabel ("Observed")
    # plt.ylabel ("Predicted")
    # plt.legend ()
    # plt.savefig(os.path.join (Output_dir1 + file [:-4] + ".png"), dpi = 400)
    # plt.close ()

# =============================================================================
# Average RMSE and Plots
# =============================================================================        
df = pd.DataFrame (list(zip(Experiments_list, RMSE_list)), columns = ["Experiment_ID", "RMSE"])  
df.plot.density ()
plt.title ("RMSE")
plt.savefig(os.path.join (Output_dir3 , "RMSE_Density.png"), dpi = 400)
plt.close ()

df ["RMSE"].plot.hist (color = "black")
plt.title ("RMSE")
plt.savefig(os.path.join (Output_dir3 , "RMSE_Histogram.png"), dpi = 400)
plt.close ()

#df ["RMSE_Min"].plot.hist (color = "green")
#plt.title ("RMSE_Min")
#plt.savefig(os.path.join (Output_dir3 + "RMSE_Min_Histogram.png"), dpi = 400)
#plt.close ()

#df ["RMSE_Max"].plot.hist (color = "red")
#plt.title ("RMSE_Max")
#plt.savefig(os.path.join (Output_dir3 + "RMSE_Max_Histogram.png"), dpi = 400)
#plt.close ()

df.plot.box ()
plt.title ("RMSE")
plt.savefig(os.path.join (Output_dir3 , "RMSE_Box.png"), dpi = 400)
plt.close ()

print ("RMSE_ave =", mean (RMSE_list))
#print ("RMSE_ave_Min =", mean (RMSE_list_Min))
#print ("RMSE_ave_Max =", mean (RMSE_list_Max))

lat_lon = pd.read_csv(os.path.join (Input_dir1 , "lat_lon.csv"))
df ["Experiment_ID"] = df ["Experiment_ID"].str [1:]
Merge = pd.merge (df, lat_lon, on = "Experiment_ID")

Merge.to_csv(os.path.join (Output_dir5 , Abb + "_Performance.csv"), index = None)

# =============================================================================
# Complete Database
# =============================================================================
files = glob.glob(os.path.abspath(os.path.join(Input_dir, '*.csv')))
yfiles = glob.glob(os.path.abspath(os.path.join(Output_dir2, '*.csv')))
for filename in files:
    for yfilename in yfiles:
        file = os.path.basename(filename)
        yfile = os.path.basename(yfilename)
        if file [:-4] == yfile [:-4]:
            dF = pd.read_csv (filename)
            dF = dF.iloc [:,:4]
            dy = pd.read_csv (yfilename)
            complete = pd.concat ([dF,dy], join = "inner")
            complete.sort_values (by = ["Day of Year [Local]"], inplace = True)
            complete.dropna (inplace = True)
            complete.columns = ["Day", Abb + "M"]
            complete [Abb + "M_Day"] = Abb + "M" + complete ["Day"].astype (str)
            complete = complete [["Day", Abb + "M", Abb + "M_Day"]]
            complete.to_csv(os.path.join (Output_dir10 , file), index = None)