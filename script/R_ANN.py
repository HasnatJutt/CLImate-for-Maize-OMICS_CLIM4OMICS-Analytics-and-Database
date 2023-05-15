# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 00:30:50 2020

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
Input_dir = os.chdir ("../../../Database/output/R/more")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../../../../ML/ANN/output/R/pairplots")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"
Output_dir1 = os.chdir ("../predictions")
Output_dir1 = os.getcwd ().replace ("\\", "/")
Output_dir1 = Output_dir1 + "/"
Output_dir2 = os.chdir ("../y_predicted")
Output_dir2 = os.getcwd ().replace ("\\", "/")
Output_dir2 = Output_dir2 + "/"
Output_dir4 = os.chdir ("../loss")
Output_dir4 = os.getcwd ().replace ("\\", "/")
Output_dir4 = Output_dir4 + "/"
Output_dir3 = os.chdir ("../")
Output_dir3 = os.getcwd ().replace ("\\", "/")
Output_dir3 = Output_dir3 + "/"
Output_dir5 = os.chdir ("../Performance")
Output_dir5 = os.getcwd ().replace ("\\", "/")
Output_dir5 = Output_dir5 + "/"
Output_dir10 = os.chdir ("../../../../Database/output/All_Files")
Output_dir10 = os.getcwd ().replace ("\\", "/")
Output_dir10 = Output_dir10 + "/"
Input_dir1 = os.chdir ("../../../G2F data preprocessing/Meta/output")
Input_dir1 = os.getcwd ().replace ("\\", "/")
Input_dir1 = Input_dir1 + "/"

print("Input directory = ", Input_dir)
print ("Output directory = ", Output_dir3)

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
files = os.listdir (Input_dir)
for file in files:
    Experiments_list.append (file [:-4])
    df = pd.read_csv (Input_dir + file, index_col = "Day of Year [Local]")
    df_new = df [df.isnull().any(1)]
    df_new_index = df_new.index.values.tolist()
    df_index = pd.DataFrame (df_new_index, columns = ["Day of Year [Local]"])
    df.dropna (inplace = True)
    
# Pairplot
    plt.style.use ("seaborn")
    pairplot = sns.pairplot (df)
    pairplot.savefig (Output_dir + file [:-4] + ".png", dpi = 400)
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
        plt.savefig (Output_dir4 + "Mean" + file [:-4] + ".png", dpi = 400)
        plt.close ()

# Predict for Test Data    
        predictions = ANN.predict (X_test)
        scatterplot = plt.scatter (y_test, predictions, c = "black", label = "$R^2$ Mean = " + str(round (r2_score (y_test, predictions), 4)))
        plt.xlabel ("Observed")
        plt.ylabel ("Predicted")
        plt.legend ()
        plt.savefig (Output_dir1 + "Mean" + file [:-4] + ".png", dpi = 400)
        RMSE = np.sqrt (metrics.mean_squared_error (y_test, predictions))
        RMSE_list.append (RMSE)
        # plt.savefig (Output_dir1 + file [:-4] + ".png", dpi = 400)

# Predict New Data    
    # X_new = df_new [selected_feature].values
    X_new = df_new.iloc [:,3].values.reshape (-1, 1)
    X_new = scaler.transform (X_new)
    y_new = ANN.predict (X_new)
    y_new = pd.DataFrame (y_new, columns = [variable])
    y_new = pd.concat ([df_index, y_new], axis = 1)
    y_new.to_csv (Output_dir2 + file [:-4] + ".csv", index = None)
    
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
#     plt.savefig (Output_dir4 + file [:-4] + ".png", dpi = 400)
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
    # plt.savefig (Output_dir1 + file [:-4] + ".png", dpi = 400)
    # plt.close ()

# =============================================================================
# Average RMSE and Plots
# =============================================================================        
df = pd.DataFrame (list(zip(Experiments_list, RMSE_list)), columns = ["Experiment_ID", "RMSE"])  
df.plot.density ()
plt.title ("RMSE")
plt.savefig (Output_dir3 + "RMSE_Density.png", dpi = 400)
plt.close ()

df ["RMSE"].plot.hist (color = "black")
plt.title ("RMSE")
plt.savefig (Output_dir3 + "RMSE_Histogram.png", dpi = 400)
plt.close ()

#df ["RMSE_Min"].plot.hist (color = "green")
#plt.title ("RMSE_Min")
#plt.savefig (Output_dir3 + "RMSE_Min_Histogram.png", dpi = 400)
#plt.close ()

#df ["RMSE_Max"].plot.hist (color = "red")
#plt.title ("RMSE_Max")
#plt.savefig (Output_dir3 + "RMSE_Max_Histogram.png", dpi = 400)
#plt.close ()

df.plot.box ()
plt.title ("RMSE")
plt.savefig (Output_dir3 + "RMSE_Box.png", dpi = 400)
plt.close ()

print ("RMSE_ave =", mean (RMSE_list))
#print ("RMSE_ave_Min =", mean (RMSE_list_Min))
#print ("RMSE_ave_Max =", mean (RMSE_list_Max))

lat_lon = pd.read_csv (Input_dir1 + "lat_lon.csv")
df ["Experiment_ID"] = df ["Experiment_ID"].str [1:]
Merge = pd.merge (df, lat_lon, on = "Experiment_ID")

Merge.to_csv (Output_dir5 + Abb + "_Performance" + ".csv", index = None)

# =============================================================================
# Complete Database
# =============================================================================
files = os.listdir (Input_dir)
yfiles = os.listdir (Output_dir2)
for file in files:
    for yfile in yfiles:
        if file [:-4] == yfile [:-4]:
            dF = pd.read_csv (Input_dir + file)
            dF = dF.iloc [:,:4]
            dy = pd.read_csv (Output_dir2 + yfile)
            complete = pd.concat ([dF,dy], join = "inner")
            complete.sort_values (by = ["Day of Year [Local]"], inplace = True)
            complete.dropna (inplace = True)
            complete.columns = ["Day", Abb + "M"]
            complete [Abb + "M_Day"] = Abb + "M" + complete ["Day"].astype (str)
            complete = complete [["Day", Abb + "M", Abb + "M_Day"]]
            complete.to_csv (Output_dir10 + file, index = None)