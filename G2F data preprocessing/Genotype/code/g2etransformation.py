#!/usr/bin/python
# -*- coding: utf-8 -*-
# created by Hasnat Aslam
""" g2etransformation docstrings
This Scripy Transform Genetic Data to G2E model
input files. This only take one Input file.

copyright reservered you can use and modify under FAIR Principles

Info:
    This module do not require any additional library or package.
    To run the script set data directories and mention name of 
    input and output files. data_input_dir is Input Data Directory 
    and data_output_dir is Output Data Directory. The Input default 
    file Name is Markers.txt. The output files Names are SNPs.csv, 
    X.csv, GIDs2.csv, NaNs.freq.csv and percentage.NaNs.csv.
    By default it delete already existed files with same name. 
    To save old versions set prev_file to yes. And to use 
    specific sufix for files st value for sufix_str, otherwise
    it will add today's date and time as sufix.
    The Script is tested on Windows and Linux.

Input:
    Only one input SNPs sequenced file in text format (.txt)

Return:
    Five output files all in comma seprated format (.csv)    
     
Parameters:
        Common:
            :data_input_dir: The Input directory location or path of Input Directory.
            :type data_input_dir: str
            :data_output_dir: The output directory location or path of Output Directory.
            :type data_output_dir: str
            :in_file: Input file name
            :type in_file: str
            :snp_file: First Output file name
            :type snp_file: str
            :gid_file: Second Output file name
            :type gid_file: str
            :freq_file: Third Output file name
            :type freq_file: str
            :precfreq_file: Fourth Output file name
            :type precfreq_file: str
            :x_file: First Fifth file name
            :type x_file: str
            
        Advance:
            :prev_file: Determine hold previous versions of files with same name or Not
            :type prev_file: str or bool
            :sufix_str: Suffix add in the filenames of already existed files with same name
            :type sufix_str: str
            :gene_limit: The value that is used how many number of genes or number of rows process
                (default is 100000. In G2F initiative 1577 gene exists or 1579 rows)
            :type gene_limit: int            
            :ignor_rows: The numbers of rows ignor or number of rows before header row. It shows 
                header header row location. (default is 1)
            :type ignor_rows: int             
            :start_keyword: The keyword use to identify starting position or gene name column 
                (default is marker)
            :type start_keyword: str    
            :col_check: Number of column used to search keyword (default value is 3 that search 4 columns)
            :type col_check: int
            :incase_multikey_no: The value that determine which column is use in case of multiple 
                keywords values within col_check limit (default is None)
            :type incase_multikey_no: int

ToDo:
    Compulsary:
        Set Input Directory Path in data_input_dir variable.
        Set Output Directory Path in data_output_dir variable.
        The default value for Input Directory is '../../../File Upload/Genotype'
        The default value for Output Dirctory is '../output'
    Optional:
        You can Change Input and output file names.
        Default Input file Name: 'Markers.txt'
        Default Output file Names: SNPs.csv, X.csv, GIDs2.csv, 
                                    NaNs.freq.csv and percentage.NaNs.csv.
    File Versions:
        To save alread existed files.
        Set prev_file: 'yes'
        To add sufix in the file name set sufix_str
        By default it not save the already existed files.
        The default value of sufix_str is datetime
    Advance parameters:
        Change these parameters in the function statement. 
            To set or process the particular number of rows or number of genes set gene_limit value.
            Default value of gene_limit: 100,000. 
                It means it will process upto 100,001 + ignor_rows. First 2nd row is header row. 
            To set how many rows ignor from the start of file set value of ignor_rows.
            Default value of ignor_row: 1.
            To set any specific keyword that used to identify first or starting row in file set 
                start_keyword value. And this column will use as first column in each row or gene name.
            Default value of start_keyword: marker
            The value of col_check is used to search the number of columns for keyword.
            Default value of col_check: 3
                It search first 4 columns for key word.            
            If keyword exists multiple times in mentioned number of columns then it will take last 
                column from col_check value. And if you want to use any specific column. 
                set value of incase_multikey_no.
            Default value of incase_multikey_no: None.                
 ToRun:
       python g2etransformation.py 
      
:python version: 3.7, 3.8, 3.9
:platform: windows, Linux 
       
 @author: Hasnat Aslam
 @copyright: Copyright 2022, HIH Group, SNR, University of Nebraska-Lincoln
 @license: GPLv3
 @version: 1.0
 @maintainer: Hasnat Aslam
 @email: hhasnat44868@gmail.com
 @status: Production
 @date: 2022/09/27
"""
# import libraries
try:
    import os
    import io
    import sys
    import profile
    import platform
    from multiprocessing import Process, Pool
    from csv import writer, reader
    from datetime import datetime
except ImportError:
    print('Libraries not found')
# To change other parameters change values in function
# Set input directory
data_input_dir = "../../../File Upload/Genotype"
# Set output directory
data_output_dir = "../output"
# Provide input or makers file name
in_file = os.path.join(data_input_dir, "Markers.txt").replace("\\", "/")
# Provide name of first output or SNPs file name
snp_file = os.path.join(data_output_dir, "SNPs.csv").replace("\\", "/")
# Provide name of meta output or Markers List file name
gid_file = os.path.join(data_output_dir, "GIDs2.csv").replace("\\", "/")
# Provide name of meta output or Nan Frequencies file name
freq_file = os.path.join(data_output_dir, "NaNs.freq.csv").replace("\\", "/")
# Provide name of meta output or Nan Frequency Percentage file name
precfreq_file = os.path.join(data_output_dir, "percentage.NaNs.csv").replace("\\", "/")
# Provide name of final output or G2E input file name
x_file = os.path.join(data_output_dir, "X.csv").replace("\\", "/")

## Preserve previous files with same names.
# You want to overwrite files or delete if exists then set value of prev_file to No otherwise set value to yes
prev_file = 'no'  # The values are yes or True and No or False
# Add the sufix you want to add in the ebd of your files otherwise today's date will be added
# Underscore _ between file name and suffix string will be added by default
sufix_str = ''
# Delete output files if already exits with the same name
def file_rmcheck(d_file,*args, **kwargs):
    if os.path.exists(d_file):
        try:
            if str(prev_file).lower() == 'yes' or str(prev_file).lower() == 'true':
                sfile_name = str(d_file).rsplit('.',1)
                if sufix_str == 'null' or sufix_str==None or sufix_str == '':
                    rename_file = sfile_name[0]+'_'+datetime.today().strftime('%Y_%m_%d')+'.'+sfile_name[1]
                    if os.path.exists(rename_file):
                        rename_file = sfile_name[0]+'_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.'+sfile_name[1]
                        print(f'Date and Time Stemp is included with the name of already existing files to save previous version')
                    os.rename(d_file,rename_file)
                else:
                    rename_file = sfile_name[0]+'_'+str(sufix_str)+'.'+sfile_name[1]
                    if os.path.exists(rename_file):
                        rename_file = sfile_name[0]+'_'+str(sufix_str)+'_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.'+sfile_name[1]
                        print(f'Date and Time Stemp is included with the name and suffix of already existing files to save previous version')
                    os.rename(d_file,rename_file)
            else:
                os.remove(d_file)
        except:
            os.remove(d_file)
    else:
        pass
def writecsv(out_filename, data_list, *args, **kwargs):
    with open(out_filename, 'w', newline='') as o_object:
        writer_object = writer(o_object, delimiter = ',')
        for r in data_list:
            writer_object.writerow([r])

""" The function takes input and output file names and produce required files
if you want to ignor more rows change ignor_rows value with desire number
if you want to limit the markers or rows change gene_limit values if you want to use uncomment
line 114 to 116. In current implementation it is not used.
if you want to cahnge header keyword or first key word in makers column change start_keyword
The start keyword compare using substring or partial string comparison. Thereofore it is not
case sensitive or full word may not required.
If you want to search keywords more than first 4 columns then change col_check value to desire no
incase if multiple start key words exits in search keywords columns than specify index which you
want to consider otherwise or by default it consider last column that has keyword from search columns.
"""
def datatransform(marker_file, out_snp, out_gids, out_freq,out_prec, out_x, gene_limit=100000, ignor_rows=1, start_keyword="marker", col_check=3,incase_multikey_no=None, *args, **kwargs):
    if os.path.exists(marker_file):
        #open SNPs output files using open function as append
        with open(out_snp, 'w', newline='') as snp_object:
            snp_writer = writer(snp_object, delimiter = ',')
            # open GIDs output file
            with open(out_gids, 'w', newline='') as gid_object:
                gid_writer = writer(gid_object, delimiter = ',')
                # open Markers file to read format, buffering=io.DEFAULT_BUFFER_SIZE is used to
                # optimize read file by adding buffer based on system
                with open(marker_file, 'r',buffering=io.DEFAULT_BUFFER_SIZE) as Lines:
                    # the following loop is use to negelect or pass rows or ignor rows equal to ignor_row value
                    for _ in range(ignor_rows):
                        next(Lines)
                    # it is use to identify header in the data using keyword
                    for j in Lines:
                        # it split data and convert list elements to lowercase. change col_check if you want to check more than first 4 values
                        ignor_word = [element.lower() for element in j.split('\t')[0:col_check]]
                        # it check if start_keyword is present in the list it match substrings.
                        start_keyword = start_keyword.lower()
                        # it return the keyword from ignor_word list by using partial string match
                        match_list = [string for string in ignor_word if start_keyword in string]
                        if len(match_list) > 0:
                        #if start_keyword in ignor_word:
                            # identify how many columns ignor based on key word. and provide data value started column
                            if incase_multikey_no is None:
                                # takes last column that has keyword
                                key_column = ignor_word.index(match_list[len(match_list)-1])
                            else:
                                # takes column based on incase_multikey_no and keyword
                                key_column = ignor_word.index(match_list[int(incase_multikey_no)-1])
                            start_columns = key_column + 1
                            # it writes header in SNPs files and ignors start key word if you want to ignor more columns change 1 to desire no and remove '\n' from last
                            snp_writer.writerow([''] + j.split('\t')[start_columns:-1] + [j.split('\t')[-1].rstrip('\n')])
                            # calulates total columns that contain data
                            total_columns = (len(j.split('\t')[start_columns:]))
                            # generate list of 0's that have lenght equal to number of data coulmns
                            nan_count = [0] * total_columns
                            list_mean = [0] * total_columns
                            nonnan_count = [0] * total_columns
                            gid_writer.writerow(['GIDs',''])
                            break
                        else:
                            pass
                        # use to break if want to restrict on particular column count    
                        if row_count == gene_limit+ignor_rows+1:
                            print(f'You reach the limit {gene_limit}. That is {gene_limit+ignor_rows+1} row in the file')
                            break    
                    row_count = 0
                    # iterate over rows and perform computation on rows
                    for i in Lines:
                        row_count = row_count + 1
                        col_index = 0
                        # write data into SNPs file
                        # Read last column and remove '\n' from the last
                        snp_writer.writerow([i.split(':')[key_column]] + i.split('\t')[start_columns:-1] + [i.split('\t')[-1].rstrip('\n')])
                        # write data into GIDs file or write only markers name and row number
                        gid_writer.writerow([i.split(':')[key_column]]+[row_count])
                        # iterate over columns
                        for col in i.split('\t')[start_columns:]:
                            # check Na or None values for each column of each row. it partially match string
                            if "N" in col or "n" in col  or col==' ':
                                # add one value at particular index of column in each iteration
                                nan_count[col_index] = nan_count[col_index] + 1
                            else:
                                # use to calculate mean value for each column. add value of cell at particular index
                                list_mean[col_index] = list_mean[col_index] + float(col)
                                # use to calculate total non-nan values in each column. if non-nan value add 1 at particular index
                                nonnan_count[col_index] = nonnan_count[col_index] + 1
                            col_index = col_index + 1
                        # use to break if want to restrict on particular column count
                        if row_count == gene_limit+ignor_rows+1:
                            print(f'You reach the limit {gene_limit}. That is {gene_limit+ignor_rows+1} row in the file')
                            break
                    if row_count==0:
                        print(f'The keyword: {start_keyword} not found in first: {col_check} columns. Increase col_check value or change start_keyword')
            gid_object.close()
        snp_object.close()
    else:
        print(f'The {marker_file} does not exists in the following path with following name therefore, check the file exists or correct file name or path')
    try:
        try:
            # calculate mean value for each column by ignoring NaN values
            col_mean = [x/y for x, y in zip(list_mean, nonnan_count)]
        except:
            nonnan_count_zero = nonnan_count.count(0)
            # Replace 0 with 1 in nonnan_count list to avoid ZeroDivisionError
            nonnan_count = list(map(lambda x: 1 if x==0 else x,  nonnan_count))
            print(f'{nonnan_count_zero} columns have 0 non-nan values in the column that replace with 1 to avoid ZeroDivisionError for Column Mean Calculation')
            # calculate mean value for each column by ignoring NaN values
            col_mean = [x/y for x, y in zip(list_mean, nonnan_count)]            
        # calculate total number of values in columns
        #col_tot = [x+y for x, y in zip(nan_count, nonnan_count)]
        del nonnan_count
        del list_mean
        del col_index
        # calculate unique values from NaN list of all columns
        nan_set = set(nan_count)
        #print(len(nan_set))
        # remove if 0 value exists
        nan_set.discard(0)
        #print(len(nan_set))
        # calculate percentage of Nan value using unique Nan value. Multiple value with 100 and divide by total row counts
        nan_perc = [i * 100/row_count for i in nan_set]
        # write NaN freq set to csv file using writecsv function. output file name and data list are function argments
        writecsv(out_freq,nan_set)
        # write NaN Percentage freq set to csv file using writecsv function. output file name and data list are function argments
        writecsv(out_prec,nan_perc)
        del nan_set
        del nan_perc
        # calculate nan_freq constant using row counts and multiple by 0.2. 0.2 is constant present in previous script
        nan_freq = row_count * 0.2
        # 0.03 is constant present in previous script
        maf = 0.03
        # calculate index of columns from list that has NaN values less or equal to nan_freq constant. add 1 to i to incorporate index in the data files column
        # the list start from data index and have no info of marker or first column the 0 index represent first data column but in file first data column is 1 therefore 1 added
        index_leq_nan = [i+1 for i, j in enumerate(nan_count) if j <= nan_freq]
        # sort the index list that has value
        index_leq_nan = sorted(index_leq_nan)
        # get the values form list that has column mean values using index_leq_nan index
        col_mean1 = [col_mean[index] for index in index_leq_nan]
        del col_mean
        # divide index of column mean values by 2. it is present in previous script
        col_means2 = [i/2 for i in col_mean1]
        del col_mean1
        # calculate p values if col_means2 value less or equal to 0.5 than value will remain same in col_mean2, if not than value will subtract from 1 and replace with
        # origional value. design using previous script
        p = [i if i<=0.5 else 1-i for i in col_means2]
        # calculate index from p list. the list index_3 has index of p that has value greater or equal to maf (0.03) constant
        index_3 = [i for i, j in enumerate(p) if j >= maf]
        #print(len(index_3))
        # sort index_3 values
        index_3 =sorted(index_3)
        # get the values from index_leq_nan based on the values of index_3. It takes values using index of p list
        colum = [index_leq_nan[index] for index in index_3]
        # 0 is appended to add maker names or 0 or Non-data column in output
        colum.append(0)
        colum = sorted(colum)
    except:
        print(f'The required list not created due to absence of data file or ignor_rows: {ignor_rows}, start_keyword: {start_keyword}, col_check: {col_check}, incase_multikey_no: {incase_multikey_no}')
    try:
        # open SNPs csv file and write into X.csv it writes only those coulmns that are present at particular index or colum list values. colum list values shows clumns index
        # in SNPs file
        with open(out_x, 'w', newline='') as x_object:
            x_writer = writer(x_object)
            with open(out_snp, 'r', newline='') as osnp_object:
                snp_reader = reader(osnp_object, delimiter=',')
                for lines in snp_reader:
                    x_writer.writerow([lines[index] for index in colum])
            osnp_object.close()
        x_object.close()
    except:
        print(f'The error is due to read of file{out_snp} or write of file{out_x} Please check read file is exitss')

# call the functions
if __name__ == '__main__':
    # create multiprocessing pool of 5
    with Pool(5) as p:
        # delete files if already exits using concurrent processing method
        p.map(file_rmcheck, [snp_file, gid_file, freq_file, precfreq_file, x_file])
        p.terminate()  
    datatransform(in_file, snp_file, gid_file, freq_file, precfreq_file, x_file)
    # use this line only if analyze performance and comment above one
    #profile.run('print(datatransform(in_file, snp_file, gid_file, freq_file, precfreq_file, x_file)); print()')
 #   if len(sys.argv)==2 and sys.argv[1]=='--help':
 #       print(__doc__)
