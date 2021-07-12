# -*- coding: utf-8 -*-

"""
@author: Sandeep Shetty
@date: June 16, 2021

Helper Functions for File Management under STS/HMS Submissions

"""
from datetime import datetime
from os.path import join, isfile, isdir
import pandas as pd
import numpy as np
import os
import time
import re
import shutil


class HelperFileManage:
    """
    Defining some helper functions for file management.
    Input: Folder path.
    Functions:
   """ 
    
    def __init__(self):
        self._pth = ''

    @property
    def pth(self):
        return self._pth

    @pth.setter
    def pth(self, filepath):
        self._pth = filepath

    @property
    def new_folder(self):
        return self._new_folder


    @new_folder.setter
    def new_folder(self, name):
        name2 = '{}_{}'.format(name,time.ctime())
        self._new_folder = name2

    def unzip_file(self):
        """
        Uncompress files within a given directory (pth).
        Move the zip files to a user defined folder in the same directory (new_folder)

        """
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
                                os.path.join(self.pth,self.new_folder))
                    print('{} completed'.format(fp))

    @staticmethod
    def data_save(pd_dat, outpth, name_path, ifcsv=True):
        """Save file with time stamp"""
        if ifcsv:
            date = datetime.now().strftime("%Y_%m_%d-%I%M%p")
            fname = f"{name_path}_{date}"
            otpth = os.path.join(outpth, fname)
            pd_dat.to_csv("{}.csv".format(otpth))


if __name__ == '__main__':

    FLDR_PTH = r'/Users/sandeep/Documents/1-PROJECTS/sts/hms_data/acsd/or_log_data/UploadedFiles'

    helpme = HelperFileManage()
    helpme.pth = FLDR_PTH
    helpme.new_folder = 'downloaded'
    helpme.unzip_file()
