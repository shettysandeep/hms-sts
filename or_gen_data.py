#-*-coding: utf-8-*-
"""
__author__: Sandeep Shetty
__date__: July 06, 2021

Code cleans up the almost-raw data obtained from or_parsing_data.py. Selects
only the  columns that are relevant for auditing, namely, admission date, discharge
date, procedure, and the identifiers.

Similar columns are pooled together. The final resulting dataset will have the
following columns --

 [id, mrn, gender, admit date, surgery date, discharge date, procedure]

"""
import os, re
import pandas as pd
from datetime import datetime


def combine_cols(pd_dat, name_comb_col, col_name_search, func):
    """Combining all similarly titles variables"""
    temp_cols = pd_dat.columns.str.contains(col_name_search)
    pd_dat[name_comb_col] = pd_dat.iloc[:, temp_cols].apply(func, axis=1)
    return pd_dat


def drop_cols(pd_dat, del_col_names):
    """drop columns that contain the text in del_col_names"""
    try:
        if isinstance(del_col_names, list):
            for items in del_col_names:
                temp_cols = pd_dat.columns.str.contains(items)
                pd_dat.drop(columns=pd_dat.columns[temp_cols], inplace=True)
    except:
        print('del_col_names must be a list')
    return pd_dat


def non_blank_value(x):
    """x is pandas series, int, not-empty"""
    return x[x.notnull()]


def non_null_mrn(col_search="mrn"):
    """Specific function to obtain non-null values from a columns of mrn
    (medical record number). Applicable to a set of columns with string
    and integer values, etc

    Returns a pandas Series
    """
    col_mrn = {}
    # columns with mrn in names
    mrn_cols = datafile.columns.str.contains(col_search)
    # subset the datafile
    mrn = datafile.iloc[:, mrn_cols]
    for index in mrn.index:
        # Slice (series) with values (True/False)
        not_na_val = pd.notna(mrn.iloc[index, :])
        # obtain the values - so far the best way to deal with NaN
        val = mrn.loc[index, not_na_val].to_list()
        # val is a list (with a non-blank, if available)
        if len(val) > 0:
            col_mrn[index] = next(s for s in val if s)
        else:
            col_mrn[index] = None
    return pd.Series(col_mrn)


def subset_select_cols(pd_dat, search_text):
    """Utility function to print select columns based on search text"""
    cols_select = pd_dat.columns.str.contains(search_text)
    temp_dat = pd_dat.iloc[:, cols_select]
    return temp_dat


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
    all_columns = pd.read_csv('Rename_columns_file.csv')
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

    # Convert all date variable into Datetime objects
    date_columns = datafile.columns[datafile.columns.str.contains('dt')]
    non_date_cols = datafile.columns[~datafile.columns.str.contains('dt')]
    for cols in date_columns:
        datafile[cols] = datafile[cols].apply(pd.to_datetime, errors='coerce')

    # drop columns with no values
    datafile.dropna(how="all", axis=1, inplace=True)

    # combine similar columns- admit, surgery, discharge
    datafile = combine_cols(datafile, 'admission_dt', 'admit_dt', func=max)
    datafile = combine_cols(datafile, 'surgery_dt', 'surg_dt', func=max)
    datafile = combine_cols(datafile, 'discharge_dt', 'disch_dt', func=max)
    # delete date columns after combining
    datafile = drop_cols(pd_dat=datafile,
                         del_col_names=['admit_dt', 'surg_dt', 'disch_dt'])

    # combine columns with procedure description
    datafile = combine_cols(datafile,
                            'prcdr_des',
                            'procedure',
                            func=non_blank_value)
    # drop columns with procedure
    datafile = drop_cols(pd_dat=datafile, del_col_names=['procedure'])
    # combine gender variables
    datafile = combine_cols(datafile,
                            'patient_sex',
                            'gender',
                            func=non_blank_value)
    # drop columns with gender
    datafile = drop_cols(pd_dat=datafile, del_col_names=['gender'])


    # combining columns 'mrn' using non_null_mrn() defined above
    datafile['medical_id'] = non_null_mrn()
    # drop mrn variables
    datafile = drop_cols(pd_dat=datafile,
                         del_col_names=['mrn'])

    print(datafile.head())
    print(datafile[[
        'admission_dt', 'surgery_dt', 'discharge_dt', 'patient_sex',
        'prcdr_des']])

    # saving data
    datafile.to_csv(os.path.join(OUT_PTH, 'mrn_maa2.csv'))
