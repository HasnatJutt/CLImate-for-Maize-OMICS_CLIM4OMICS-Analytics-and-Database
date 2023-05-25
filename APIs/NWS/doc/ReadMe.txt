Goal: Downloading climate data from NWS
URL = https://mesonet.agron.iastate.edu/request/download.phtml
Variables: temperature [C], dew point [C], relative humidity [%], rainfall[mm], wind speed [m/s], wind direction [degrees], vapor pressure [mb]
Data type: Station
Spatial resolution:-
Temporal resolution: 30-min
Model(s): (1) 01_NES API, (2) NWS Cleaning, (3) 03_NWS Nearest Station, (4) NWS Postprocessing
Input: lat_lon.csv file
Output: (1) Clean, (2) Download