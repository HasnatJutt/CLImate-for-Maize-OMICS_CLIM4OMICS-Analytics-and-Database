Goal: Checking the primary and secondary columns' names in G2F metafiles
URL = https://www.genomes2fields.org/
Models: (1) Meta_Primary_Secondary_Columns
Input: Meta raw files
Output: Meta_Files_Controlled files
The Primary Columns are the columns that must be available in the meta data raw files and the columns names should be like below:
Primary Columns Names: "Experiment", "lat", "lon"
Secondary Columns Names are the columns that must be created based on primary columns: "Year", "State", "Experiment_ID", "Experiment_Type"