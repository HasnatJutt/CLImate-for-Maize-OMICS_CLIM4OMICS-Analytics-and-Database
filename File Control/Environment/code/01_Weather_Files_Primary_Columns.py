# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:21:04 2019

@author: psarzaeim2, Hasnat

Updated on May 2023 
"""

## Controlling G2F weather data files and the columns names 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import glob
import re
import pathlib
import argparse
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory from Current Path', required=False)
parser.add_argument('-o', '--output', help='Path of Output Directory from Current Path', required=False)

parser.add_argument('-s', '--Station ID', help='Alternative Name for Station ID that exists in Data', required=False)
parser.add_argument('-e', '--Experiment', help='Alternative Name for Experiment that exists in Data', required=False)
parser.add_argument('-d', '--Day [Local]', help='Alternative Name for Day that exists in Data', required=False)
parser.add_argument('-y', '--Year [Local]', help='Alternative Name for Year that exists in Data', required=False)
parser.add_argument('-m', '--Month [Local]', help='Alternative Name for Month that exists in Data', required=False)
parser.add_argument('-t', '--Time [Local]', help='Alternative Name for Time that exists in Data', required=False)
parser.add_argument('-tmp', '--Temperature [C]', help='Alternative Name for Temperature that exists in Data', required=False)
parser.add_argument('-dp', '--Dew Point [C]', help='Alternative Name for Station ID that exists in Data', required=False)
parser.add_argument('-rh', '--Relative Humidity [%]', help='Alternative Name for Relative Humidity that exists in Data', required=False)
parser.add_argument('-sr', '--Solar Radiation [W/m2]', help='Alternative Name for Solar Radiation that exists in Data', required=False)
parser.add_argument('-r', '--Rainfall [mm]', help='Alternative Name for Rainfall that exists in Data', required=False)
parser.add_argument('-wd', '--Wind Direction [degrees]', help='Alternative Name for Wind Direction that exists in Data', required=False)
parser.add_argument('-ws', '--Wind Speed [m/s]', help='Alternative Name for Wind Speed that exists in Data', required=False)
parser.add_argument('-wg', '--Wind Gust [m/s]', help='Alternative Name for Wind Gust that exists in Data', required=False)
parser.add_argument('-da', '--Date', help='Alternative Name for Date that exists in Data', required=False)
parser.add_argument('-doy', '--Day of Year [Local]', help='Alternative Name for Day of Year [Local] that exists in Data', required=False)

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
            Output_path = os.path.join(Input_path,'../../File Control/Environment/output')
            Output_dir = output_fdir(Output_path)
    else:
        print(f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../File Upload/Environment"):
    Input_dir = os.path.abspath("../../../File Upload/Environment")
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../File Control/Environment/output'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("File Upload/Environment"):
    Input_dir = os.path.abspath("File Upload/Environment")
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'File Control/Environment/output'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("../File Upload/Environment"):
    Input_dir = os.path.abspath("../File Upload/Environment")
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../File Control/Environment/output'
        Output_dir = output_fdir(Output_path)

else:
    print("No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")

print ("Input directory = ", Input_dir)
print ("Output directory = ", Output_dir)
def column_identifier(col_name_list, identifier):
    """
    This function try to find the column names that are required by parital search and removing different parts of the string.
    It first use parial search if only one column found it rename it otherwise first it remove parenthesess and spaces and check.
    If more then one column have similar names then it try other methods.
    Args:
        col_name_list:
        identifier:

    Returns:
        identified_col_name
    """
    col_identy = identifier.lower()
    col_index = []
    col_index1 = []
    col_index2 = []
    for col in range(len(col_name_list)):
        if col_name_list[col].lower() == col_identy:
            col_index.append(col)
        elif col_name_list[col].lower() in col_identy:
            col_index1.append(col)
        elif col_identy in col_name_list[col].lower():
            col_index2.append(col)
        else:
            pass
    if len(col_index) == 1:
        identified_col_name = col_name_list[col_index[0]]
    elif len(col_index1) == 1 and len(col_index) == 0:
        identified_col_name = col_name_list[col_index1[0]]
    elif len(col_index2) == 1 and len(col_index) == 0 and len(col_index1) == 0:
        identified_col_name = col_name_list[col_index2[0]]
    else:
        col_identy = re.sub(r'[^0-9a-zA-Z]', '', identifier.lower())
        col_name_change = [re.sub(r'[^0-9a-zA-Z]', '', col) for col in col_name_list]
        col_name_change = [col.lower() for col in col_name_change]
        col_index = []
        col_index1 = []
        col_index2 = []
        for col in range(len(col_name_change)):
            if col_name_change[col] == col_identy:
                col_index.append(col)
            elif col_name_change[col] in col_identy:
                col_index1.append(col)
            elif col_identy in col_name_change[col]:
                col_index2.append(col)
            else:
                pass
        if len(col_index) == 1:
            identified_col_name = col_name_list[col_index[0]]
        elif len(col_index1) == 1 and len(col_index) == 0:
            identified_col_name = col_name_list[col_index1[0]]
        elif len(col_index2) == 1 and len(col_index) == 0 and len(col_index1) == 0:
            identified_col_name = col_name_list[col_index2[0]]
        else:
            col_identy = re.sub(r'[^a-zA-Z]', '', identifier.lower())
            col_name_change = [re.sub(r'[^a-zA-Z]', '',  col) for col in col_name_list]
            col_name_change = [col.lower() for col in col_name_change]
            col_index = []
            col_index1 = []
            col_index2 = []
            for col in range(len(col_name_change)):
                if col_name_change[col] == col_identy:
                    col_index.append(col)
                elif col_name_change[col] in col_identy:
                    col_index1.append(col)
                elif col_identy in col_name_change[col]:
                    col_index2.append(col)
                else:
                    pass
            if len(col_index) == 1:
                identified_col_name = col_name_list[col_index[0]]
            elif len(col_index1) == 1 and len(col_index) == 0:
                identified_col_name = col_name_list[col_index1[0]]
            elif len(col_index2) == 1 and len(col_index) == 0 and len(col_index1) == 0:
                identified_col_name = col_name_list[col_index2[0]]
            else:
                col_identy = re.sub(r'[^0-9a-zA-Z]', '', identifier.lower().split('[')[0])
                col_name_change = [re.sub(r'[^0-9a-zA-Z]', '' , col.lower().split(r'\W')[0]) for col in col_name_list]
                col_index = []
                col_index1 = []
                col_index2 = []
                for col in range(len(col_name_change)):
                    if col_name_change[col] == col_identy:
                        col_index.append(col)
                    elif col_name_change[col] in col_identy:
                        col_index1.append(col)
                    elif col_identy in col_name_change[col]:
                        col_index2.append(col)
                    else:
                        pass
                if len(col_index) == 1:
                    identified_col_name = col_name_list[col_index[0]]
                elif len(col_index1) == 1 and len(col_index) == 0:
                    identified_col_name = col_name_list[col_index1[0]]
                elif len(col_index2) == 1 and len(col_index) == 0 and len(col_index1) == 0:
                    identified_col_name = col_name_list[col_index2[0]]
                else:
                    col_identy = re.sub(r'[^a-zA-Z]', '' , identifier.lower().split('[')[0])
                    col_name_change = [re.sub(r'[^a-zA-Z]','' , col.lower().split(r'\W')[0]) for col in col_name_list]
                    col_index = []
                    col_index1 = []
                    col_index2 = []
                    for col in range(len(col_name_change)):
                        if col_name_change[col] == col_identy:
                            col_index.append(col)
                        elif col_name_change[col] in col_identy:
                            col_index1.append(col)
                        elif col_identy in col_name_change[col]:
                            col_index2.append(col)
                        else:
                            pass
                    if len(col_index) == 1:
                        identified_col_name = col_name_list[col_index[0]]
                    elif len(col_index1) == 1 and len(col_index) == 0:
                        identified_col_name = col_name_list[col_index1[0]]
                    elif len(col_index2) == 1 and len(col_index) == 0 and len(col_index1) == 0:
                        identified_col_name = col_name_list[col_index2[0]]
                    else:
                        identified_col_name = None
    return identified_col_name




# =============================================================================
# Read the weather files and check the columns names
# =============================================================================        
Defined_col_names = ["Station ID", "Experiment", "Day [Local]", "Month [Local]", "Year [Local]", "Time [Local]",
                     "Temperature [C]", "Dew Point [C]", "Relative Humidity [%]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Wind Speed [m/s]",
                     "Wind Direction [degrees]", "Wind Gust [m/s]", "Date"]

Weather_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
#print(Weather_files)
for filename in Weather_files:
    try:
        df = pd.read_csv (filename, low_memory=False)
    except:
        with open(filename, "r") as rawdata:
            encoding_name=rawdata.encoding
        df = pd.read_csv (filename, encoding=encoding_name, low_memory=False)
    col_name = df.columns.tolist()
    for defined_col in Defined_col_names:
        if defined_col not in col_name:
            if vars(args).get(defined_col) is not None:
                args_value = vars(args).get(defined_col)
                if args_value in col_name:
                    df.rename(columns={args_value: defined_col}, inplace=True)
                else:
                    possible_col_name = column_identifier(col_name, args_value)
                    if possible_col_name is not None:
                        df.rename(columns={possible_col_name: defined_col}, inplace=True)
                    else:
                        possible_col_name = column_identifier(col_name, defined_col)
                        if possible_col_name is not None:
                            df.rename(columns={possible_col_name: defined_col}, inplace=True)
                        else:
                            if defined_col=="Year [Local]" or defined_col=="Month [Local]" or defined_col=="Day [Local]":
                                if column_identifier(col_name, args.Date) is not None:
                                    if df[column_identifier(col_name, args.Date)].isna().count() > df.index.count()/2:
                                        df[defined_col] = None
                                    else:
                                        pass
                                elif column_identifier(col_name, "Date") is not None:
                                    if df[column_identifier(col_name, "Date")].isna().count() > df.index.count()/2:
                                        df[defined_col] = None
                                    else:
                                        pass
                                else:
                                    print(
                                        f"{defined_col} column is unrecognized in {filename}, {args.defined_col} is also not exits in {filename}, therefor it cannot be rename to {defined_col} And it is also not match with any possible name")
                            elif defined_col=="Date" or defined_col=="Day of Year [Local]":
                                df[defined_col]=None
                            else:
                                print(f"{defined_col} column is unrecognized in {filename}, {args.defined_col} is also not exits in {filename}, therefor it cannot be rename to {defined_col} And it is also not match with any possible name")
            else:
                possible_col_name = column_identifier(col_name, defined_col)
                if possible_col_name  is not None:
                    df.rename(columns={possible_col_name: defined_col}, inplace=True)
                else:
                    if defined_col == "Year [Local]" or defined_col == "Month [Local]" or defined_col == "Day [Local]":
                        if column_identifier(col_name, "Date") is not None:
                            if df[column_identifier(col_name, "Date")].isna().count() > df.index.count() / 2:
                                df[defined_col] = None
                            else:
                                pass
                        else:
                            print(
                                f"{defined_col} column is unrecognized in {filename}, {args.defined_col} is also not exits in {filename}, therefor it cannot be rename to {defined_col} And it is also not match with any possible name")

                    elif defined_col=='Date' or defined_col=="Day of Year [Local]":
                        df[defined_col]=None
                    else:
                        print (f"{defined_col} column is unrecognized in {filename}, please find the {defined_col} values column and rename it to {defined_col}")
        else:
            pass
    df["Day of Year [Local]"] = None
    col_name = df.columns.tolist()
    for col in col_name:
        if 'unname' in col.lower():
            df.drop([col], axis=1, inplace=True)
        else:
            pass
    for defined_col in col_name:
        try:
            if defined_col== "Day [Local]":
                if df["Day [Local]"].isna().count() > 0:
                    if df["Date"].isna().count() == 0:
                        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                        df["Day [Local]"] = df["Date"].dt.day
                    else:
                        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                        df.loc[df["Day [Local]"].isna(), "Day [Local]"]= df["Date"].dt.day
                df["Day [Local]"] = pd.to_numeric(df["Day [Local]"], errors='coerce')
                if df["Day [Local]"].max() > 31:
                    print(f"The {defined_col} column in {filename} has values greater than 31 that is due to some error or wrong column name")
                else:
                    pass
            elif defined_col == "Month [Local]":
                if df["Month [Local]"].isna().count() > 0:
                    if df["Date"].isna().count() == 0:
                        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                        df["Month [Local]"] = df["Date"].dt.month
                    else:
                        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                        df.loc[df["Month [Local]"].isna(), "Month [Local]"]= df["Date"].dt.month
                df["Month [Local]"] = pd.to_numeric(df["Month [Local]"], errors='coerce')
                if df["Month [Local]"].max() > 12:
                    print(f"The {defined_col} column in {filename} has values greater than 31 that is due to some error or wrong column name")
                else:
                   pass
            elif defined_col == "Year [Local]":
                if df["Year [Local]"].isna().count() > 0:
                    if df["Date"].isna().count() > 0:
                        p_year = re.split(r'[_\n\t\f\v\r ]+', filename)
                        for sub_string in p_year:
                            integers = re.sub(r'[^0-9]', '', sub_string)
                            if len(integers) == 4 and int(integers) > 2010 and int(integers) < 2100:
                                df["Year [Local]"] = integers
                                break
                            else:
                                pass
                    else:
                        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                        df["Year [Local]"] = df["Date"].dt.year
                df["Year [Local]"] = pd.to_numeric(df["Year [Local]"], errors='coerce')
                if df["Year [Local]"].max() > 2100:
                    print(f"The {defined_col} column in {filename} has values greater than 31 that is due to some error or wrong column name")
                else:
                    pass
            elif defined_col == "Date":
                if df["Date"].isna().count() > 0:
                    df["Date"] = df["Year [Local]"].apply(str) + "/" + df["Month [Local]"].apply(str) + "/" + df[
                        "Day [Local]"].apply(str)
                    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                else:
                    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            elif defined_col == "Day of Year [Local]":
                df["Day of Year [Local]"] = pd.to_numeric(df["Day of Year [Local]"], errors='coerce')
                if df["Day of Year [Local]"].isna().count() > 0:
                    if df["Date"].isna().count() > 0:
                        df["Date"] = df["Year [Local]"].apply(str) + "/" + df["Month [Local]"].apply(str) + "/" + df[
                        "Day [Local]"].apply(str)
                        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                        df ["Day of Year [Local]"] = df ["Date"].dt.dayofyear
                    else:
                       df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                       df ["Day of Year [Local]"] = df ["Date"].dt.dayofyear
                else:
                    pass
                if df["Day of Year [Local]"].max() > 366:
                    print(
                        f"The {defined_col} column in {filename} has values greater than 366 that is due to some error or wrong column name")
                else:
                    pass
            elif defined_col == "Relative Humidity [%]":
                df["Relative Humidity [%]"] = pd.to_numeric(df["Relative Humidity [%]"], downcast='float',
                                                            errors='coerce')
                df.loc[(df["Relative Humidity [%]"] < 0) | (
                            df["Relative Humidity [%]"] > 100), "Relative Humidity [%]"] = " "
            elif defined_col == "Solar Radiation [W/m2]":
                df["Solar Radiation [W/m2]"] = pd.to_numeric(df["Solar Radiation [W/m2]"], downcast='float',
                                                             errors='coerce')
                df.loc[(df["Solar Radiation [W/m2]"] < 0), "Solar Radiation [W/m2]"] = " "
            elif defined_col == "Rainfall [mm]":
                df["Rainfall [mm]"] = pd.to_numeric(df["Rainfall [mm]"], downcast='float', errors='coerce')
                df.loc[(df["Rainfall [mm]"] < 0), "Rainfall [mm]"] = " "
            elif defined_col == "Wind Direction [degrees]":
                df["Wind Direction [degrees]"] = pd.to_numeric(df["Wind Direction [degrees]"], downcast='float',
                                                               errors='coerce')
                df.loc[(df["Wind Direction [degrees]"] < 0) | (
                            df["Wind Direction [degrees]"] > 360), "Wind Direction [degrees]"] = " "
            else:
                pass
        except Exception as E:
            print(f"The following column {defined_col} of {filename} is not converted properly due to {E}")

    df.to_csv (os.path.abspath(os.path.join(Output_dir, os.path.basename(filename))), index = None)

