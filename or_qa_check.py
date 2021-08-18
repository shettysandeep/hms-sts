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
