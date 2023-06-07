# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 12:43:29 2020

@author: psarzaeim2
"""

## Control
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import sys
import glob
import os.path
import argparse
import pandas as pd
import numpy as np
from functools import reduce
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
import shutil

# =============================================================================
# Input and Output directories
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory from Current Path', required=False)
parser.add_argument('-o', '--output', help='Path of Output Directory from Current Path', required=False)
parser.add_argument('-p', '--pheno', help='Path of Phenotype Files Input Directory (G2F/Phenotype) from Current Path', required=False)
parser.add_argument('-g', '--geno', help='Path of Phenotype Files Input Directory (G2F/Genotype) from Current Path', required=False)
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
            Output_path = os.path.join(Input_path, '../../Control/output')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../Selection/output/Selected_Files"):
    Input_dir = "../../Selection/output/Selected_Files"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../Control/output'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("Selection/output/Selected_Files"):
    Input_dir = "Selection/output/Selected_Files"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'Control/output'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../Selection/output/Selected_Files"):
    Input_dir = "../Selection/output/Selected_Files"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../Control/output'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()

if args.pheno is not None:
    Input_path1 = os.path.abspath(args.pheno)
    if os.path.exists(Input_path1):
        Input_dir1 = Input_path1
    else:
        print(
            f'The input directory {args.pheno} does not exists on system path. Correct the Input directory, provided directory has {Input_path1} path')

elif os.path.exists("../../G2F data preprocessing/Phenotype/output"):
    Input_dir1 = "../../G2F data preprocessing/Phenotype/output"

elif os.path.exists("G2F data preprocessing/Phenotype/output"):
    Input_dir1 = "G2F data preprocessing/Phenotype/output"

elif os.path.exists("../G2F data preprocessing/Phenotype/output"):
    Input_dir1 = "../G2F data preprocessing/Phenotype/output"
elif os.path.exists("../G2F data preprocessing/Phenotype/output"):
    Input_dir1 = "../G2F data preprocessing/Phenotype/output"
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()
if args.geno is not None:
    Input_path2 = os.path.abspath(args.geno)
    if os.path.exists(Input_path2):
        Input_dir2 = Input_path2
    else:
        print(
            f'The input directory {args.geno} does not exists on system path. Correct the Input directory, provided directory has {Input_path2} path')

elif os.path.exists("../../G2F data preprocessing/Genotype/output"):
    Input_dir2 = "../../G2F data preprocessing/Genotype/output"

elif os.path.exists("G2F data preprocessing/Genotype/output"):
    Input_dir2 = "G2F data preprocessing/Genotype/output"

elif os.path.exists("../G2F data preprocessing/Genotype/output"):
    Input_dir2 = "../G2F data preprocessing/Genotype/output"
elif os.path.exists("../G2F data preprocessing/Genotype/output"):
    Input_dir2 = "../G2F data preprocessing/Genotype/output"
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()

print("Input directory = ", Input_dir)
print("Input directory = ", Input_dir1)
print("Input directory = ", Input_dir2)
print ("Output directory = ", Output_dir)

# =============================================================================    
# Controling the consistency between selected Weather files (Wall.csv) and Phenotype file (YP1P2.csv)
# =============================================================================
# Wall
Wall = pd.read_csv(os.path.join(Input_dir, "Wall.csv"))
Experiments_Wall = Wall["Experiment"].tolist()

# YP1P2
YP1P2 = pd.read_csv(os.path.join(Input_dir1,"YP1P2.csv"))
Experiments_YP1P2 =  YP1P2 ["Env.x"].tolist ()

Shared = list (set (Experiments_Wall) & set (Experiments_YP1P2))
# print (len(Shared))

Wall = Wall [Wall ["Experiment"].isin (Shared)]
YP1P2 = YP1P2 [YP1P2 ["Env.x"].isin (Shared)]

# =============================================================================    
# Controling the consistency between Phenotype file (YP1P2.csv) and Genotype files (GIDs.csv and X.csv)
# ============================================================================= 
# GIDs
GIDs = pd.read_csv(os.path.join(Input_dir2, "GIDs2.csv"))
GIDs.drop_duplicates (subset = ["GIDs"], inplace = True)
GIDs_list = GIDs ["GIDs"].tolist ()
# print(len(GIDs_list))

# X
X = pd.read_csv(os.path.join(Input_dir2, "X.csv"), low_memory = False)
X.rename (columns = {"Unnamed: 0":"index"}, inplace = True)
X.drop_duplicates (subset = ["index"], inplace = True)
X.dropna (how = "all", inplace = True)
X.dropna (axis = "columns", how = "all", inplace = True)
# X.index.name = "index"
# X.drop_duplicates (subset = ["index"], inplace = True)
# print (len (X))
# print (len (X.columns))
# X.reset_index (inplace = True)
# X_list = X.iloc [:,0].tolist ()
X_list = X ["index"].tolist()
# print(len(X_list))
# print(X)

# YP1P2
P1_list = YP1P2 ["P1"].tolist ()
# print(len(list (set (P1_list))))

Shared_1 = list (set (GIDs_list) & set (X_list) & set (P1_list))
# print(len(Shared_1))

YP1P2_1 = YP1P2 [YP1P2 ["P1"].isin (Shared_1)]

P2_list = YP1P2_1 ["P2"].tolist ()
# print(len(list (set (P2_list))))

Shared_2 = list (set (GIDs_list) & set (X_list) & set (P2_list))
# print(len(Shared_2))

YP1P2_2 = YP1P2_1 [YP1P2_1 ["P2"].isin (Shared_2)]
# print(YP1P2_2)

P1_list_new = YP1P2_2 ["P1"].tolist ()
P2_list_new = YP1P2_2 ["P2"].tolist ()

Shared_3 = list (set (P1_list_new) | set (P2_list_new))
GIDs = GIDs [GIDs ["GIDs"].isin (Shared_3)]
X = X [X.iloc [:,0].isin (Shared_3)]

GIDs.to_csv(os.path.join(Output_dir,"GIDs2.csv"), index = None)
X.to_csv(os.path.join(Output_dir, "X.csv"), index = None)

# =============================================================================    
# Controling the consistency between Phenotype file (Updated YP1P2.csv) and Weather file (updated Wall.csv)
# ============================================================================= 
# Updated Wall
Experiments_Wall = Wall ["Experiment"].tolist ()

# Updated YP1P2
Experiments_YP1P2 =  YP1P2_2 ["Env.x"].tolist ()

Shared = list (set (Experiments_Wall) & set (Experiments_YP1P2))
print(Shared)

# Wall = Wall [Wall ["Experiment"].isin (Shared)]
# YP1P2 = YP1P2_2 [YP1P2_2 ["Env.x"].isin (Shared)]

Wall.to_csv (os.path.join(Output_dir, "Wall.csv"), index = None)

# =============================================================================    
# Adding UID and EID columns to the updated Phenitype file (YP1P2.csv)
# ============================================================================= 
YP1P2.reset_index (drop = True, inplace = True)
YP1P2.index += 1
YP1P2 ["UID"] = YP1P2.index
YP1P2 ["EID"] = YP1P2 ["Env.x"].astype ("category").cat.codes
YP1P2 ["EID"] = YP1P2 ["EID"] + 1

YP1P2 ["CV0"] = YP1P2 ["EID"]
YP1P2 ["CV00"] = YP1P2 ["UID"]

YP1P2.to_csv(os.path.join(Output_dir, "YP1P2.csv"), index = None)

# =============================================================================    
# Printing some informations about the selected experiments
# =============================================================================
GIDs_list = GIDs ["GIDs"].tolist ()
print ("NO. of Genotypes =", len(GIDs_list))

# X_list = X.iloc [:,0].tolist ()
# print ("NO. of Genotypes X =", len(X_list))

Experiment_list = Wall ["Experiment"].tolist ()
Experiment_set = set (Experiment_list)
Experiment_list_new = list (Experiment_set)
print ("NO. of Experiments =", len(Experiment_list_new))

P1_list = YP1P2 ["P1"].tolist ()
print ("NO. of Hybrids =", len(P1_list))

Pedigree_list = YP1P2 ["Pedigree.x"].tolist ()
Pedigree_set = set (Pedigree_list)
Pedigree_list_new = list (Pedigree_set)
print ("NO. of Unique Hybrids =", len(Pedigree_list_new))