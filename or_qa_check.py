#-*-coding: utf-8-*-
"""
__author__: Sandeep Shetty
__date__: July 12, 2021

"""

import os, re
import pandas as pd
import numpy as np
import argparse
# from or_parsing_data import clean_data_app2, dupe_columns_clean, parse_excel
from HelperFileManage import HelperFileManage

def missing_files(DATA_PTH, RAW_PTH):
    # Read the final dataset
    comb_dat = pd.read_csv (DATA_PTH)
    # Check the filenames against the raw files in directory
    # Checking if we missed any files
    # 1. Filenames included in Final data
    in_data_files = comb_dat.filename.unique().tolist()

    # 2. Pulling filenames in the directory
    dir_files = os.listdir(RAW_PTH)
    in_dir_files = [f for f in dir_files if
                    os.path.splitext(f)[1] in ['.xlsx', '.xls', '.csv']]
    miss_files1 = list(set(in_dir_files) - set(in_data_files))
    miss_files2 = list(set(in_data_files) - set(in_dir_files))
    print(f"missing files A-B: {miss_files1}")
    print(f"missing files B-A: {miss_files2}")


def missing_report(datafile):
    dat = pd.read_csv(datafile)
    newdat = pd.DataFrame()
    for nm in set(dat.SITE_ID):
        temp_dat = dat.loc[dat['SITE_ID']==nm]
        siteid = temp_dat.SITE_ID.tolist()[0]
        lenth = temp_dat.shape[0]
        temp_dat=temp_dat.isnull().sum()/lenth*100
        temp_dat['Site_ID']=str(siteid)
        temp_dat['OBS_COUNT'] = lenth
        newdat = newdat.append(temp_dat, ignore_index=True)
    # reorder Cols
    newdat_Cols = ['Site_ID', 'RCD_ID','MEDICAL_ID', 'PAT_ID',
                   'ADMISSION_DT', 'SURGERY_DT', 'DISCHARGE_DT', 'PRCDR',
                   'PRCDR_DES', 'PATIENT_SEX','OBS_COUNT']
    newdat=newdat[newdat_Cols]
    return newdat


if __name__ == '__main__':
    #~~~ Import Dataset
    # Path to Final Combined dataset
    PRJT_FLDR = '/Users/sandeep/Documents/1-PROJECTS/sts'
    FILE_NAME = 'Clean_Comb_OR_2021_08_18-0450PM.csv'
    DATA_PTH = os.path.join(PRJT_FLDR, 'reports', FILE_NAME)
    # Directory where the raw data are saved
    RAW_PTH = os.path.join(PRJT_FLDR, 'hms_data/acsd/or_log_data')

    hfm=HelperFileManage()
    # Check which files are not read into the Combined Dataset
    missing_files(DATA_PTH=DATA_PTH, RAW_PTH=RAW_PTH)
    newdat = missing_report(DATA_PTH)
    hfm.data_save(newdat,outpth=os.path.join(PRJT_FLDR,'reports'), name_path='Missing_Report')
"""
# Testing some dataset

# files_list = ['30376_ACSD_ORlog.xlsx',
# 'OR_12104.xlsx', '10705_ACSD_ORlog.xlsx','ORLog_30466.xlsx', '11719_ACSD_Audit_SS.xlsx',
            # 'ORLog_14301.xlsx', 'OR_30111.xlsx', 'OR_30029.xlsx', 'ORLog_31076.xlsx', 'ORLog_30424.xlsx']

files_list=['ORLog_14301.xlsx']
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
                 "sts": "sts id"
                 }

datnew2 = pd.DataFrame()
for key, fil1 in enumerate(files_list):
    fil = os.path.join(RAW_PTH, fil1)
    print(fil)
    clean_dataset = clean_data_app2(dataset=fil,
                                col_replace=list_cols,
                                search_term=COLUMN_TERMS)
    print(clean_dataset.head())
    excel_name = os.path.basename(fil)
    clean_dataset['filename'] = excel_name
    col_dupe_cnd = clean_dataset.columns.duplicated().any()
    print(col_dupe_cnd)
    if col_dupe_cnd:
        clean_dataset = dupe_columns_clean(dataset=clean_dataset)
    datnew2 = pd.concat([datnew2, clean_dataset],
                    axis=0).reset_index(drop=True)

print(datnew2.head())
"""

