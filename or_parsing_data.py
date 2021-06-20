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
import numpy as np
import os
import re


def read_files(filepath):
    dat=pd.read_excel(filepath, sheet_name=None, index_col=0)
    return dat


def gather_files(filedir):
    # collect all files with proper path from the directory
    all_file = [os.path.join(filedir, f)
                for f in os.listdir(filedir)
                if '.DS' not in f]
    fil_typ = '(xls|csv)'
    keep_excel = [f for f in all_file
                  if re.search(fil_typ, os.path.splitext(f)[1])]
    return keep_excel


def parse_excel(filepath, search_term):
    '''
    Loop through sheets in an Excel file.
    Append each sheet with an identifier into a DataFrame
    '''
    dat = read_files(filepath)
    newdat=pd.DataFrame()
    for keys in dat.keys():
        ''' Excel with multiple spreadsheets '''
        dat2=dat[keys]
        # Check default columns by Pandas are not Unnamed
        #print(dat2.head())
        dat2.reset_index(inplace=True)
        cond1 = dat2.columns.str.contains('Unnamed:').any()
        print(dat2.columns)
        print("First {}".format(cond1))
        if cond1:
            # If Unnamed then find the real columns
            for ind in dat2.index:
                cond = dat2.loc[ind].str.contains(search_term, case=False)
                print("Dat2 loc")
                print(dat2.loc[ind])
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
        newdat=pd.concat([newdat,dat2],axis=0).reset_index(drop=True)
        # newdat = newdat.append(dat2)
        #print(newdat)
    return newdat


def clean_data(dataset, col_replace, search_term):
    """Clean data: replace columns names of one DataFrame per sit"""
    dat_new=parse_excel(dataset, search_term)
    print("Parsed well~~~~~\n")
    print(dat_new.head(2))
    dat_new.columns=dat_new.columns.str.lower()
    all_columns = dat_new.columns.tolist()
    print(all_columns)
    for col in all_columns:
        for item, val in col_replace.items():
            if re.search(item, col):
            #if item in col:
                dat_new.rename(columns={col:val},
                               inplace = True)
    return dat_new


def clean_data_app2(dataset, col_replace, search_term):
    """Clean data: replace columns names of one DataFrame per sit"""
    dat_new=parse_excel(dataset, search_term)
    print("Parsed well~~~~~\n")
    # print(dat_new.head(2))
    dat_new.columns=dat_new.columns.str.lower()
    all_columns = dat_new.columns.tolist()
    cleanedList = [x for x in all_columns if x == x]
    print(cleanedList)
    filter_col = []
    for col in cleanedList:
        # filter_col = [col for item in col_replace.keys() if re.search(item,col,re.IGNORECASE)]

        # print('FILTER ~~~\n')
        # print(filter_col)
        for item, val in col_replace.items():
            if item in col:
                filter_col.append(col)
    print('FILTER ~~~\n')
    set_filter_col = list(set(filter_col))
    dat_new = dat_new[set_filter_col]
    print(dat_new.shape)
    return dat_new


def dupe_columns_clean(dataset):
    """Handles duplicate columns in dataset.
    Adds _v# to each duplicated column"""

    clean_dataset = dataset
    cols_to_list =  clean_dataset.columns
    col_dupes =  clean_dataset.columns.duplicated()
    test_zip = zip(cols_to_list, col_dupes)
    new_col_list=[]
    for key,items in enumerate(test_zip):
        if items[1]==True:
            print(items[0])
            new_name = items[0] + '_v1' + str(key)
            print(new_name)
            new_col_list.append(new_name)
        else:
            new_col_list.append(items[0])
    clean_dataset.columns = new_col_list
    return clean_dataset


def find_site_id(file_name):
    """ Extract 5-digit number from string"""
    num_id = re.findall('(\d{5})', file_name)
    return num_id


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
    columns_term = "Age|Date|DOB|DT|Birth"

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
               "sex": "gender",
               "dt": "dt",
               "date":"date",
               "adm" : "admission",
               "mrn" : "medical id",
               "id" : "medical id"
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
    # datnew2 = pd.DataFrame()
    dict_columns = {}
    for key, fil in enumerate(f):
        print(fil)
        clean_dataset = clean_data_app2(dataset=fil,
                                   col_replace=list_cols,
                                   search_term=columns_term)
        excel_name = os.path.basename(fil)
        clean_dataset['filename'] = excel_name
        col_dupe_cnd = clean_dataset.columns.duplicated().any()
        if col_dupe_cnd:
            """put dataset through column clean-up"""
            clean_dataset=dupe_columns_clean(dataset=clean_dataset)
        dict_columns[excel_name]=clean_dataset.columns.tolist()

        # datnew2 = pd.concat([datnew2,clean_dataset],axis=0).reset_index(drop=True)
    col_dat = pd.DataFrame.from_dict(dict_columns, orient='index')
    data_save(col_dat,opth,'OR_combined_cols')

    # saving data for analysis
    # data_save(datnew2,opth,'OR_combined')


