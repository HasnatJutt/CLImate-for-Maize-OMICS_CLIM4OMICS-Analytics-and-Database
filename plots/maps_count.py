# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 18:59:44 2022

@author: psarzaeim2, Hasnat
"""

# =============================================================================
# Import necessary libraries
# =============================================================================
import os, re, os.path
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

# =============================================================================
# Input and Output directories
# =============================================================================
Input_dir1 = "../G2F data preprocessing/Meta/output"
Input_dir2 = "shapefiles"
Input_dir3 = "../G2F data preprocessing/Phenotype/output"

# =============================================================================
# Creating dataframes
# =============================================================================
experiment_data = gpd.GeoDataFrame.from_file("shapefiles/Experiment_count_proj.shp")
gdf = gpd.GeoDataFrame.from_file("shapefiles/USA_Canada_ShapefileMerge.shp")
gdf1 = gpd.GeoDataFrame.from_file("shapefiles/DEU_adm1.shp")
experiment = experiment_data[experiment_data["Experiment"] != 'GEH1']
minx, miny, maxx, maxy = experiment.geometry.total_bounds
extent = gpd.GeoDataFrame([[Polygon(
    [(minx - 2.5, miny - 1.5), (minx - 2.5, maxy + 1.5), (maxx + 2, maxy + 1.5), (maxx + 2, miny - 1.5),
     ])]], columns=['geometry']).set_crs(gdf.crs)
#m_extent = gdf1.intersection(extent.unary_union)
m_extent = gdf.clip(extent)
for y in experiment["Year"].unique().tolist():
    exp_year = experiment[experiment["Year"] == y]
    print(y)
    print(len(exp_year.index))
    try:
        maps = m_extent.plot(color='lightgrey', figsize=(20, 15), edgecolor='grey', )
        exp_year.plot(ax=maps, marker='o', column="counts", scheme="Quantiles", k=6,categorical=False, cmap="GnBu",
               linewidths=1, edgecolors='black',legend=True, markersize=120,
               legend_kwds={'loc': 'lower right', 'fontsize': 17}
                  )
        plt.xticks(fontsize=14, rotation=0)
        plt.yticks(fontsize=14, rotation=0)
        plt.margins(0, 0)
        plt.savefig(f'experiment_observation_{y}.jpg', dpi=500, bbox_inches=None, pad_inches=0.01, )
    except:
        pass

experiment_g = experiment_data[experiment_data["Experiment"] == 'GEH1']
minx, miny, maxx, maxy = experiment_g.geometry.total_bounds
extent = gpd.GeoDataFrame([[Polygon(
    [(minx - 1.5, miny - 1.5), (minx - 1.5, maxy + 1.5), (maxx + 1.5, maxy + 1.5), (maxx + 1.5, miny - 1.5),
     (minx - 1.5, miny - 1.5)])]], columns=['geometry']).set_crs(gdf.crs)
#m_extent = gdf1.intersection(extent.unary_union)
m_extent = gdf1.clip(extent)
for y in experiment_g["Year"].unique().tolist():
    exp_year = experiment_g[experiment_g["Year"] == y]
    maps = m_extent.plot(color='lightgrey', figsize=(20, 15), edgecolor='grey', )
    exp_year.plot(ax=maps, marker='o', column="counts", scheme="Quantiles", k=6,categorical=False, cmap="GnBu",
               linewidths=1, edgecolors='black',legend=True, markersize=120,
               legend_kwds={'loc': 'lower right', 'fontsize': 17}
                  )
    plt.xticks(fontsize=14, rotation=0)
    plt.yticks(fontsize=14, rotation=0)
    plt.margins(0, 0)
    plt.savefig(f'experiment_observation_germany_{y}.jpg', dpi=500,
                bbox_inches=None, pad_inches=0.01, )