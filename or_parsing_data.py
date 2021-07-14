# -*- coding: utf-8 -*-

"""
__author__: Sandeep Shetty
__date__: June 06, 2021

Code to parse OR Logs submitted as Excel workbooks. The files differ in the breadth of
information shared (variable names, etc.). The objective is to parse,
harmonize and combine data into one large table for comparing for auditing.

Input: Path to collection of files
Output: Combined Pandas DataFrame

"""
from datetime import datetime
import os
import re
import pandas as pd


def read_files(filepath):
    """Returns .xlsx workbook as Pandas DataFrame (dictionary)"""
    dat = pd.read_excel(filepath, sheet_name=None, index_col=0)
    return dat

def gather_files(file_dir, file_type='(xls|csv)'):
    """ Returns a list of .xls or .csv files at the given location

    Keyword arguments:
    file_dir -- Path to the folder
    file_type -- Type of file to select - xlsx or csv
    """
    all_file = [os.path.join(file_dir, f)
                for f in os.listdir(file_dir)
                if '.DS' not in f]
    # fil_typ = '(xls|csv)'
    keep_excel = [f for f in all_file
                  if re.search(file_type, os.path.splitext(f)[1])]
    return keep_excel

def parse_excel(filepath, search_term):
    '''
    Loop through sheets in an Excel file.
    Combine data from different sheets into one large dataset,
    Append each sheet with an identifier into a DataFrame.
    '''
    dat = read_files(filepath)
    print("First entry")
    
    newdat = pd.DataFrame()
    for keys in dat.keys():
        # Excel with multiple spreadsheets
        dat2 = dat[keys]
        print(dat2.head())
        dat2.reset_index(inplace=True)
        # Check default columns by Pandas are not Unnamed
        cond1 = dat2.columns.str.contains('Unnamed:').any()
        # print(dat2.columns)
        print("First {}".format(cond1))
        if cond1:
            # If Unnamed columns then find the real columns
            # Multi-index in excel files (with merged cols, etc.)
            # Look for the real columns (names) that matter
            # These are columns with text of interest such as age, birth, date of surgery, etc.
            for ind in dat2.index:
                cond = dat2.loc[ind].str.contains(search_term, case=False)
                print("Dat2 loc")
                print(dat2.loc[ind])
                if cond.sum() > 0:
                    # collect the index where the actual columns are
                    dat2_start = ind
                    break
            # Assign columns to the spreadsheet frame
            dat2.columns = dat2.loc[dat2_start].to_list()
            dat2.drop(index=dat2_start, inplace=True)
        # dat2.dropna(inplace=True)
        # Add a spreadsheet key before appending each sheet
        dat2['newkey'] = str(keys)
        newdat = pd.concat([newdat, dat2], axis=0).reset_index(drop=True)
        # newdat = newdat.append(dat2)
        print("Yeh hain ~~~~~\n")
        print(newdat.head())
    return newdat

# def clean_data(dataset, col_replace, search_term):
#     """Clean data: replace columns names of one DataFrame per sit"""
#     dat_new = parse_excel(dataset, search_term)
#     print("Parsed well~~~~~\n")
#     print(dat_new.head(2))
#     dat_new.columns = dat_new.columns.str.lower()
#     all_columns = dat_new.columns.tolist()
#     print(all_columns)
#     for col in all_columns:
#         for item, val in col_replace.items():
#             if re.search(item, col):
#                 dat_new.rename(columns={col: val}, inplace=True)
#     return dat_new

def clean_data_app2(dataset, col_replace, search_term):
    """Clean data: replace columns names of one DataFrame per sit"""
    dat_new = parse_excel(dataset, search_term)
    print("what is")
    print(dat_new.head())
    print("Parsed well~~~~~\n")
    # print(dat_new.head(2))
    dat_new.columns = dat_new.columns.str.lower()
    all_columns = dat_new.columns.tolist()
    cleaned_list = [x for x in all_columns if x == x]
    print("Clean list ~~~~")
    print(cleaned_list)
    filter_col = []
    for col in cleaned_list:
        for item, _ in col_replace.items():
            if item in col:
                filter_col.append(col)
    set_filter_col = list(set(filter_col))
    print("Set filter col ~~~~")
    print(set_filter_col)
    print(dat_new.head())
    dat_new = dat_new[set_filter_col]
    print(dat_new.shape)
    return dat_new

def dupe_columns_clean(dataset):
    """Handles duplicate columns in dataset.
    Adds _v# to each duplicated column"""
    cols_to_list = dataset.columns
    col_dupes = dataset.columns.duplicated()
    test_zip = zip(cols_to_list, col_dupes)
    new_col_list = []
    for indx, items in enumerate(test_zip):
        if items[1]:
            print(items[0])
            new_name = items[0] + '_v' + str(indx)
            print(new_name)
            new_col_list.append(new_name)
        else:
            new_col_list.append(items[0])
    dataset.columns = new_col_list
    return dataset

def find_site_id(file_name):
    """ Extract 5-digit number from string"""
    num_id = re.findall(r'(\d{5})', file_name)
    return num_id


def data_save(pd_dat, outpth, name_path, ifcsv=True):
    """Save file with time stamp"""
    if ifcsv:
        date = datetime.now().strftime("%Y_%m_%d-%I%M%p")
        fname = f"{name_path}_{date}"
        otpth = os.path.join(outpth, fname)
        pd_dat.to_csv("{}.csv".format(otpth))


if __name__ == '__main__':

    # File path
    PRJCT_PTH = r'/Users/sandeep/Documents/1-PROJECTS/sts'
    FLDR_PTH = r'hms_data/acsd/or_log_data/'
    FILEPTH = os.path.join(PRJCT_PTH, FLDR_PTH)

    OUT_PTH = r'/Users/sandeep/Documents/1-PROJECTS/sts/reports'

    # Collecting the list of files
    f = gather_files(FILEPTH)

    # Search terms for identifying potential columns
    COLUMN_TERMS = "Age|Date|DOB|DT|Birth"

    # Columns to replace to harmonize the different submissions from Sites
    list_cols = {"record id": "record id",
                 "age": "age",
                 "birth": "birth dt",
                 "discharge": "disch dt",
                 "procedure": "procedure",
                 "admission": "admit dt",
                 "admit": "admit dt",
                 "surgery": "surgery dt",
                 "surgeon": "surgeon",
                 "dosurg": "surgery dt",
                 "doadm": "admit dt",
                 "dodisch": "disch dt",
                 "patient name": 'patient',
                 "patient's name": 'patient',
                 "patient id": 'patient id',
                 "patient": "patient id",
                 "case": "procedure",
                 "dob": "birth dt",
                 "record_id": "record id",
                 "sex": "gender",
                 "dt": "dt",
                 "date": "date",
                 "adm": "admission",
                 "mrn": "medical id",
                 "id": "medical id",
                 "gender": "gender",
                 "record" : "record",
                 "sts": "sts id",
                 "dos": "surgery dt",
                 "cabg": "procedure",
                 'hosp_disch': "discharge",
                 "hosp_admsn_time": "admission date",
                 "hosp_disch_time":"discharge date"

                 }
    """
    for key, fil in enumerate(f):
        print(fil)
        clean_dataset = clean_data(dataset=fil,
                                   col_replace=list_cols,
                                   search_term=columns_term)

        # column duplicates condition
        col_dupe_cnd = clean_dataset.columns.duplicated().any()
        if col_dupe_cnd:
            clean_dataset = dupe_columns_clean(dataset=clean_dataset)

        #print(clean_dataset.columns.tolist())
        datnew2 = datnew2.append(clean_dataset)
    """

    datnew2 = pd.DataFrame()
    # dict_columns = {}
    for key, fil in enumerate(f):
        print(fil)
        clean_dataset = clean_data_app2(dataset=fil,
                                        col_replace=list_cols,
                                        search_term=COLUMN_TERMS)
        excel_name = os.path.basename(fil)
        clean_dataset['filename'] = excel_name
        col_dupe_cnd = clean_dataset.columns.duplicated().any()
        if col_dupe_cnd:
            clean_dataset = dupe_columns_clean(dataset=clean_dataset)
        # dict_columns[excel_name] = clean_dataset.columns.tolist()
        datnew2 = pd.concat([datnew2, clean_dataset],
                            axis=0).reset_index(drop=True)
    # col_dat = pd.DataFrame.from_dict(dict_columns, orient='index')
    # data_save(col_dat, OUT_PTH, 'OR_combined_cols')
    # saving data for analysis
    data_save(datnew2,OUT_PTH,'OR_combined_data')

    # ~~~~~~~~~~ Intermediate end ~~~~~~~~~~~

    # NOTES
    # We need to continue working with combined dataset (datanew2)
    # We need to filter the columns further.
    # The relevant columns by each site are in the below filename
    # Record_Cols_2021_07_06-1111AM_FINALLIST_COLS.csv
    # The rest of the analysis to clean up the above dataset is in
    # 'or_gen_data.py', which is available here
    # https://github.com/shettysandeep/hms-sts

