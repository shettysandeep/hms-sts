import string
import pandas as pd
import re
import fitz
import os

printable = set(string.printable)


def doc_open(filepath):
    doc = fitz.open( filepath)
    return doc


def extract_2_frame(doc):
    codebook = {}
    for pages in doc.pages():
        pg_txt_blk = pages.getTextBlocks()
        for i in pg_txt_blk:
            txt= i[4].split(":")
            if len(txt) > 1 :
                codebook[txt[0]]=txt[1]
    codebook_data = pd.DataFrame(index=codebook.keys(),data = codebook.values())
    codebook_data.reset_index(inplace=True)
    return codebook_data



def rename_cols(pd_dat):
    cols = {'index': 'Description', 0: 'Keys'}
    pd_dat.rename(columns=cols, inplace=True)
    return pd_dat

# add some fucntions to be used in data cleanup below (6.7.2021)

def data_cleanup(pd_dat: 'Pandas DataFrame'):
    codebook_data['Description'] = codebook_data.Description.str.replace("\n*", "")
    codebook_data['Keys'] = codebook_data.Keys.str.replace("\n*", "")
    codebook_data['Description']=codebook_data['Description'].apply(lambda x: ''.join(filter(lambda x: x in printable,x)))
    codebook_data['Keys']=codebook_data['Keys'].apply(lambda x: ''.join(filter(lambda x: x in printable,x)))
    codebook_data['var_names']=codebook_data.Keys.str.extract('(?P<var_names>\w*\s?\([0-9]*\))',expand=True)
    codebook_data["Keys"]=codebook_data.Keys.str.replace(r"(\w*\s?\([0-9]*\))","")
    codebook_data['Description']=codebook_data['Description']+codebook_data['Keys']
    codebook_data.drop(columns=['Keys'], inplace=True)


def data_save(pd_dat,pth,name_path, ifcsv=True):
    if ifcsv:
        date = datetime.now().strftime("%Y_%m_%d-%I%M%p")
        filname=f"{name_path}_{date}"
        outpath = os.path.join(pth,filname)
        pd_dat.to_csv("{}.csv".format(outpath), encoding='ascii')


if __name__='__main__':
    path = "/Users/sandeep/Documents/1-PROJECTS/sts/"
    filename = "Appendix 2 Details on Text Extraction - PyMuPDF Documentation.pdf"
    to_file = os.path.join(path, filename)
    pd_data = extract_2_frame(to_file)

