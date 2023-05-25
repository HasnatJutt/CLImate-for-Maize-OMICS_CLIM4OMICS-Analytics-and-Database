Goal: Checking the primary and secondary columns, names in G2F phenotype files
URL = https://www.genomes2fields.org/
Models: (1) 01_Phenotype_Files_Primary_Columns, (2) 02_Phenotype_Files_Secondary_Columns
Input: Phenotypes raw files
Output: Phenotype_Files_Controlled files
The Primary Columns are the columns that must be available in the phenotype data raw files and the columns names should be like below:
Primary Columns Names: "Year", "Field-Location", "Pedigree", "Plant Height [cm]", "Ear Height [cm]", "Grain Moisture [%]", "Grain Yield [bu/A]"
Secondary Columns Names are the columns that must be created based on primary columns: "ID", "Year.x", "Loc.x", "Env.x", "Pedigree.x", "Year.y", Experiment", "P1", "P2"