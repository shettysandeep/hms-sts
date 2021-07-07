#-*-coding: utf-8-*-
"""
__author__: Sandeep Shetty
__date__: July 06, 2021

Code cleans up the almost-raw data combined in or_parsing_data.py. Here we have
to reduce the columns relevant for auditing, namely, admission date, discharge
date, procedure, and the identifiers. In this code after filtering all the
columns we will also rename them to combine the dataset.
Eventually, this code will produce dataset with the following columns
[id, mrn, gender, admit date, surgery date, discharge date, procedure]

"""
import os, re
import pandas as pd
from datetime import datetime

if __name__ == '__main__':

    # File path
    FLDR_PTH = '/Users/sandeep/Documents/1-PROJECTS/sts/reports'
    FILE_NAME = 'OR_combined_data_2021_07_06-0403PM.csv'
    OUT_PTH = r'/Users/sandeep/Documents/1-PROJECTS/sts/reports'

    CSV_FILE = os.path.join(FLDR_PTH, FILE_NAME)

    # ~~~ Step 1.
    # Read the files with the columns to use
    # Create list of columns to drop from datafile above
    # Create list of Columns to rename from datafile above
    all_columns = pd.read_csv('../reports/Rename_columns_file.csv')
    cols_to_drop = all_columns[
        all_columns.New_names.isnull()]['Old_names'].tolist()
    cols_to_rename = all_columns[all_columns.New_names.notnull()]
    # Dictionary of renaming columns
    old_new_cols = dict(
        zip(cols_to_rename.Old_names.tolist(),
            cols_to_rename.New_names.tolist()))

    # ~~~~ Step 2
    # Import the main dataset (roughly combined)
    # Remove unnecessary columns (cols_to_drop)
    # Rename columns name (cols_to_rename) using the dictionary created in (old_new_cols)

    datafile = pd.read_csv(CSV_FILE, low_memory=False)
    datafile.drop(columns=cols_to_drop, inplace=True)
    datafile.rename(columns=old_new_cols, inplace=True)
    datafile.drop(columns="Unnamed: 0", inplace=True)

    # ~~~ Convert dtypes
    # Convert all time variable into time
    date_columns = datafile.columns[datafile.columns.str.contains('dt')]
    non_date_cols = datafile.columns[~datafile.columns.str.contains('dt')]
    for cols in date_columns:
        datafile[cols] = datafile[cols].apply(pd.to_datetime, errors='coerce')

    def combine_cols(pd_dat, name_comb_col, col_name_search):
        """Combining all similarly titles variables"""
        temp_cols = pd_dat.columns.str.contains(col_name_search)
        pd_dat[name_comb_col] = pd_dat.iloc[:, temp_cols].max(axis=1)
        return pd_dat

    def drop_cols(pd_dat, del_col_names):
        """drop columns that contain the text in del_col_names"""
        try:
            if isinstance(del_col_names, list):
                for items in del_col_names:
                    temp_cols = pd_dat.columns.str.contains(items)
                    pd_dat.drop(columns=pd_dat.columns[temp_cols],
                                inplace=True)
        except:
            print('del_col_names must be a list')
        return pd_dat

    # combine columns with dates - admit, surgery, discharge
    datafile = combine_cols(datafile, 'admission_dt', 'admit_dt')
    datafile = combine_cols(datafile, 'surgery_dt', 'surg_dt')
    datafile = combine_cols(datafile, 'discharge_dt', 'disch_dt')
    # delete date columns after combining
    datafile = drop_cols(pd_dat=datafile,
                         del_col_names=['admit_dt', 'surg_dt', 'disch_dt'])
    # drop all columns with no values
    datafile.dropna(how="all", axis=1, inplace=True)

    # combine columns with procedure description
    datafile = combine_cols(datafile, 'surgery_procedure', 'proc')
    # drop columns with procedure
    datafile = drop_cols(pd_dat=datafile,
                         del_col_names=['proc'])

    print(datafile['surgery_procedure'].head())

    # datafile.iloc[:,datafile.columns.str.contains('gender')].to_csv(os.path.join(OUT_PTH,'gender.csv'))
    # datafile.to_csv(os.path.join(OUT_PTH,'Test_ki_maa.csv'))
