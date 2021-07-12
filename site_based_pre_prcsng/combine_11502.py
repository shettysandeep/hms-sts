"""
11502 submitted .xlsx for each case id separately.
Below code is  as short code to combine the files into one.
The main purpose is to document the activities.

The zipped file unzipped into folder named "OR LOGS".
Each .xlsx file was named "11502_VXXXX.xlsx"




"""

import pandas as pd
import os

pth = '/Users/sandeep/Documents/1-PROJECTS/sts/hms_data/acsd/ehr_data/UploadedFiles/11502_ACSD_ORlog_6_3_2021'

data_comb = pd.DataFrame()
for items in os.listdir(pth):
    fname = os.path.join(pth,items)
    fname2, filext = os.path.splitext(items)
    if filext == '.xlsx':
        dat=pd.read_excel(fname, index_col=0)
        dat['id'] = fname2.split('_')[1]
        data_comb=data_comb.append(dat)
        print(fname2)
        #print(data_comb.head())
print(data_comb.shape)
print(data_comb.head())

data_comb.to_excel(os.path.join(pth,'OR_11502.xlsx'))




