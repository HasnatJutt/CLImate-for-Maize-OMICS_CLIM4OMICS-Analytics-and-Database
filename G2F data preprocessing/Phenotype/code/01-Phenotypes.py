# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:27:08 2019

@author: psarzaeim2, Hasnat

Updated on May 2023 
"""

## Creating Pivot Tables for G2F Phenotypes Data, Y.csv, and YP1P2.csv files
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
import pathlib
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

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
            Output_path = os.path.join(Input_path,'../../G2F data preprocessing/Phenotype/output')
            Output_dir = output_fdir(Output_path)
    else:
        print(f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../File Control/Phenotype/output"):
    Input_dir = "../../../File Control/Phenotype/output"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../G2F data preprocessing/Phenotype/output'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("File Control/Phenotype/output"):
    Input_dir = "File Control/Phenotype/output"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'G2F data preprocessing/Phenotype/output'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("../File Control/Phenotype/output"):
    Input_dir = "../File Control/Phenotype/output"     
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../G2F data preprocessing/Phenotype/output'
        Output_dir = output_fdir(Output_path)
else:
    print("No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

# =============================================================================
# Concatenation
# =============================================================================
Phenotype_files =glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
Phenotype_file = pd.concat ([pd.read_csv (f) for f in Phenotype_files])

Phenotype_file = Phenotype_file [["ID", "Year.x", "Loc.x", "Env.x", "Pedigree.x", "Year.y", "Experiment", "P1", "P2", "Plant Height [cm]", 
                                  "Ear Height [cm]", "Grain Moisture [%]", "Grain Yield [bu/A]"]]

# =============================================================================
#  Creating pivot tables
# =============================================================================
pivot = pd.pivot_table (Phenotype_file, values = ["Plant Height [cm]", "Ear Height [cm]" , "Grain Moisture [%]", "Grain Yield [bu/A]"], 
                                      index = "ID", 
                                      aggfunc = np.mean,
                                      dropna = False)


pivot.to_csv(os.path.abspath(os.path.join(Output_dir ,"pivot.csv")))


df = pd.read_csv (os.path.abspath(os.path.join(Output_dir ,"pivot.csv")))

df ["Year.x"] = df ["ID"].str[:4]
df ["Loc.x"] = df ["ID"].str[5:9]
df ["Env.x"] = df ["ID"].str[:9]
df ["Experiment_ID"] = df ["Env.x"].str.replace ("_", "")
df ["Pedigree.x"] = df ["ID"].str[10:]
df ["Year.y"] = df ["Year.x"]
df ["Experiment"] = df ["Loc.x"]
df [["P1", "P2"]] = df ["Pedigree.x"].str.split ("/", expand = True)

df = df [["ID", "Year.x", "Loc.x", "Env.x", "Pedigree.x", "Year.y", "Experiment", "P1", "P2", "Plant Height [cm]", "Ear Height [cm]", 
          "Grain Moisture [%]", "Grain Yield [bu/A]", "Experiment_ID"]]

df.to_csv(os.path.abspath(os.path.join(Output_dir ,"Phenotypes.csv")), index = None)

os.remove (os.path.abspath(os.path.join(Output_dir ,"pivot.csv")))

# =============================================================================
# YP1P2.csv and Y.csv
# =============================================================================
YP1P2 = pd.read_csv (os.path.abspath(os.path.join(Output_dir ,"Phenotypes.csv")), index_col = None)

YP1P2 ["State"] = YP1P2 ["Experiment"].str[:2]
YP1P2 ["City"] = YP1P2 ["Experiment"].str[:2]

YP1P2.rename (columns = {"Plant Height [cm]":"Ismean.y"}, inplace = True)
YP1P2.rename (columns = {"Grain Yield [bu/A]":"Ismean.x"}, inplace = True)

YP1P2 = YP1P2 [["ID", "Year.x", "Loc.x", "Env.x", "Pedigree.x", "Year.y", "Ismean.x", "Ismean.y",
                "Experiment", "State", "City", "P1", "P2", "Experiment_ID"]]

YP1P2.to_csv(os.path.abspath(os.path.join(Output_dir ,"0YP1P2.csv")), index = None)

YP1P2  = YP1P2.dropna (subset = ["Ismean.x"])
YP1P2.to_csv(os.path.abspath(os.path.join(Output_dir ,"Nomissing.csv")), index = None)

#Y = pd.read_csv (Output_dir + "0YP1P2" + ".csv", index_col = None)
#Y = Y [["ID", "Year.x", "Loc.x", "Env.x", "Pedigree.x", "Year.y", "Ismean.x", "Ismean.y", "Experiment", "State", "City", "UID", "EID", "CV1", "CV2", "Experiment_ID"]]
#Y.to_csv ("Y" + ".csv", index = None)

# =============================================================================
# Plots
# =============================================================================
df.dropna (inplace = True)
sns.set (style = "darkgrid")

plt.figure (figsize = (10,6))
sns.histplot(df["Plant Height [cm]"], kde=True, stat="density")
plt.savefig(os.path.abspath(os.path.join(Output_dir , "Plant Height [cm].png")), dpi = 400)
plt.close ()

plt.figure (figsize = (10,6))
sns.histplot(df["Ear Height [cm]"], color = "Pink", kde=True, stat="density")
plt.savefig(os.path.abspath(os.path.join(Output_dir , "Ear Height [cm].png")), dpi = 400)
plt.close ()

plt.figure (figsize = (10,6))
sns.histplot(df["Grain Moisture [%]"], color = "Blue", kde=True, stat="density")
plt.savefig(os.path.abspath(os.path.join(Output_dir ,"Grain Moisture [%].png")), dpi = 400)
plt.close ()

plt.figure (figsize = (10,6))
sns.histplot(df["Grain Yield [bu/A]"], color = "Green", kde=True, stat="density")
plt.savefig(os.path.abspath(os.path.join(Output_dir ,"Grain Yield [bu per Ac].png")), dpi = 400)
plt.close ()

plt.figure(figsize = (10,6))
sns.countplot(df["Year.x"])
plt.xlabel("Year")
plt.ylabel("No. of Unique Hybrids")
plt.savefig(os.path.abspath(os.path.join(Output_dir , "No. of Unique Hybrids.png")), dpi=400)
plt.close ()
###############################################################################
df = df.drop (["Year.x", "Year.y"], axis = 1)
pair = sns.pairplot (df)
plt.savefig(os.path.abspath(os.path.join(Output_dir , "pairplot.png")), dpi = 400)
plt.close ()
###############################################################################
df1 = df._get_numeric_data ()
df2 = MinMaxScaler ().fit_transform (df1.values)
df3 = pd.DataFrame (df2)
df3.columns = ["Plant Height_Scaled", "Ear Height_Scaled", "Grain Mosture_Scaled", "Grain Yeild_Scaled"]
plt.figure()
g = sns.PairGrid (df3, height = 4)
g.map_diag (sns.histplot, color = "orange",kde=True, stat="density")
g.map_upper (plt.scatter, color = "skyblue")
g.map_lower (sns.kdeplot, color = "green")
plt.savefig(os.path.abspath(os.path.join(Output_dir , "pairgrid_scaled.png")), dpi = 400)
plt.close ()