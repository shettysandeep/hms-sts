'''
Final Approach for Parsing Emails
@ April 28, 2021
'''
import email
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

def gen_list_emails(folder_path):
    ematches = []
    for rt, dnames, fnames in os.walk(folder_path):
        for filename in fnames:
            if filename.endswith('.eml'):
                ematches.append(os.path.join(rt, filename))
    return ematches


# ACSD

ematches = gen_list_emails('./sts_emails/')

sts2=[]
for email1 in ematches:
    print(email1)
    # Part 1 - Read Email
    with open(email1) as f:
        b = email.message_from_file(f)
    body = ""
    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/html' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
    # Part 2 - Soupify
    soup = BeautifulSoup(body, 'html.parser')
    # Part 3 - Parse
    dict1={}
    for el in soup.find_all('div'):
        cnt = 0
        for el2 in el.find_all('b'):
            if 'Email:' in el2.string :
                keyname=el2.string+str(cnt)
                dict1[keyname]=el2.next_sibling.next_sibling.next_sibling.string
                cnt+=1
            txt = el2.next_sibling.next_sibling
            if txt is not None:
                txt2 = txt.string
                dict1[el2.string] = txt2
            else:
                dict1[el2.string] = ''
    sts2.append(dict1)

sts_dat=pd.DataFrame(sts2)
sts_dat.replace(r'\n|\r','',regex=True, inplace=True)
sts_dat.to_csv('sts_April_28.csv')

# INTERMACS

ematches = gen_list_emails('./intermacs_emails/')

intmacs=[]
for email1 in ematches:
    print(email1)
    # Part 1 - Read Email
    with open(email1) as f:
        b = email.message_from_file(f)
    body = ""
    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/html' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
    # Part 2 - Soupify
    soup = BeautifulSoup(body, 'html.parser')
    # Part 3 - Parse
    dict1={}
    for el in soup.find_all('div'):
        cnt = 0
        for el2 in el.find_all('b'):
            if 'Email:' in el2.string :
                keyname=el2.string+str(cnt)
                dict1[keyname]=el2.next_sibling.next_sibling.next_sibling.string
                cnt+=1
            txt = el2.next_sibling.next_sibling
            if txt is not None:
                txt2 = txt.string
                dict1[el2.string] = txt2
            else:
                dict1[el2.string] = ''
    intmacs.append(dict1)


intmacs_dat=pd.DataFrame(intmacs)
intmacs_dat.head()
intmacs_dat.replace(r'\n|\r','',regex=True, inplace=True)

intmacs_dat.to_csv('intermacs_April_28.csv')

# Complete April 28, 2021
'''
Note: I took a procedural approach as it was most convenient. Slight differences
in HTML parsing for ACSD and Intermacs. However, now it appears more functions
will be helpful in reading the code.
'''
import email
from bs4 import BeautifulSoup
import pandas as pd
import os
import re


def gen_list_emails(folder_path):
    ematches = []
    for rt, dnames, fnames in os.walk(folder_path):
        for filename in fnames:
            if filename.endswith('.eml'):
                ematches.append(os.path.join(rt, filename))
    return ematches


def read_email_file(email_pth):
    with open(email_pth) as f:
        b = email.message_from_file(f)
    body = ""
    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/html' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)
    return body


def parse_email(em_body, parser='html.parser'):
    '''Return a Soupified email body'''
    soup = BeautifulSoup(em_body, parser)
    return soup


def extract_info(soup):
    '''Return elements from the Email as a Dictionary'''
    dict1={}
    for el in soup.find_all('div'):
        cnt = 0
        for el2 in el.find_all('b'):
            if 'Email:' in el2.string :
                keyname=el2.string+str(cnt)
                dict1[keyname]=el2.next_sibling.next_sibling.next_sibling.string
                cnt+=1
            txt = el2.next_sibling.next_sibling
            if txt is not None:
                txt2 = txt.string
                dict1[el2.string] = txt2
            else:
                dict1[el2.string] = ''
    return dict1


