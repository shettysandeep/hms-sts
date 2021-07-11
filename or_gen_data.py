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

This takes two input datasets:
1. (OR_combined..xlsx)Roughly appended data from all sites (with loosely selected key variables)
2. (Record_Cols...xlsx) This data has a list of selected variables above  and only relevant
   variables have a new name. Variables (old) without a new name are dropped from the final dataset.
 
"""
import os, re
import pandas as pd
from datetime import datetime


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


def non_null_mrn(col_search="mrn"):
    """Function to obtain non-null values from a columns of mrn
    (medical record number). Applicable to a set of columns with string
    and integer values, etc. Searches for a non-null value along the
    selected rows.

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
        # val is a list (non-blank, if available)
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


def find_site_id(file_name):
    num_id = re.findall('(\d{5})', file_name)
    if len(num_id) > 0:
        return num_id[0]
    else:
        return ""


def data_save(pd_dat: 'Pandas DataFrame', opth, name_path, ifcsv=True):
    '''File save'''
    if ifcsv:
        date = datetime.now().strftime("%Y_%m_%d-%I%M%p")
        fname = f"{name_path}_{date}"
        otpth = os.path.join(opth, fname)
        pd_dat.to_csv("{}.csv".format(otpth))


if __name__ == '__main__':

    # File path
    FLDR_PTH = '/Users/sandeep/Documents/1-PROJECTS/sts/reports'
    # FILE_NAME = 'OR_combined_data_2021_07_06-0403PM.csv' OLD ONE
    FILE_NAME = 'OR_combined_data_2021_07_11-0502PM.csv' # Updated with new sites
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
    # Dictionary of columns to be renamed
    old_new_cols = dict(
        zip(cols_to_rename.Old_names.tolist(),
            cols_to_rename.New_names.tolist()))

    # ~~~~ Step 2
    # Import the main dataset (roughly combined)
    # Remove unnecessary columns (cols_to_drop)
    # Rename columns name (cols_to_rename) using the dictionary
    # created in (old_new_cols)

    datafile = pd.read_csv(CSV_FILE, low_memory=False)
    datafile.drop(columns=cols_to_drop, inplace=True)
    datafile.rename(columns=old_new_cols, inplace=True)
    datafile.drop(columns="Unnamed: 0", inplace=True)

    # Convert all date variable into Datetime objects
    date_columns = datafile.columns[datafile.columns.str.contains('dt')]
    for cols in date_columns:
        datafile[cols] = datafile[cols].apply(pd.to_datetime, errors='coerce')

    # drop columns with no values
    datafile.dropna(how="all", axis=1, inplace=True)

    # ~~~ COMBINE COLUMNS
    # KEY - Columns to search and combine
    # VALUE - Name for the combined variable
    COLS_DT = {
        'admit_dt': 'ADMISSION_DT',
        'surg_dt': 'SURGERY_DT',
        'disch_dt': 'DISCHARGE_DT',
        'proc_des': 'PRCDR_DES',
        'mrn': 'MEDICAL_ID',
        'rec': 'RCD_ID',
        'patient_id': 'PAT_ID',
        'procedure': 'PRCDR',
        'gender': 'PATIENT_SEX'
    }

    for key, val in COLS_DT.items():
        datafile[val] = non_null_mrn(key)

    datafile = drop_cols(pd_dat=datafile, del_col_names=list(COLS_DT.keys()))

    # Add SITE ID
    datafile['SITE_ID'] = datafile['filename'].apply(find_site_id)

    # Organize cols
    cols_order = [
        "SITE_ID", "RCD_ID", "PAT_ID", "MEDICAL_ID", "PATIENT_SEX",
        "ADMISSION_DT", "SURGERY_DT", "DISCHARGE_DT", "PRCDR", "PRCDR_DES",
        "filename"
    ]

    datafile = datafile[cols_order]

    print(datafile.head())
    print(datafile.columns.to_list())
    # Save Dataset
    data_save(pd_dat=datafile, opth=OUT_PTH, name_path='Clean_Comb_OR')
