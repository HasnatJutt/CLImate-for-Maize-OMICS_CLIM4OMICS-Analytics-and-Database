# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:43:32 2020
@author: psarzaeim2, Hasnat

Updated on May 2023 
"""

## Controlling G2F weather data files and the columns names 
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import re
import glob
import pathlib
import argparse
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory from Current Path', required=False)
parser.add_argument('-o', '--output', help='Path of Output Directory from Current Path', required=False)

parser.add_argument('-e', '--Experiment', help='Alternative Name for Experiment that exists in Data', required=False)
parser.add_argument('-la', '--lat', help='Alternative Name for Latitude that exists in Data', required=False)
parser.add_argument('-lo', '--lon', help='Alternative Name for Longitude that exists in Data', required=False)
parser.add_argument('-y', '--Year', help='Alternative Name for Year that exists in Data', required=False)

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
            Output_path = os.path.join(Input_path,'../../File Control/Meta/output')
            Output_dir = output_fdir(Output_path)
    else:
        print(f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../File Upload/Meta"):
    Input_dir = os.path.abspath("../../../File Upload/Meta")
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../File Control/Meta/output'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("File Upload/Meta"):
    Input_dir = os.path.abspath("File Upload/Meta")
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'File Control/Meta/output'
        Output_dir = output_fdir(Output_path)  
elif os.path.exists("../File Upload/Meta"):
    Input_dir = os.path.abspath("../File Upload/Meta")
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../File Control/Meta/output'
        Output_dir = output_fdir(Output_path)
else:
    print("No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")


print ("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)

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
# Read the meta files and create the columns names
# =============================================================================        
Defined_col_names = ["Experiment", "lat", "lon", "Year"]

Meta_files = glob.glob(os.path.abspath(os.path.join(Input_dir,'*.csv')))
#print(Meta_files)
for filename in Meta_files:
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
                            if defined_col=="Year":
                                df[defined_col]=None
                            else:
                                print(f"{defined_col} column is unrecognized in {filename}, {args.defined_col} is also not exits in {filename}, therefor it cannot be rename to {defined_col} And it is also not match with any possible name")
            else:
                possible_col_name = column_identifier(col_name, defined_col)
                if possible_col_name  is not None:
                    df.rename(columns={possible_col_name: defined_col}, inplace=True)
                else:
                    if defined_col == "Year":
                        df[defined_col] = None
                    else:
                        print(f"{defined_col} column is unrecognized in {filename}, please find the {defined_col} values column and rename it to {defined_col}")
        else:
            pass

    df = df[Defined_col_names]
    col_name = df.columns.tolist()
    for col in col_name:
        if 'unname' in col.lower():
            df.drop([col], axis=1, inplace=True)
        else:
            pass
    for defined_col in col_name:
        try:
            if defined_col == "Year":
                if df["Year"].isna().count() > 0:
                    p_year = re.split(r'[_\n\t\f\v\r ]+', filename)
                    for sub_string in p_year:
                        integers = re.sub(r'[^0-9]', '', sub_string)
                        if len(integers) == 4 and int(integers) > 2010 and int(integers) < 2100:
                            df["Year"] = integers
                            break
                        else:
                            pass
                else:
                    pass
                df["Year"] = pd.to_numeric(df["Year"], errors='coerce')
                if df["Year"].max() > 2100:
                    print(f"The {defined_col} column in {filename} has values greater than 31 that is due to some error or wrong column name")
                else:
                    pass
            elif  defined_col == "lat" or defined_col == "lon":
                df[defined_col] = pd.to_numeric(df[defined_col], errors='coerce')
            else:
                pass
        except Exception as E:
            print(f"The following column {defined_col} of {filename} is not converted properly due to {E}")
    try:
        df["State"] = df["Experiment"].str[:2]
        df["Experiment_ID"] = df["Year"].astype('str') + df["Experiment"]
        df["Experiment_Type"] = df["Experiment"].str[2]
        df.to_csv (os.path.abspath(os.path.join(Output_dir, os.path.basename(filename))), index = None)
    except Exception as E:
        print(f"The following file {os.path.basename(filename)} is not processed due to exception {E}")