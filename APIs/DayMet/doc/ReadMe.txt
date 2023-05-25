Goal: Downloading climate data from DayMet
URL = https://daymet.ornl.gov/getdata
Variables: min temperature (C) max temperature (C), solar radiation (W/m2), precipitation (mm/day), water vapor pressure (Pa), 
	   snow water equivalent (kg/m2), day length (second/day)
Data type: Gridded
Spatial resolution: 1 km*1 km
Temporal resolution: Daily
Time span: 1980-the most recent published year
Model(s): (1) 01_DayMet Preprocessing, (2) 02_DayMet API, (3) 03_DayMet Cleaning, (4) 04_DayMet Postprocessing
Input: lat_lon.csv file
Output: (1) Download, (2) Clean, (3) DayMet