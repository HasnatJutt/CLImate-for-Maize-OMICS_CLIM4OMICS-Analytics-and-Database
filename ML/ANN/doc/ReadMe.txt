Goal: Implementing the deep neural networks to fulfill the gaps in "incomplete" G2F datasets.

For Temperature:
Model(s): (1) T_ANN
Input: Incomplete temperature files from "Database/output/T/"
Output: Predicted values files, loss values, and plots
Environmental variables: Temperature (T) includes Tmin, Tmean, and Tmax
Note 1: The defined abbreviation (Abb): T
Note 2: The unit: [C]

For Dew Point:
Model(s): (1) D_ANN
Input: Incomplete dew point files from "Database/output/D/"
Output: Predicted values files, loss values, and plots
Environmental variables: Dew point (D) includes Dmin, Dmean, and Dmax
Note 1: The defined abbreviation (Abb): D
Note 2: The unit: [C]

For Relative Humidity:
Model(s): (1) H_ANN
Input: Incomplete relative humidity files from "Database/output/H/"
Output: Predicted values files, loss values, and plots
Environmental variables: Relative humidity (H) includes Hmin, Hmean, and Hmax
Note 1: The defined abbreviation (Abb): H
Note 2: The unit: [%]

For Solar Radiation:
Model(s): (1) S_ANN
Input: Incomplete solar radiation files from "Database/output/S/"
Output: Predicted values files, loss values, and plots
Environmental variables: Solar radiation (S) includes Smin, Smean, and Smax
Note 1: The defined abbreviation (Abb): S
Note 2: The unit: [W/m2]

For Rainfall:
Model(s): (1) R_ANN
Input: Incomplete rainfall files from "Database/output/R/"
Output: Predicted values files, loss values, and plots
Environmental variables: Rainfall (R) includes Racc
Note 1: The defined abbreviation (Abb): R
Note 2: The unit: [mm]

For Wind Speed:
Model(s): (1) W_ANN
Input: Incomplete wind speed files from "Database/output/W/"
Output: Predicted values files, loss values, and plots
Environmental variables: Wind speed (W) includes Wmean
Note 1: The defined abbreviation (Abb): W
Note 2: The unit: [m/s]

For Wind Direction:
Model(s): (1) I_ANN
Input: Incomplete wind direction files from "Database/output/I/"
Output: Predicted values files, loss values, and plots
Environmental variables: Wind direction (I) includes Imean
Note 1: The defined abbreviation (Abb): I
Note 2: The unit: [degrees]

Note*: All of the fulfilled datasets using deep neural network in this step are saved into "Database/output/All_Files" directoty.
