Goal: Categorizing the G2F datasets to "complete", "empty", "incomplete" files, creating environmental databases from G2F, NSRDB, DayMet, and NWS ready for data gaps fulfillment, and quntifyting the uncertainty.

For Temperature:
Model(s): (1) T_Database, (2) T_uncertainty
Input: Weather_Files_Controlled from G2F data preprocessing and APIs
Output: (1) Weather files in each category and the plots, (2) The uncertainty plots in folder of "T"
Environmental variables: Temperature (T) includes Tmin, Tmean, and Tmax
Note 1: The defined abbreviation (Abb): T
Note 2: The unit: [C]

For Dew Point:
Model(s): (1) D_Database, (2) D_uncertainty
Input: Weather_Files_Controlled from G2F data preprocessing and APIs
Output: (1) Weather files in each category and the plots, (2) The uncertainty plots in folder of "D"
Environmental variables: Dew point (D) includes Dmin, Dmean, and Dmax
Note 1: The defined abbreviation (Abb): D
Note 2: The unit: [C]

For Relative Humidity:
Model(s): (1) H_Database, (2) H_uncertainty
Input: Weather_Files_Controlled from G2F data preprocessing and APIs
Output: (1) Weather files in each category and the plots, (2) The uncertainty plots in folder of "H"
Environmental variables: Relative humidity (H) includes Hmin, Hmean, and Hmax
Note 1: The defined abbreviation (Abb): H
Note 2: The unit: [%]

For Solar Radiation:
Model(s): (1) S_Database, (2) S_uncertainty
Input: Weather_Files_Controlled from G2F data preprocessing and APIs
Output: (1) Weather files in each category and the plots, (2) The uncertainty plots in folder of "S"
Environmental variables: Solar radiation (S) includes Smin, Smean, and Smax
Note 1: The defined abbreviation (Abb): S
Note 2: The unit: [W/m2]

For Rainfall:
Model(s): (1) R_Database, (2) R_uncertainty
Input: Weather_Files_Controlled from G2F data preprocessing and APIs
Output: (1) Weather files in each category and the plots, (2) The uncertainty plots in folder of "R"
Environmental variables: Rainfall (R) includes Racc
Note 1: The defined abbreviation (Abb): R
Note 2: The unit: [mm]

For Wind Speed:
Model(s): (1) W_Database, (2) W_uncertainty
Input: Weather_Files_Controlled from G2F data preprocessing and APIs
Output: (1) Weather files in each category and the plots, (2) The uncertainty plots in folder of "W"
Environmental variables: Wind speed (W) includes Wmean
Note 1: The defined abbreviation (Abb): W
Note 2: The unit: [m/s]

For Wind Direction:
Model(s): (1) I_Database, (2) I_uncertainty
Input: Weather_Files_Controlled from G2F data preprocessing and APIs
Output: (1) Weather files in each category and the plots, (2) The uncertainty plots in folder of "I"
Environmental variables: Wind direction (I) includes Imean
Note 1: The defined abbreviation (Abb): I
Note 2: The unit: [degrees]

Note*: The "All_Files" folder is the final folder containing all of the files. The "complete" dataset for each variable are directly saved into "All_Files" folder in this step.
The "empty" datasets for each variable are fulfilled and saved into "All_Files" folder in this stage. 
The "incomplete" datasets will be fulfilled in the next step (ML) and then will be saved into "All_Files" folder.
