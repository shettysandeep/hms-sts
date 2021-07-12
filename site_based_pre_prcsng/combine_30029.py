#-*-coding: utf-8-*-

"""
__author__: Sandeep Shetty
__date__: date

Code to merge multiple excel spreadsheets from site 30029

"""

import pandas as pd
import os

pth = '/Users/sandeep/Documents/1-PROJECTS/sts/hms_data/acsd/or_log_data/UploadedFiles_08Jun2021/30029_ACSD_ORLOG'

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

data_comb.to_excel(os.path.join(pth,'OR_30029.xlsx'))
