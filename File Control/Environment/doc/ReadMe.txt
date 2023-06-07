Goal: Checking the primary and secondary columns' names in G2F environmental (weather) files and also controling and removing the values out of range for each variable (False values).
URL = https://www.genomes2fields.org/
Models: (1) Weather_Primary_Secondary_Control
Input: G2F_Weather_Data raw files
Output: G2F_weather_Data_Controlled files
The Primary Columns are the columns that must be available in the weather data raw files and the columns names should be like below:
Primary Columns Names: "Station ID", "Experiment(s)", "Day [Local]", "Month [Local]", "Year [Local]", Time [Local]", "Temperature [C]",
			"Dew Point [C]", "Relative Humidity [%]", "Solar Radiation [W/m2]", "Rainfall [mm]", "Wind Speed [m/s]", 
			"Wind Direction [degrees]", "Wind Gust [m/s]"
Secondary Columns Names are the columns that must be created based on primary columns: "Record Number", "Day of Year [Local]"