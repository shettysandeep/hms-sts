"""
10803 and 30111 submitted .xlsx for each case id separately.
Below code is  as short code to combine the files into one.
The main purpose is to document the activities.

The zipped file unzipped into folder named "OR LOGS".
Each .xlsx file was named "11502_VXXXX.xlsx"

"""

import pandas as pd
import numpy as np
import os

pth = '/Users/sandeep/Documents/1-PROJECTS/sts/hms_data/acsd/or_log_data/zip_archive'


def combine_xlwb(site_id):
    files_int = [f for f in os.listdir(pth) if site_id in f]
    print(files_int)
    data_comb = pd.DataFrame()
    for items in files_int:
        fname = os.path.join(pth,items)
        fname2, filext = os.path.splitext(items)
        if filext == '.xls':
            dat=pd.read_excel(fname, index_col=0, sheet_name='Dec 19')
            dat['id'] = fname2.split('-')[1]
            dat.reset_index(inplace=True)
            
            # dat = dat[dat['Surgery Date'] != ""]
            data_comb=data_comb.append(dat)
            print(fname2)

    # print(drop_rows)
    # data_comb = data_comb[dropidx]
    data_comb.replace('', np.nan, inplace = True)
    data_comb.dropna(subset=['STS Record ID'], inplace=True)
    print(data_comb.shape)
    print(data_comb.head())
    filesav = 'OR %s.xlsx' %site_id
    return data_comb.to_excel(os.path.join(pth,filesav))


# combine_xlwb('1080')
# combine_xlwb('30111')
combine_xlwb('14819')
