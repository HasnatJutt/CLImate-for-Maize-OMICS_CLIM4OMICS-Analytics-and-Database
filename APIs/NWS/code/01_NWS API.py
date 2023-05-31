from __future__ import print_function
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:24:04 2019

@author: psarzaeim2, Hasnat

Updated on May 2023
"""

## Reading data from IEM website for certain NWS station names 
# =============================================================================
# Import necessary libraries
# =============================================================================
import csv
import os
import sys
import argparse
import json
import time
import datetime
import pandas as pd
from urllib.request import urlopen

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Path of Input Directory from Current Path', required=False)
parser.add_argument('-o', '--output', help='Path of Output Directory from Current Path', required=False)
parser.add_argument('-m', '--metafile', help='Path of Lat Lon text file from Current Path', required=False)
parser.add_argument('-sy', '--startyear', help='Start Year e.g 1980', required=False)
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
            Output_path = os.path.join(Input_path, '../../../APIs/NWS/output/Download')
            Output_dir = output_fdir(Output_path)
    else:
        print(
            f'The input directory {args.input} does not exists on system path. Correct the Input directory, provided directory has {Input_path} path')

elif os.path.exists("../../../G2F data preprocessing/Meta/output/"):
    Input_dir = "../../../G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../../../APIs/NWS/output/Download'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("G2F data preprocessing/Meta/output/"):
    Input_dir = "G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = 'APIs/NWS/output/Download'
        Output_dir = output_fdir(Output_path)
elif os.path.exists("../G2F data preprocessing/Meta/output/"):
    Input_dir = "../G2F data preprocessing/Meta/output/"
    if args.output is not None:
        Output_dir = output_fdir(args.output)
    else:
        Output_path = '../APIs/NWS/output/Download'
        Output_dir = output_fdir(Output_path)
else:
    print(
        "No input directory is provided in arguments and directory is not exits on possible locations. Provide the directory in arguments or create directories based on instructions")
    sys.exit()

print("Input directory = ", Input_dir)
print ("Output directory ", Output_dir)


# Number of attempts to download data
MAX_ATTEMPTS = 6
# HTTPS here can be problematic for installs that don't have Lets Encrypt CA
SERVICE = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
#
#
def download_data(uri):
    """Fetch the data from the IEM
    The IEM download service has some protections in place to keep the number
    of inbound requests in check. This function implements an exponential
    backoff to keep individual downloads from erroring.
    Args:
      uri (string): URL to fetch
    Returns:
      string data
    """
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        try:
            data = urlopen(uri, timeout=300).read().decode('utf-8')
            if data is not None and not data.startswith('ERROR'):
                return data
        except Exception as exp:
            print("download_data(%s) failed with %s" % (uri, exp))
            time.sleep(5)
        attempt += 1

    print("Exhausted attempts to download, returning empty data")
    return ""


def get_stations_from_filelist(filename):
    """Build a listing of stations from a simple file listing the stations.
    The file should simply have one station per line.
    """
    stations = []
    for line in open(filename):
        stations.append(line.strip())
    return stations


def get_stations_from_networks():
    """Build a station list by using a bunch of IEM networks."""
    stations = []
    df = pd.read_csv(os.path.join(Input_dir, "lat_lon.csv"), index_col = "Experiment")
    states = df["State"].unique()

    # IEM quirk to have Iowa AWOS sites in its own labeled network
    networks = ['AWOS']
    for state in states:
        networks.append("%s_ASOS" % (state,))

    for network in networks:
        # Get metadata
        uri = ("https://mesonet.agron.iastate.edu/"
               "geojson/network/%s.geojson") % (network,)
        data = urlopen(uri)
        jdict = json.load(data)
        for site in jdict['features']:
            stations.append(site['properties']['sid'])
    return stations


def main():
    """Our main method"""
    # timestamps in UTC to request data for
    startts = datetime.datetime(2014, 1, 1)
    endts = datetime.datetime(2017, 12, 1)

    service = SERVICE + "data=all&tz=Etc/UTC&format=comma&latlon=yes&"

    service += startts.strftime('year1=%Y&month1=%m&day1=%d&')
    service += endts.strftime('year2=%Y&month2=%m&day2=%d&')

    # Two examples of how to specify a list of stations
    stations = get_stations_from_networks()
    # stations = get_stations_from_filelist("mystations.txt")
    for station in stations:
        uri = '%s&station=%s' % (service, station)
#        print('Downloading: %s' % (station, ))
        data = download_data(uri)
        outfn = station
        
        out = open(os.path.join(Output_dir, outfn), 'w')
        out.write(data)
        out.close()
        with open(os.path.join(Output_dir, outfn), 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)
            with open(os.path.join(Output_dir, outfn + ".csv"), 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerows(lines)
#                print("Save")
        

if __name__ == '__main__':
    main()