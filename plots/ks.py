"""
Created on Mon Apr 24 14:35:00 2023

@author: Hasnat
"""

# =============================================================================
# Import necessary libraries
# =============================================================================
import os, re, os.path
import glob
import pandas as pd
import numpy as np
from functools import reduce
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import time
import random
from matplotlib import ticker
import pylab
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
from shapely.geometry import Point, Polygon
from scipy import interpolate
import shapefile as shp
from collections import Counter
from sklearn import preprocessing
from matplotlib.legend_handler import HandlerLine2D
import statistics
from mpl_toolkits.axes_grid1 import make_axes_locatable

# =============================================================================
# Input and Output directories
# =============================================================================

Input_dir1 = "../G2F data preprocessing/Meta/output/"

Input_dir2 = "shapefiles"
Input_dir3 = "../Database/output/S"

Input_dir4 = "./"

# =============================================================================
# Creating dataframes
# =============================================================================
df = pd.read_csv(os.path.join(Input_dir1, "All_lat_lon.csv"))
G2F_files = glob.glob(os.path.abspath(os.path.join(Input_dir3, '**/*.csv')), recursive=True)

# =============================================================================
# Temperature
complete = pd.DataFrame()
ind = pd.DataFrame()
for file in G2F_files:
    filename = os.path.basename(file)
    G2F = pd.read_csv(file)
    if filename[5:7] == 'KS':
        Mean = G2F["NSRDB Solar Radiation [W/m2]"].mean()  # here
        sub_T = pd.DataFrame(
            {"Experiment_ID": [filename[1:9]], "mean_v": [Mean],"state":[filename[5:7]], "variable":[filename[0]]})
        ind = pd.concat([ind, sub_T], ignore_index=True, sort=False)
    # G2F.rename(columns={f"{filename[0]}M": "gMean"}, inplace=True)
    # names=G2F.columns.tolist()
    # names.remove("gMean")
    # G2F.drop(columns=names, axis=1, inplace=True)
    # G2F["Experiment_ID"]= filename[1:9]
    # G2F["state"] = filename[5:7]
    # G2F["variable"] = filename[0]
    # G2F["count_v"] = None
    # G2F.at[0, "count_v"]=1
    # complete = pd.concat([complete, G2F], ignore_index=True, sort=False)
print(ind)
ind_group = ind.groupby(["variable", "state"]).agg({"mean_v":'mean', "Experiment_ID":'count'})
ind_group.reset_index(inplace=True)
ind_group.to_csv("KS.csv", index=False)
# R_complete = complete[complete["variable"]=='R'].groupby(["variable", "state"]).agg({"gMean":'sum', "count_v":'count'})
# R_complete.reset_index(inplace=True)
# No_R_complete = complete[complete["variable"]!='R'].groupby(["variable", "state"]).agg({"gMean":'sum', "count_v":'count'})
# No_R_complete.reset_index(inplace=True)
# complete_group = pd.concat([R_complete, No_R_complete], ignore_index=True, sort=False)
# # complete_group.reset_index(inplace=True)
# complete_group.to_csv("StateGMean.csv", index=False)
# joined = pd.merge(complete_group, ind_group, how='inner', left_on=["variable", "state"], right_on=["variable", "state"])
# joined.to_csv("StateCountMean.csv", index=False)
# for var in ind_group["variable"].tolist():
#     data = ind_group[ind_group["variable"]==var]
#     #data.drop(columns=["variable", "mean_v", "Experiment_ID"], axis=1, inplace=True)
#     data.drop(columns=["variable"], axis=1, inplace=True)
#     data.rename(columns={"mean_v":f"mean_{var}", "Experiment_ID":f"count_{var}", "state":"State"}, inplace=True)
#     data.to_csv(f"{var}_count.csv", index=False)