Goal: Extracting and converting the raw G2F genetic data, applying PMV and MAF filters, and imputing data gaps.
URL = https://www.genomes2fields.org/
Models: (1) g2etransformation
Input: G2F_Genetic_Data raw file
Output: (1) GIDs2.csv, (2) NaNs.freq.csv, (3) percentage.NaNs.csv, (4) SNPs.csv, (5) X.csv
Genotypic variables: SNPs
To Run script file only change the Input and Output Directory path on line 21 and 23 OR place the script file (g2etransformation.py) file in the same folder where Input file (G2F_Genetic_Data) present.
If you don't want to re-write the files or save previous versions of file 