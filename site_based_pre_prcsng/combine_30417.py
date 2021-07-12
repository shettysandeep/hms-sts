"""

Code to extract metadata on file submission under ACSD
@author: Sandeep Shetty
@data: May 18, 2021

"""
import os
import re
from os.path import isfile, isdir, join
import shutil
import pandas as pd
from datetime import datetime
import fitz

"""
Things to do:
- create folders with site name & collect all relevant files
- unzip and collect all files
- consider the following metadata report
  - pdf scanned or notes
  - pages
  - id names

- Unzip files
- Collect site id from filename
- check if .csv, .xls or .pdf
- if .pdf check if OCR is needed

"""

class ParseEhr:

    def __init__(self, pth):
        self.pth = pth


    def unzip_file(self, new_folder):
        """
        Uncompress files within a given directory (pth).
        Move the zip files to a user defined folder in the same directory (new_folder)

        """
        self.new_folder=new_folder

        if not os.path.exists(join(self.pth,self.new_folder)):
            os.makedirs(join(self.pth,self.new_folder))

        file_path = [join(self.pth,items) for items in os.listdir(self.pth)]
        for fp in file_path:
            base_name=os.path.basename(fp)
            if isfile(fp):
                fname, file_ext = os.path.splitext(base_name)
                if re.search('.zip',file_ext):
                    shutil.unpack_archive(fp,self.pth)
                    shutil.move(fp,
                                join(self.pth,self.new_folder))
                    print('{} completed'.format(fp))


    def read_files(self, file_name):
        filepath = os.path.join(mypth,file_name)
        dat=pd.read_excel(filepath, sheet_name=None)
        return dat


    def gather_files(self):
        # collect all files with proper path from the directory
        all_file = [os.path.join(self.pth, f)
                    for f in os.listdir(self.pth)
                    if '.DS' not in f]

        # keep only xls(x) or csv
        fil_typ = '(xls|csv)'
        keep_excel = [f for f in all_file
                      if re.search(fil_typ, os.path.splitext(f)[1])]
        return keep_excel


    def parse_excel(self, file_name, search_term):
        '''
        # Code meant to loop through sheets in an Excel file.
        # Append each sheet with an identifier into a DataFrame
        '''
        dat = self.read_files(file_name)
        newdat=pd.DataFrame()
        datkeys = [keys for keys in dat.keys() if "Sheet" not in keys]
        for keys in datkeys:
            # ''' Excel with multiple spreadsheets '''
            dat2=dat[keys]
            # Check default columns by Pandas are not Unnamed
            cond1 = dat2.columns.str.contains('Unnamed:').any()
            print(cond1)
            if cond1:
                # If Unnamed then find the real columns
                for ind in dat2.index:
                    cond = dat2.loc[ind].str.contains(search_term, case=False)
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

    @staticmethod
    def clean_data(dataset, col_replace, search_term):
        """Clean data: replace columns names of one DataFrame per sit"""
        dat_new=dataset
        dat_new.columns=dat_new.columns.str.lower()
        all_columns = dat_new.columns.tolist()
        for col in all_columns:
            for item, val in col_replace.items():
                if item in col:
                    dat_new.rename(columns={col:val},
                                   inplace = True)
        return dat_new


    def data_save(self, pd_dat: 'Pandas DataFrame',
                  name_file, ifcsv=True):
        '''File save'''
        if ifcsv:
            date = datetime.now().strftime("%Y_%m_%d-%I%M%p")
            fname=f"{name_file}_{date}"
            otpth = os.path.join(self.pth,fname)
            pd_dat.to_excel("{}.xlsx".format(otpth))


if __name__ == '__main__':
    mypth = '/Users/sandeep/Documents/1-PROJECTS/sts/hms_data/acsd/or_log_data/30417'
    parseehr=ParseEhr(pth=mypth)
    # parseehr.unzip_file(new_folder='zipped')
    columns_term = "Age|Date|DOB|DT|DOS"
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

    filelist=parseehr.gather_files()
    pd_Data = pd.DataFrame()
    for f in filelist:
        newdat=parseehr.parse_excel(f, search_term=columns_term)
        data_clean = parseehr.clean_data(newdat,
                                         col_replace=list_cols,
                                         search_term=columns_term)
        pd_Data = pd_Data.append(data_clean)
    print(pd_Data.head())
    parseehr.data_save(pd_Data,name_file='30417_OR')

