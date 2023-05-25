Goal: Downloading climate data from NSRDB
URL = https://maps.nrel.gov/nsrdb-viewer/?aL=UdPEX9%255Bv%255D%3Dt%26f69KzE%255Bv%255D%3Dt%26f69KzE%255Bd%255D%3D1&bL=clight&cE=0&lR=0&mC=4.740675384778373%2C22.8515625&zL=2
Variables: temperature (C), dew point (C), relative humidity (%), GHI (Global Horizontal Irradiance) (W/m2), DNI (Direct Normal Irradiance) (W/m2), DHI (Diffuse Horizontal Irradiance) (W/m2), 
	   wind speed (m/s), wind direction (degrees), precipitable water (mm), pressure (mbar)
Data type: Gridded
Spatial resolution: 4 km*4 km
Temporal resolution: 30-min
Time span: 1998-2018 (it may be updated)
Model(s): (1) 01_NSRDB API, (2) NSRDB Postprocessing
Input: lat_lon.csv file
Output: (1) Download, (2) NSRDB