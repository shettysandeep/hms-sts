'''
Code for OR Data Analysis
@author: Sandeep Shetty
@date: May 25, 2021

'''
from datetime import datetime
import os
import re
import pandas as pd


def gen_report(filpath):
    fname_list = [f for f in os.listdir(filpath) if not f.startswith('.DS')]
    num_lngth = [find_site_id(fil) for fil in fname_list]
    file_type = [filetype_extraction(fil) for fil in fname_list]

    dat_cols = zip(num_lngth,fname_list,file_type)
    col_names = ['ID','Filename','File_type']

    dataset = pd.DataFrame(dat_cols, columns=col_names)
    return dataset


def filetype_extraction(file_name):
    a, b = os.path.splitext(file_name)
    return b


def find_site_id(file_name):
    num_id = re.findall('(\d{5})', file_name)
    return num_id


def data_save(pd_dat: 'Pandas DataFrame',opth,name_path, ifcsv=True):
    '''File save'''
    if ifcsv:
        date = datetime.now().strftime("%Y_%m_%d-%I%M%p")
        fname=f"{name_path}_{date}"
        otpth = os.path.join(opth,fname)
        pd_dat.to_csv("{}.csv".format(otpth))


if __name__ == '__main__':
    #input path
    filpath = '/Users/sandeep/Documents/1-PROJECTS/sts/hms_data/acsd/or_log_data'

    #report path
    opth = '/Users/sandeep/Documents/1-PROJECTS/sts/reports/or_report'

    dataset = gen_report(filpath)
    dataset['ID'] = dataset['ID'].str.get(0)
    data_save(dataset,opth,'OR_log_submitted')

