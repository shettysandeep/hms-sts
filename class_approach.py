"""

Temp content: Class approach to parsing and combining excel files
__author__: Sandeep Shetty
__date__: June 20, 2021


"""
import os
import re
import shutil
from os.path import isfile, isdir, join
from datetime import datetime
import pandas as pd
import fitz


class ParseORLogs:
    """ Parse OR log Excel files."""

    def __init__(self):
        self._pth = ''
        self._fname = ''

    @property
    def pth(self):
        return self._pth

    @property
    def fname(self):
        return self._fname

    @pth.setter
    def pth(self, filepath):
        self._pth = filepath

    @fname.setter
    def fname(self, filename):
        self._fname=filename

    def read_files(self, visible_sheets_only=True):
        if visible_sheets_only:
            list_sheets = self.get_hidden_sheets(self._fname)
            dat=pd.read_excel(self._fname, sheet_name=None)
            return dat
        else:
            dat=pd.read_excel(self._fname, sheet_name=None)
            return dat

    @staticmethod
    def get_hidden_sheets(excel_file):
        """Return a list of un-hidden sheet names from an Excel workbook"""
        dat = pd.ExcelFile(excel_file)
        sheet_list = []
        for sheet in dat.book.sheets():
            if sheet.visibility==0:
                sheet_list.append(sheet.name)
        return sheet_list

    def gather_xl_files(self):
        """
        Collect all .xls(x) and .csv  files at the location
        Input : Directory
        Output : List of Excel file pathnames
        """
        try:
            if isdir(self._pth):
                all_file = [os.path.join(self._pth, f)
                            for f in os.listdir(self._pth) if '.DS' not in f]
                xl_files = [f for f in all_file if re.search('(xls|csv)', os.path.splitext(f)[1])]
        except ValueError:
            print("Not a Directory")

        return xl_files

    def parse_excel(self, file_name, search_term):
        """
        Parse an excel file with multiple sheets.
        Ignore hidden sheets, and drop blank columns.
        Combine data from different sheets within a workbook,
        and add the sheet name as a column in the  DataFrame
        """
        print(file_name)
        dat = self.read_files(file_name)
        newdat=pd.DataFrame()
        datkeys = [keys for keys in dat.keys() if "Sheet" not in keys]
        for keys in datkeys:
            # ''' Excel with multiple spreadsheets '''
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

if __name__ == '__main__':

    mypth = '/Users/sandeep/Documents/1-PROJECTS/sts/hms_data/acsd/or_log_data/'
    parseehr=ParseORLogs()
    parseehr.pth=mypth
    print(parseehr.xl_files)
    # parseehr.unzip_file(new_folder='zipped')
    # dat=parseehr.read_files('Audit List December 2019.xlsx')
    # columns_term = "Age|Date|DOB|DT|DOS"
    # newdat=parseehr.parse_excel('Audit List December 2019.xlsx', search_term=columns_term)
    # print(newdat)



