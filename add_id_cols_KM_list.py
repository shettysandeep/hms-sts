# -*- coding: utf-8 -*-
"""
__author__: Sandeep Shetty
__date__: July 02, 2021

Returns a list of columns that includes identifying variables such as Record
ID/ STS ID. These variables identify the site and record within the ACSD master
spreadsheet. Katie's list of columns (by site) did not include these variables.
I'm adding these variables to the list. The approach is to retrieve these
variables from the original excel submissions and then append it to Katie's
list.

"""

import os, re
import pandas as pd
import HelperFileManage as hfm


def obtain_non_null_values(dat):
    """ Code to remove null values in column"""
    newdat = {}
    for index in dat.index:
        key = dat.iloc[index, 0]
        non_null = dat.iloc[index, :].notnull().tolist()
        val = dat.iloc[index, non_null].tolist()[1:]
        newdat[key] = val
    return newdat


def add_record_id_cols(data_file, search_term):
    """Returns a list of columns that includes identifying variables such as Record
    ID/ STS ID. These are important variables to identify the site and record
    with the ACSD master spreadsheet. Katie's list of columns (by site) did not
    include these variables. The approach is to retrieve these variables from
    the original excel submissions and then append it to Katie's list.

    keyword arguments:
    data_file -- DataFrame with columns for each site (saved as row)
    search_term -- new columns to look for and append to the list
    """
    cols_by_site = {}
    for index in data_file.index:
        key_file = data_file.iloc[index, 0]
        cols_index = data_file.iloc[index, :].notnull().tolist()
        cols_list = data_file.iloc[index, cols_index][1:]
        cols_by_site[key_file] = [
            items for items in cols_list
            if re.search(search_term, items, re.IGNORECASE)
        ]
    return cols_by_site


if __name__ == '__main__':
    # Directory
    FLDR = '/Users/sandeep/Documents/1-PROJECTS/sts/reports'
    KM_FILE =  'OR_combined_cols_2021_06_21-1042PM_removed variablesKM.xls'

    # Helper class - for data_save()
    h = hfm.HelperFileManage()

    #~~~~ File 1 - Loading KM cols
    dat = pd.read_excel(os.path.join(FLDR, KM_FILE))
    km_cols = obtain_non_null_values(dat=dat)
    km_dat = pd.DataFrame.from_dict(km_cols, orient='index')

    #~~~~ File 2 - Loading all original Columns
    ALL_COLS_FILE = 'KM_variables_2021_07_01-1024AM.csv'
    dat2 = pd.read_csv(os.path.join(FLDR, ALL_COLS_FILE))

    # Keep only variables with the following terms
    SEARCH_TERM = r'(record|id|gender)'

    # Select the columns with the SEARCH TERMS
    cols_with_record_id = add_record_id_cols(dat2, search_term=SEARCH_TERM)
    record_cols = pd.DataFrame.from_dict(cols_with_record_id, orient='index')

    # Merge KM cols with "Record ID/STS ID", etc
    comb_cols = pd.merge(km_dat,
                         record_cols,
                         how='inner',
                         left_index=True,
                         right_index=True)

    # remove null values
    final_dict = obtain_non_null_values(comb_cols.reset_index())

    # Remove duplicate columns names
    for key, val in final_dict.items():
        final_dict[key] = set(val)

    final_dat = pd.DataFrame.from_dict(final_dict, orient='index')
    h.data_save(final_dat, O_DIRECT, "Record_Cols")

#~~~ END
