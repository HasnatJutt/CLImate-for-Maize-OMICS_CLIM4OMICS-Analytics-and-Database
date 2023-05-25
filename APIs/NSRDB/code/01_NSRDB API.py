# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:33:04 2019

@author: psarzaeim2
"""

## Reading data from NSRDB website for certain lats and lons  
# =============================================================================
# Import necessary libraries
# =============================================================================
import os
import pandas as pd

# =============================================================================
# Input and Output directories
# =============================================================================
path = os.chdir ("../../../G2F data preprocessing/Meta/output/")
Input_dir = os.getcwd ().replace ("\\", "/")
Input_dir = Input_dir + "/"
Output_dir = os.chdir ("../../../APIs/NSRDB/output/Download/")
Output_dir = os.getcwd ().replace ("\\", "/")
Output_dir = Output_dir + "/"
print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)
    
# =============================================================================
# Define the year, lat, and lon of the experiments
# Enter the directory that year, lat, and lon od G2F experiments has been saved
# =============================================================================    
count_file = 0
df = pd.read_csv (Input_dir + "lat_lon.csv")
dF = df.dropna()
#print(dF)

for index, row in dF.iterrows():
    #print(row["Year"])
    year = str(row ["Year"])
    experiment = row ["Experiment"]
    
    lat = row ["lat"]
    lon = row ["lon"]

    # You must request an NSRDB api key from the link above
    api_key = 'GpdvuInieYc7m1sF5CEW3n9OVQjHX0nkbq6Ild6U'

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
    your_name = 'Parisa+Sarzaeim'
    # Your reason for using the NSRDB.
    reason_for_use = 'research'
    # Your affiliation
    your_affiliation = 'UNL'
    # Your email address
    your_email = 'parisa.sarzaeim@huskers.unl.edu'
    # Please join our mailing list so we can keep you up-to-date on new developments.
    mailing_list = 'true'
    # Declare url string
    url = 'https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
    # Return all but first 2 lines of csv to get data:
    df = pd.read_csv('https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes), skiprows=2)
    #Check
    #print("D1")
    
    df.index.name = "Record Number"
    df ["Date"] = df ["Year"].apply (str) + "/" + df ["Month"].apply(str) + "/" + df ["Day"].apply(str)
    df ["DOY"] = 1
    #Check
#    print("D2")
      
    for i in range (1, len(df)): 
#        print("D"+ str(i))
        #print(i)
        if df.Date.loc[i] == df.Date.loc[i-1]:
          #print(df.Date.loc[i])
            df ["DOY"].loc [i] = df ["DOY"].loc [i-1]
        elif df.Date.loc [i] != df.Date.loc [i-1]:          
            df ["DOY"].loc [i] = df ["DOY"].loc [i-1] + 1
#    print(df)

    # Set the time index in the pandas dataframe:
    #df = df.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=interval+'Min', periods=525600/int(interval)))

    # take a look
    count_file += 1
#    print ("count_file = ", count_file)
#    print ("year =", year)
#    print ("Experiment =", experiment)
#    print ('shape:',df.shape)
    
    # Saving the downloaded files
    df = df [["Year", "Month", "Day", "Hour", "Minute", "Date", "DOY", "Temperature", "Dew Point", "Relative Humidity", "GHI", "DHI", "DNI",
              "Precipitable Water", "Wind Speed", "Wind Direction", "Pressure"]]
    
    df.rename (columns = {"Year":"Year [Local]", "Month":"Month [Local]", "Day":"Day [Local]", "Hour":"Hour [Local]", "Minute":"Minute [Local]","Date":"Date [Local]", 
                          "DOY":"Day of Year [Local]", "Temperature":"Temperature [C]", "Dew Point":"Dew Point [C]", "Relative Humidity":"Relative Humidity [%]",
                          "GHI":"Solar Radiation [W/m2]", "DHI":"DHI [W/m2]", "DNI":"DNI [W/m2]", "Wind Speed":"Wind Speed [m/s]", "Wind Direction":"Wind Direction [degrees]",
                          "Precipitable Water":"Precipitable Water [mm]", "Pressure":"Pressure [mb]"}, inplace = True) 
    df.to_csv (Output_dir + year + str(experiment) + ".csv")