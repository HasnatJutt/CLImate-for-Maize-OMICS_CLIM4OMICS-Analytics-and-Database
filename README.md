# CLImate-for-Maize-OMICS_CLIM4OMICS-Analytics-and-Database
CLImate for Maize OMICS: CLIM4OMICS Analytics and Database developed for GxE models under G2F initiative

CLIM4OMICS Analytics and Database is Improved database of G2F data repository that contains OMICs (genetic and phenotypic) and environmental data for maize yield predictability across 84 experimental fields in the U.S. and province of ON in Canada between 2014-2021. The goal of this pipeline is to aggregate, improve, and synthesize multi-dimensional G2F data including Geno-type, Phenotype and Environmental data for GxE modeling. This dataset contains 79,122 phenotype measurements, 378 genotypes of maize lines, environmental data of 178 locations and Python Scripts for Quality control (QC), Consistency control (CC) steps and ML models for GxE interactions. The Environmental data is extracted from NWS, DayMet and NSRDB databases and processed for QC and CC. The environmental dataset contains the minimum temperature (Tmin), average temperature (Tmean), maximum temperature (Tmax), minimum dew point (DPmin), average dew point (DPmean), maximum dew point (DPmax), minimum relative humidity (RHmin), average relative humidity (RHmean), maximum relative humidity (RHmax), minimum solar radiation (SRmin), average solar radiation (SRmean), maximum solar radiation (SRmax), accumulative rainfall (Racc), average wind speed (WSmean), and average wind direction (WDmean). This package also contains the raw G2F data and preprocessing pipeline.

# To Run all scripts Follow one of the following steps

In every directory open doc directory it has all the instructions to run scripts present in that directory.
If you follow the same diectory structure then you don't need to provide system arguments to set input and out put directories. The script also search folder name in current and parent directories. If you want to create output in some other place or use different name or location of input data, then you have to provide input and output directories path in sys arguments.
You only have to create input directory if you want to run all the scripts step-by-step then scripts will create and read ouput directories.
**File Upload** folder contains raw input data.  Download all af the genetic, phenotypic, environmental, and meta files from G2F website and save into the "File Upload" folder and read the "ReadMe.txt" file in the "doc" folder.
Use the following sequence to run all the scripts
There are follwoing steps:
1. File Upload
1. File Control
1. G2F data preprocessing
1. APIs
1. Database
1. ML
1. Selection
1. Control

* *Note 1: After implmeneting above steps in a row, the final improved environmental database is saved into "Database/output/All_Files".* *
