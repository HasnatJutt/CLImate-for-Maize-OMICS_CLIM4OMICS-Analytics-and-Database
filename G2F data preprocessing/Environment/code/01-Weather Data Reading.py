# -*- coding: utf-8 -*-
"""
Created on Mon May 20 11:45:11 2019

@author: psarzaeim2
"""

## Reading Waether (Environmental) Data Excel Files 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../../../File Control/Environment/output/")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../../../G2F data preprocessing/Environment/output/Weather Data Reading")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Counting the number of yaers and list the subdirectory of environment data files
# =============================================================================
Weather_files = os.listdir (Input_dir) 
for file in Weather_files:
    df = pd.read_csv (Input_dir + file)
    df ["Experiment_ID"] = df ["Year [Local]"].astype (str) + df ["Experiment"]
    Experiments = df["Experiment"].unique()
#    print(Experiments)
    for exp in Experiments:
        Experiment = df.loc [df["Experiment"] == exp]
        Year = Experiment ["Year [Local]"].unique ()
#        print (str (exp))
#        print (str (Year))
        Experiment.to_csv (str (Year [0]) + str (exp) + ".csv")
        