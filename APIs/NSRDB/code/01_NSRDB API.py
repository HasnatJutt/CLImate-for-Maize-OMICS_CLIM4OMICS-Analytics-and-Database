# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:33:04 2019

@author: psarzaeim2, Hasnat

Updated on May 2023
"""

## Reading data from NSRDB website for certain lats and lons  
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import sys
import glob
import argparse
import pandas as pd

##############################################################################
##############################################################################
############### User Inputs API Key User Name ################################
# Personal info
yourfirstname = None
yourlastname = None
# Your reason for using the NSRDB.
reasonforuse = None
# Your affiliation
youraffiliation = None
# Your email address
youremail = None
# Please join our mailing list so we can keep you up-to-date on new developments.
mailinglist = 'false'
# API key
apikey = None
##############################################################################
# =============================================================================
# Input and Output directories
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory from Current Path', required=False)
parser.add_argument('-o', '--output', help='Path of Output Directory from Current Path', required=False)
parser.add_argument('-fn', '--firstname', help='First Name', required=False)
parser.add_argument('-ln', '--lastname', help='Last Name', required=False)
parser.add_argument('-r', '--reason', help='Reason of Use', required=False)
parser.add_argument('-a', '--affiliation', help='Your Affiliation', required=False)
parser.add_argument('-e', '--email', help='Your Email', required=False)
parser.add_argument('-k', '--api', help='API Keys', required=False)
parser.add_argument('-m', '--mail', help='Mail list', required=False)
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
            Output_path = os.path.join(Input_path, '../../../APIs/NSRDB/output/Download')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../G2F data preprocessing/Meta/output/"):
    Input_dir = "../../../G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../APIs/NSRDB/output/Download'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("G2F data preprocessing/Meta/output/"):
    Input_dir = "G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'APIs/NSRDB/output/Download'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../G2F data preprocessing/Meta/output/"):
    Input_dir = "../G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../APIs/NSRDB/output/Download'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()

print("Input directory = ", Input_dir)
print("Output directory ", Output_dir)

# =============================================================================
# Define the year, lat, and lon of the experiments
# Enter the directory that year, lat, and lon od G2F experiments has been saved
# =============================================================================    
count_file = 0
df = pd.read_csv(os.path.join(Input_dir, "lat_lon.csv"))
dF = df.dropna()
# print(dF)

for index, row in dF.iterrows():
    # print(row["Year"])
    year = str(row["Year"])
    experiment = row["Experiment"]

    lat = row["lat"]
    lon = row["lon"]

    # You must request an NSRDB api key from the link above
    if apikey == '' or apikey == None:
        if args.api is None:
            print(f"No API Key is provided, provide API Key in argument or file")
        else:
            api_key = args.api
    else:
        if args.api is None:
            api_key = apikey
        else:
            api_key = args.api

    # Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
    attributes = 'air_temperature,dew_point,relative_humidity,ghi,dhi,dni,total_precipitable_water,wind_speed,wind_direction,surface_pressure'

    # Set leap year to true or false. True will return leap day data if present, false will not.
    leap_year = 'false'

    # Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
    interval = '30'

    # Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
    # NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
    # local time zone.
    utc = 'false'

    # Personal info
    if yourfirstname == '' or yourfirstname == None:
        if args.firstname is None:
            print(f"No first Name provided in the argument or in file")
        else:
            your_name = args.firstname + "+" + args.lastname
    else:
        if args.firstname is None:
            your_name = yourfirstname + "+" + yourlastname
        else:
            your_name = args.firstname + "+" + args.lastname
    if reasonforuse == '' or reasonforuse == None:
        if args.reason is None:
            print(f"No Reason for Use is provided in the argument or in file")
        else:
            reason_for_use = args.reason
    else:
        if args.reason is None:
            reason_for_use = reasonforuse
        else:
            reason_for_use = args.reason
    if youraffiliation == '' or youraffiliation == None:
        if args.affiliation is None:
            print(f"No Affiliation is provided in the argument or in file")
        else:
            your_affiliation = args.affiliation
    else:
        if args.affiliation is None:
            your_affiliation = youraffiliation
        else:
            your_affiliation = args.affiliation
    if youremail == '' or youremail == None:
        if args.email is None:
            print(f"No Email is provided in the argument or in file")
        else:
            your_email = args.email
    else:
        if args.email is None:
            your_email = youremail
        else:
            your_email = args.email
    if mailinglist == '' or mailinglist == None:
        if args.mail is None:
            mailing_list = 'false'
        else:
            mailing_list = args.mail
    else:
        if args.mail is None:
            mailing_list = mailinglist
        else:
            mailing_list = args.mail
    # Declare url string
    url = 'https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(
        year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email,
        mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
    # Return all but first 2 lines of csv to get data:
    df = pd.read_csv(
        'https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(
            year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email,
            mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key,
            attr=attributes), skiprows=2)
    # Check
    # print("D1")

    df.index.name = "Record Number"
    df["Date"] = df["Year"].apply(str) + "/" + df["Month"].apply(str) + "/" + df["Day"].apply(str)
    df["DOY"] = 1
    # Check
    #    print("D2")

    for i in range(1, len(df)):
        #        print("D"+ str(i))
        # print(i)
        if df.Date.loc[i] == df.Date.loc[i - 1]:
            # print(df.Date.loc[i])
            df["DOY"].loc[i] = df["DOY"].loc[i - 1]
        elif df.Date.loc[i] != df.Date.loc[i - 1]:
            df["DOY"].loc[i] = df["DOY"].loc[i - 1] + 1
    #    print(df)

    # Set the time index in the pandas dataframe:
    # df = df.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=interval+'Min', periods=525600/int(interval)))

    # take a look
    count_file += 1
    #    print ("count_file = ", count_file)
    #    print ("year =", year)
    #    print ("Experiment =", experiment)
    #    print ('shape:',df.shape)

    # Saving the downloaded files
    df = df[["Year", "Month", "Day", "Hour", "Minute", "Date", "DOY", "Temperature", "Dew Point", "Relative Humidity",
             "GHI", "DHI", "DNI",
             "Precipitable Water", "Wind Speed", "Wind Direction", "Pressure"]]

    df.rename(columns={"Year": "Year [Local]", "Month": "Month [Local]", "Day": "Day [Local]", "Hour": "Hour [Local]",
                       "Minute": "Minute [Local]", "Date": "Date [Local]",
                       "DOY": "Day of Year [Local]", "Temperature": "Temperature [C]", "Dew Point": "Dew Point [C]",
                       "Relative Humidity": "Relative Humidity [%]",
                       "GHI": "Solar Radiation [W/m2]", "DHI": "DHI [W/m2]", "DNI": "DNI [W/m2]",
                       "Wind Speed": "Wind Speed [m/s]", "Wind Direction": "Wind Direction [degrees]",
                       "Precipitable Water": "Precipitable Water [mm]", "Pressure": "Pressure [mb]"}, inplace=True)
    df.to_csv(os.path.join(Output_dir, year + str(experiment) + ".csv"))
