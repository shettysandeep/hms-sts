#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Sandeep Shetty
@date: June 06, 2021

Code to parse HMS ACSD Data Submissions. Files submitted in Excel format with a
variety of format. After parsing, format the data into a table for comparing
(or automating audit) of ACSD master file.

TODO
1. import the files
2. check the number of sheets with data
3. collect the name of sheets
4. get to the point where the data is
5. collect the data

"""
from datetime import datetime
import pandas as pd
import os
import re


def read_files(filepath):
    dat=pd.read_excel(filepath, sheet_name=None)
    return dat


def gather_files(filedir):
    # collect all files with proper path from the directory
    all_file = [os.path.join(filedir, f)
                for f in os.listdir(filedir)
                if '.DS' not in f]

    # keep only xls(x) or csv
    fil_typ = '(xls|csv)'
    keep_excel = [f for f in all_file
                  if re.search(fil_typ, os.path.splitext(f)[1])]
    return keep_excel

def parse_excel(filepath, search_term):
    '''
    Code meant to loop through sheets in an Excel file.
    Append each sheet with an identifier into a DataFrame
    '''
    dat = read_files(filepath)
    newdat=pd.DataFrame()
    for keys in dat.keys():
        ''' Excel with multiple spreadsheets '''
        dat2=dat[keys]
        # Check default columns by Pandas are not Unnamed
        #print(dat2.head())
        cond1 = dat2.columns.str.contains('Unnamed:').any()
        print(cond1)
        if cond1:
            # If Unnamed then find the real columns
            for ind in dat2.index:
                cond = dat2.loc[ind].str.contains("Age|Date|DOB|DT", case=False)
                if cond.sum() > 0:
                    # collect the index where the actual columns are
                    dat2_start=ind
                    break
            # Assign columns to the spreadsheet frame
            dat2.columns=dat2.loc[dat2_start].to_list()
            dat2.drop(index=dat2_start, inplace=True)
        dat2.dropna(inplace=True)
        # Add a spreadsheet key before appending each sheet
        dat2['newkey']= str(keys)
        newdat = newdat.append(dat2)
        #print(newdat)
    return newdat


def clean_data(dataset, col_replace, search_term):
    """Clean data: replace columns names of one DataFrame per sit"""
    dat_new=parse_excel(dataset, search_term)
    #print(dat_new.head())
    dat_new.columns=dat_new.columns.str.lower()
    all_columns = dat_new.columns.tolist()
    #print(all_columns)
    for col in all_columns:
        for item, val in col_replace.items():
            if item in col:
                dat_new.rename(columns={col:val},
                               inplace = True)
    return dat_new


def data_save(pd_dat: 'Pandas DataFrame',
              opth,name_path, ifcsv=True):
    '''File save'''
    if ifcsv:
        date = datetime.now().strftime("%Y_%m_%d-%I%M%p")
        fname=f"{name_path}_{date}"
        otpth = os.path.join(opth,fname)
        pd_dat.to_csv("{}.csv".format(otpth))


if __name__ == '__main__':

    # File path
    filedir = r'/Users/sandeep/Documents/1-PROJECTS/sts/hms_data/acsd/or_log_data/'
    opth = r'/Users/sandeep/Documents/1-PROJECTS/sts/reports'

    # Collecting the list of files
    f = gather_files(filedir)

    # Search terms for identifying potential columns
    columns_term = "Age|Date|DOB|DT"

    # Columns to replace to harmonize the different submissions from Sites
    list_cols={"record id":"record id",
               "age": "age",
               "birth": "birth dt",
               "discharge": "disch dt",
               "procedure": "procedure",
               "admission":"admit dt",
               "admit": "admit dt",
               "surgery": "surgery dt",
               "surgeon": "surgeon",
               "dosurg": "surgery dt",
               "doadm": "admit dt",
               "dodisch": "disch dt",
               "patient name": 'patient',
               "patient's name": 'patient',
               "patient id": 'patient id',
               "case": "procedure",
               "dob": "birth dt",
               "record_id": "record id",
               "sex": "gender"
               }

    datnew2 = pd.DataFrame()
    for key, fil in enumerate(f):
        print(fil)
        clean_dataset = clean_data(dataset=fil,
                                   col_replace=list_cols,
                                   search_term=columns_term)

        # column duplicates condition
        col_dupe_cnd = clean_dataset.columns.duplicated().any()
        if col_dupe_cnd:
            cols_to_list =  clean_dataset.columns
            print(len(cols_to_list))
            col_dupes =  clean_dataset.columns.duplicated()
            test_zip=zip(cols_to_list, col_dupes)
            new_col_list=[]
            for key,items in enumerate(test_zip):
                if items[1]==True:
                    print(items[0])
                    new_name = items[0] + '_v1' + str(key)
                    print(new_name)
                    new_col_list.append(new_name)
                else:
                    new_col_list.append(items[0])
            print(new_col_list)
            print(len(new_col_list))
            clean_dataset.columns = new_col_list

        #print(clean_dataset.columns.tolist())
        datnew2 = datnew2.append(clean_dataset)

    # saving data for analysis
    data_save(datnew2,opth,'OR_combined')


