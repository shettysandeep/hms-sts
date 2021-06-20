#!/usr/bin/env python3

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

def unzip_file(filepth, new_folder='zip_archives'):
    '''Unzip zip files and move the zip to a new folder in the same directory'''
    if not os.path.exists(join(filepth,new_folder)):
        os.makedirs(join(filepth,new_folder))

    for items in os.listdir(filepth):
        file_path = join(pth,items)
        if isfile(file_path):
            fname, file_ext = os.path.splitext(items)
            print(file_ext)
            print(fname)
            if re.search('.zip|.7z',file_ext):
            #if items.split('.')[-1] == '.zip':
                shutil.unpack_archive(file_path,pth)
                shutil.move(file_path,
                            join(filepth,new_folder))
                print('{} completed'.format(file_path))


def move_file(filepth):
    '''Move files out of subfolders to the root of input path'''
    for item2 in os.listdir(filepth):
        if not item2.startswith('.DS'):
            file_path = join(filepth,item2)
            if isdir(file_path):
                for rt, dnames, fnames in os.walk(file_path):
                    for fn in fnames:
                        shutil.move((join(file_path,fn)),
                                    join(filepth,fn))


def report_files(filepth):
    '''
    Read files in the filepth; extract names and
    return Pandas DataFrame
    '''
    site_name=[]
    file_name=[]
    type_file=[]
    search_pdf=[]
    pages_pdf=[]
    fillist = [f for f in os.listdir(filepth)
               if not re.search("^(zip|\.DS)", f)]
    print(fillist)
    for items in fillist:
        site_name.append(re.split(r'(_|-)', items)[0])
        file_name.append(re.split(r'(_|-)', items)[2])
        type_file.append(os.path.splitext(items)[1])
        #print(os.path.splitext(items)[1])
        if os.path.splitext(items)[1]=='.pdf':
            print(os.path.join(filepth,items))
            search_pdf_v, page_pdf_v = get_text_percentage(os.path.join(filepth,items))
            print(search_pdf_v)
            search_pdf.append(search_pdf_v)
            pages_pdf.append(page_pdf_v)
    daton = pd.DataFrame(list(zip(site_name, file_name, type_file, search_pdf, pages_pdf)),
                         columns =['site','filename','file_type', 'search_able', 'pages'])

    return daton

def data_clean(dataset):
    daton=dataset.copy()
    daton=daton.drop_duplicates()
    daton['case_id']=daton.filename.str.split('.',expand=True)[0]
    daton.sort_values(by='site',inplace=True)
    datong=daton.groupby('site').count()
    datong.rename(columns={'filename':'count_filename'})
    datong.reset_index(inplace=True)
    daton.merge(datong, left_on='site', right_on='site', how='left')
    return daton

def data_save(pd_dat,pth,name_path, ifcsv=True):
    if ifcsv:
        date = datetime.now().strftime("%Y_%m_%d-%I%M%p")
        filname=f"{name_path}_{date}"
        outpath = os.path.join(pth,filname)
        pd_dat.to_csv("{}.csv".format(outpath))

def create_folder(filpth):
    #os.listdir(filpth)
    for items in os.listdir(filpth):
        if isfile(join(filpth,items)) and not ".zip" in items :
            filename=re.split(r'(_|-)', items)[0]
            if not os.path.exists(join(filpth,filename)):
                os.makedirs(join(filpth,filename))
            shutil.move((join(filpth,items)),
                        join(filpth,filename,items))
def clean_master(dat):
    '''Clean the grand file'''
    dat['type']=dat.case_id.str.extract(r'\d([a-zA-Z]*)$', expand=False)
    dat['case_id']=dat.case_id.str.replace(r'[a-zA-Z]*\d?$','', regex=True)
    return dat


#def pdf_searchable(fileway: str) -> float:
def get_text_percentage(file_name):
    """
    Calculate the percentage of document that is covered by (searchable) text.

    If the returned percentage of text is very low, the document is
    most likely a scanned PDF
    source: https://stackoverflow.com/questions/55704218/how-to-check-if-pdf-is-scanned-image-or-contains-text
    """
    total_page_area = 0.0
    total_text_area = 0.0
    doc = fitz.Document(file_name)
    if doc.needsPass:
        try:
            doc.authenticate('Tenet123')
        except ExplicitException:
            print("Next password")
        else:
            doc.authenticate('Sanroi2021')
    page_pdf = doc.pageCount
    for page_num, page in enumerate(doc):
        total_page_area = total_page_area + abs(page.rect)
        text_area = 0.0
        for b in page.getTextBlocks():
            r = fitz.Rect(b[:4])  # rectangle where block text appears
            text_area = text_area + abs(r)
        total_text_area = total_text_area + text_area
    doc.close()
    return (total_text_area / max(total_page_area,1), page_pdf)



if __name__ == '__main__':
    pth = '/Users/sandeep/Documents/1-PROJECTS/sts/hms_data/acsd/or_log_data/zipped_files'
    opth = '/Users/sandeep/Documents/1-PROJECTS/sts/reports/'
    print(unzip_file(pth))
    #move_file(pth)
    #daton = report_files(pth)
    #newdat = data_clean(daton)
    #data_save(newdat,'acsd_submission')
    #create_folder(pth)
    '''
    fillist = [f for f in os.listdir(pth)
               if not re.search("^(zip|\.DS)", f)]
    print(fillist)

    dat=pd.DataFrame()

    #Move files out of subfolders to the root of input path
    for item2 in os.listdir(pth):
        #print(item2)
        if not re.search('(^.DS|^UNK)',item2):
            file_path = join(pth,item2)
            if isdir(file_path):
                #print(file_path)
                dattest=report_files(file_path)
                #print(dattest.head(2))
                dat=dat.append(dattest, ignore_index=True)
    data_save(dat, pth=opth,name_path='pdf_search')
    #print(dat.head())
    dat2=data_clean(dat)
    dat3=clean_master(dat2)
    data_save(dat3,pth=opth,name_path='acsd_uploads')
    '''
