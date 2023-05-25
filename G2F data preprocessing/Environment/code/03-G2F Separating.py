# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 08:42:25 2019

@author: psarzaeim2, Hasnat

Updated on May 2023 
"""

## Controlling G2F weather data files and the columns names 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
import pathlib
import argparse
import numpy as np
import pandas as pd
from shutil import copyfile

# =============================================================================
# Input and Output directories
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory from Current Path', required=False)
parser.add_argument('-o', '--output', help='Path of Output Directory from Current Path', required=False)
parser.add_argument('-s', '--singlefile', help='Filename for single file processing, Do not include Directory Path',
                    required=False)
parser.add_argument('-m', '--meta', help='Path of Meta Files Input Directory from Current Path', required=False)
parser.add_argument('-p', '--pheno', help='Path of Phenotype Files Input Directory from Current Path', required=False)
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
            Output_path = os.path.join(Input_path, '../../../G2F data preprocessing/Environment/output/G2F Separating')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../G2F data preprocessing/Environment/output/Name Fixing"):
    Input_dir = "../../../G2F data preprocessing/Environment/output/Name Fixing"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../G2F data preprocessing/Environment/output/G2F Separating'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("G2F data preprocessing/Environment/output/Name Fixing"):
    Input_dir = "G2F data preprocessing/Environment/output/Name Fixing"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'G2F data preprocessing/Environment/output/G2F Separating'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../G2F data preprocessing/Environment/output/Name Fixing"):
    Input_dir = "../G2F data preprocessing/Environment/output/Name Fixing"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../G2F data preprocessing/Environment/output/G2F Separating'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print("Input directory = ", Input_dir)
print("Output directory ", Output_dir)

# =============================================================================   
# Control
# ============================================================================= 
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

if args.pheno is not None:
    Input_path2 = os.path.abspath(args.pheno)
    if os.path.exists(Input_path2):
        Input_dir2 = Input_path2
    else:
        print(
            f'The input directory {args.pheno} does not exists on system path. Correct the Input directory, provided directory has {Input_path2} path')

elif os.path.exists("../../../G2F data preprocessing/Phenotype/output"):
    Input_dir2 = "../../../G2F data preprocessing/Phenotype/output"

elif os.path.exists("G2F data preprocessing/Phenotype/output"):
    Input_dir2 = "G2F data preprocessing/Phenotype/output"

elif os.path.exists("../G2F data preprocessing/Phenotype/output"):
    Input_dir2 = "../G2F data preprocessing/Phenotype/output"
elif os.path.exists("../../G2F data preprocessing/Phenotype/output"):
    Input_dir2 = "../../G2F data preprocessing/Phenotype/output"
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

Env_list = []
Env_Experiments = glob.glob(os.path.abspath(os.path.join(Input_dir, '*.csv')))
for file in Env_Experiments:
    file_na = os.path.basename(file)[:-4]
    Env_list.append(file_na)
# print (Env_list)

Meta = pd.read_csv(os.path.abspath(os.path.join(Input_dir1, '0lat_lon.csv')))
Meta_list = Meta["Experiment_ID"].tolist()

Pheno = pd.read_csv(os.path.abspath(os.path.join(Input_dir2, '0YP1P2.csv')))
Pheno_list = Pheno["Experiment_ID"].tolist()

# Y = pd.read_csv (Input_dir2 + "Y.csv")
# Y_list = Y ["Experiment_ID"].tolist ()

# Shared = list (set (Env_list) & set (Meta_list) & set (Pheno_list) & set (Y_list))
Shared = list(set(Env_list) & set(Meta_list) & set(Pheno_list))
print("Number of Hybrid Experiments = ", len(Shared))

# Controlled Files
for filename in Env_Experiments:
    if os.path.basename(filename)[:-4] not in (Shared):
        os.remove(filename)

Meta_new = Meta[Meta["Experiment_ID"].isin(Shared)]
Meta_new.to_csv(os.path.abspath(os.path.join(Input_dir1, "lat_lon.csv")), index=None)

Pheno_new = Pheno[Pheno["Experiment_ID"].isin(Shared)]
Pheno_new.drop(["Experiment_ID"], axis=1, inplace=True)
Pheno_new.to_csv(os.path.abspath(os.path.join(Input_dir2, "YP1P2.csv")), index=None)

# Y_new = Y [Y ["Experiment_ID"].isin (Shared)]
# Y_new.drop (["Experiment_ID"], axis = 1, inplace = True)
# Y_new.to_csv (Input_dir2 + "Y.csv", index = None)

# =============================================================================
# Reading each experiment file as data frame
# =============================================================================
Env_Experiments = glob.glob(os.path.abspath(os.path.join(Input_dir, '*.csv')))
if args.singlefile is not None:
    Env_Experiments = [os.path.abspath(os.path.join(Input_dir, args.singlefile))]
else:
    pass
for filename in Env_Experiments:
    if os.path.basename(filename)[6] == "H":
        #    print(filename)
        #    print (Output_dir + filename)
        try:
            df = pd.read_csv(filename, low_memory=False)
        except:
            with open(filename, "r") as rawdata:
                encoding_name = rawdata.encoding
            df = pd.read_csv(filename, encoding=encoding_name, low_memory=False)

        #    print ("The experiment has {0} rows and {1} columns".format (df.shape [0],
        #           df.shape [1]))
        #
        #    print ("Are there missing values? {}".format(df.isnull().any().any()))

        # =============================================================================
        # Creating pivot tables for each variable in each experiment
        # =============================================================================
        # print(filename)
        "Temperature pivot table"
        try:
            df["Temperature [C]"] = pd.to_numeric(df["Temperature [C]"], errors='coerce')
            Temperature = df.groupby("Day of Year [Local]", as_index=True, dropna=False).agg({"Temperature [C]":["mean", "max", "min"]})
            Temperature.columns = Temperature.columns.to_flat_index()
            Temperature = df.pivot_table("Temperature [C]", index=["Day of Year [Local]"], dropna=False)
            Temperature["Min Temperature [C]"] = df.pivot_table("Temperature [C]", index=["Day of Year [Local]"],
                                                            aggfunc="min", dropna=False)
            Temperature["Max Temperature [C]"] = df.pivot_table("Temperature [C]", index=["Day of Year [Local]"],
                                                            aggfunc="max", dropna=False)
            MAX = Temperature.index.max()
            MIN = Temperature.index.min()
            lst = list(range(int(round(MIN, 0)), int(round(MAX + 1, 0))))
            Df = pd.DataFrame(lst)
            Df.rename(columns={Df.columns[0]: "Day of Year [Local]"}, inplace=True)
            common = Temperature.merge(Df, how="outer", on=["Day of Year [Local]"])
            common.sort_values(by="Day of Year [Local]", inplace=True)
            common.rename(columns={("Temperature [C]", "max"): "Max Temperature [C]",
                                   ("Temperature [C]", "min"): "Min Temperature [C]",
                                   ("Temperature [C]", "mean"): "Temperature [C]"}, inplace=True)
            common.to_csv(os.path.abspath(os.path.join(Output_dir, "T" + os.path.basename(filename))), index=None)
        except Exception as E:
            print(f"Following file {filename} is not processed for Temperature due to {E}")

        # =============================================================================
        "Dew Point pivot table"
        try:
            df["Dew Point [C]"] = pd.to_numeric(df["Dew Point [C]"], errors='coerce')
            Dew_Point = df.groupby("Day of Year [Local]", as_index=True, dropna=False).agg({"Dew Point [C]":["mean", "max", "min"]})
            Dew_Point.columns = Dew_Point.columns.to_flat_index()

            MAX = Dew_Point.index.max()
            MIN = Dew_Point.index.min()
            lst = list(range(int(round(MIN, 0)), int(round(MAX + 1, 0))))
            Df = pd.DataFrame(lst)
            Df.rename(columns={Df.columns[0]: "Day of Year [Local]"}, inplace=True)
            common = Dew_Point.merge(Df, how="outer", on=["Day of Year [Local]"])
            common.sort_values(by="Day of Year [Local]", inplace=True)
            common.rename(columns={("Dew Point [C]", "max"): "Max Dew Point [C]",
                                   ("Dew Point [C]", "min"): "Min Dew Point [C]",
                                   ("Dew Point [C]", "mean"): "Dew Point [C]"}, inplace=True)
            common.to_csv(os.path.abspath(os.path.join(Output_dir, "D" + os.path.basename(filename))), index=None)
        except Exception as E:
            print(f"Following file {filename} is not processed for Dew Point due to {E}")
        # =============================================================================
        "Relative Humidity pivot table"
        try:
            df["Relative Humidity [%]"] = pd.to_numeric(df["Relative Humidity [%]"], errors='coerce')
            Relative_Humidity = df.groupby("Day of Year [Local]", as_index=True, dropna=False).agg({"Relative Humidity [%]":["mean", "max", "min"]})
            Relative_Humidity.columns = Relative_Humidity.columns.to_flat_index()

            MAX = Relative_Humidity.index.max()
            MIN = Relative_Humidity.index.min()
            lst = list(range(int(round(MIN, 0)), int(round(MAX + 1, 0))))
            Df = pd.DataFrame(lst)
            Df.rename(columns={Df.columns[0]: "Day of Year [Local]"}, inplace=True)
            common = Relative_Humidity.merge(Df, how="outer", on=["Day of Year [Local]"])
            common.sort_values(by="Day of Year [Local]", inplace=True)
            common.rename(columns={("Relative Humidity [%]", "max"): "Max Relative Humidity [%]",
                                   ("Relative Humidity [%]", "min"): "Min Relative Humidity [%]",
                                   ("Relative Humidity [%]", "mean"): "Relative Humidity [%]"}, inplace=True)
            common.to_csv(os.path.abspath(os.path.join(Output_dir, "H" + os.path.basename(filename))), index=None)
        except Exception as E:
            print(f"Following file {filename} is not processed for Ralative Humidity due to {E}")

        # =============================================================================
        "Solar Radiation pivot table"
        try:
            df["Solar Radiation [W/m2]"] = pd.to_numeric(df["Solar Radiation [W/m2]"], errors='coerce')
            Solar_Radiation = df.groupby("Day of Year [Local]", as_index=True, dropna=False).agg({"Solar Radiation [W/m2]":["mean", "max", "min"]})
            Solar_Radiation.columns = Solar_Radiation.columns.to_flat_index()
            MAX = Solar_Radiation.index.max()
            MIN = Solar_Radiation.index.min()
            lst = list(range(int(round(MIN, 0)), int(round(MAX + 1, 0))))
            Df = pd.DataFrame(lst)
            Df.rename(columns={Df.columns[0]: "Day of Year [Local]"}, inplace=True)
            common = Solar_Radiation.merge(Df, how="outer", on=["Day of Year [Local]"])
            common.sort_values(by="Day of Year [Local]", inplace=True)
            common.rename(columns={("Solar Radiation [W/m2]", "max"): "Max Solar Radiation [W/m2]",
                                   ("Solar Radiation [W/m2]", "min"): "Min Solar Radiation [W/m2]",
                                   ("Solar Radiation [W/m2]", "mean"): "Solar Radiation [W/m2]"}, inplace=True)
            common.to_csv(os.path.abspath(os.path.join(Output_dir, "S" + os.path.basename(filename))), index=None)
        except Exception as E:
            print(f"Following file {filename} is not processed for Solar Radiation due to {E}")

        # =============================================================================
        "Rainfall pivot table"
        try:
            df["Rainfall [mm]"] = pd.to_numeric(df["Rainfall [mm]"], errors='coerce')
            Rainfall_G = df.groupby("Day of Year [Local]", as_index=True, dropna=False).agg({"Rainfall [mm]":"sum"})
            Rainfall_G.reset_index(inplace=True)
            Rainfall = Rainfall_G.groupby("Day of Year [Local]", as_index=True, dropna=False).agg({"Rainfall [mm]":["mean", "max", "min"]})
            Rainfall.columns = Rainfall.columns.to_flat_index()
            MAX = Rainfall.index.max()
            MIN = Rainfall.index.min()
            lst = list(range(int(round(MIN, 0)), int(round(MAX + 1, 0))))
            Df = pd.DataFrame(lst)
            Df.rename(columns={Df.columns[0]: "Day of Year [Local]"}, inplace=True)
            common = Rainfall.merge(Df, how="outer", on=["Day of Year [Local]"])
            common.sort_values(by="Day of Year [Local]", inplace=True)
            common.rename(columns={("Rainfall [mm]", "max"): "Max Rainfall [mm]",
                                   ("Rainfall [mm]", "min"): "Min Rainfall [mm]",
                                   ("Rainfall [mm]", "mean"): "Rainfall [mm]"}, inplace=True)
            if common["Rainfall [mm]"].max() > 800:
                max_values =common["Rainfall [mm]"].nlargest(3)
                if max_values.min() < 400:
                    common.drop(common[common["Rainfall [mm]"] > 500].index, axis= 0, inplace=True)
                    common.to_csv(os.path.abspath(os.path.join(Output_dir, "R" + os.path.basename(filename))),
                                  index=None)
                else:
                    pass
            elif common["Rainfall [mm]"].max() > 400:
                max_values =common["Rainfall [mm]"].nlargest(5)
                if max_values.min() < 400:
                    common.drop(common[common["Rainfall [mm]"] > 500].index, axis= 0, inplace=True)
                    common.to_csv(os.path.abspath(os.path.join(Output_dir, "R" + os.path.basename(filename))),
                                  index=None)
                else:
                    pass
            else:
                common.to_csv(os.path.abspath(os.path.join(Output_dir, "R" + os.path.basename(filename))), index=None)
        except Exception as E:
            print(f"Following file {filename} is not processed for Rainfall due to {E}")

        # =============================================================================
        "Wind Speed pivot table"
        try:
            df["Wind Speed [m/s]"] = pd.to_numeric(df["Wind Speed [m/s]"], errors='coerce')
            Wind_Speed = df.groupby("Day of Year [Local]", as_index=True, dropna=False).agg({"Wind Speed [m/s]":["mean", "max", "min"]})
            Wind_Speed.columns = Wind_Speed.columns.to_flat_index()
            MAX = Wind_Speed.index.max()
            MIN = Wind_Speed.index.min()
            lst = list(range(int(round(MIN, 0)), int(round(MAX + 1, 0))))
            Df = pd.DataFrame(lst)
            Df.rename(columns={Df.columns[0]: "Day of Year [Local]"}, inplace=True)
            common_W = Wind_Speed.merge(Df, how="outer", on=["Day of Year [Local]"])
            common_W.sort_values(by="Day of Year [Local]", inplace=True)
            common_W.rename(columns={("Wind Speed [m/s]", "max"): "Max Wind Speed [m/s]",
                                   ("Wind Speed [m/s]", "min"): "Min Wind Speed [m/s]",
                                   ("Wind Speed [m/s]", "mean"): "Wind Speed [m/s]"}, inplace=True)
            common_W.to_csv(os.path.abspath(os.path.join(Output_dir, "W" + os.path.basename(filename))), index=None)
        except Exception as E:
            print(f"Following file {filename} is not processed for Wind Speed due to {E}")

        # =============================================================================
        "Wind Direction pivot table"
        #    df.drop (df[df["Wind Direction [degrees]"] == "No Wind"].index, inplace = True)
        try:
            df["Wind Direction [degrees]"] = pd.to_numeric(df["Wind Direction [degrees]"], errors='coerce')
            Wind_Direction = df.groupby("Day of Year [Local]", as_index=True, dropna=False).agg({"Wind Direction [degrees]":["mean", "max", "min"]})
            Wind_Direction.columns = Wind_Direction.columns.to_flat_index()
            MAX = Wind_Direction.index.max()
            MIN = Wind_Direction.index.min()
            lst = list(range(int(round(MIN, 0)), int(round(MAX + 1, 0))))
            Df = pd.DataFrame(lst)
            Df.rename(columns={Df.columns[0]: "Day of Year [Local]"}, inplace=True)
            common_I = Wind_Direction.merge(Df, how="outer", on=["Day of Year [Local]"])
            common_I.sort_values(by="Day of Year [Local]", inplace=True)
            common_I.rename(columns={("Wind Direction [degrees]", "max"): "Max Wind Direction [degrees]",
                                   ("Wind Direction [degrees]", "min"): "Min Wind Direction [degrees]",
                                   ("Wind Direction [degrees]", "mean"): "Wind Direction [degrees]"}, inplace=True)
            common_I.to_csv(os.path.abspath(os.path.join(Output_dir, "I" + os.path.basename(filename))), index=None)
        except Exception as E:
            print(f"Following file {filename} is not processed for Wind Direction due to {E}")
        # =============================================================================
        "Wind Gust pivot table"
        try:
            df["Wind Gust [m/s]"] = pd.to_numeric(df["Wind Gust [m/s]"], errors='coerce')
            Wind_Gust = df.groupby("Day of Year [Local]", as_index=True, dropna=False).agg({"Wind Gust [m/s]":["mean", "max", "min"]})
            Wind_Gust.columns = Wind_Gust.columns.to_flat_index()
            MAX = Wind_Gust.index.max()
            MIN = Wind_Gust.index.min()
            lst = list(range(int(round(MIN, 0)), int(round(MAX + 1, 0))))
            Df = pd.DataFrame(lst)
            Df.rename(columns={Df.columns[0]: "Day of Year [Local]"}, inplace=True)
            common = Wind_Gust.merge(Df, how="outer", on=["Day of Year [Local]"])
            common.sort_values(by="Day of Year [Local]", inplace=True)
            common.rename(columns={("Wind Gust [m/s]", "max"):"Max Wind Gust [m/s]", ("Wind Gust [m/s]", "min"):"Min Wind Gust [m/s]", ("Wind Gust [m/s]", "mean"):"Wind Gust [m/s]"}, inplace=True)
            common.to_csv(os.path.abspath(os.path.join(Output_dir, "G" + os.path.basename(filename))), index=None)
        except Exception as E:
            print(f"Following file {filename} is not processed for Wind Gust due to {E}")
