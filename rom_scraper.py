#!/usr/bin/env python3

import requests
import time
from bs4 import BeautifulSoup
import re
import os, sys

sys.path.append('../')
import pdfconverter


def request_content(url):
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
               'Referer': 'https://www.google.com',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Accept-Language': 'en-US,en;q=0.8,nl;q=0.6'})

    if req.status_code == 200:
        print(req.status_code, req.reason)
    else:
        print('something went wrong\nreturned:',req.status_code, req.reason)
        exit(-1)

    raw_content = req.content

    return raw_content


def extract_urls(raw_content, base):
    soup = BeautifulSoup(raw_content,"html.parser")

    pdf_urls = []

    for a in soup.find_all('a', href=True):
        attr = a['href']
        if attr.find('.pdf') != -1 and attr.find('wp-content') == -1:
            if re.search(r"(Ordin.*\d{2}.1[1-2].2018|Ordin.*\d{2}.\d{2}.(2019|202[0-9]))", attr, re.IGNORECASE):
                pdf_urls.append(base + attr)

    return pdf_urls


def download_pdfs(urls, path):
    new_files = []

    os.makedirs(path, exist_ok=True)

    if not os.path.exists(path + '/checked_files.txt'):
        with open(path + '/checked_files.txt', 'w'): pass

    with open(path + '/checked_files.txt', 'r+') as f:
        downloaded_files = f.read()

    for url in urls:
        f_name = url.split('/')[-1]
        if f_name not in downloaded_files:
            pdfconverter.download_file(url, path + '/' + f_name)
            new_files.append(path + '/' + f_name)
            with open(path + '/checked_files.txt', 'a') as f:
                f.write('\n' + time.strftime("%Y-%m-%d %H:%M:%S") + '\n')
                f.write(f_name)

    return new_files


def search(fls, tr):
    matched = 0

    for fl in fls:
        txt = pdfconverter.os_extract_text(fl)
        words = pdfconverter.tokenize_text(txt)
        file, status = pdfconverter.search(words, tr, fl)
        print('\nChecked:', file, 'for', tr, '\nMatched?', status)
        if status is True:
            matched += 1

    if matched == 0:
        print('\nNo Matches Found for', tr, '\n')
    else:
        print('\n** \033[1;31m Found a Match. See Above \033[0;m **\n')


if __name__ == "__main__":
    base_url = 'http://cetatenie.just.ro'
    full_url = base_url + '/' + str(sys.argv[2]).lstrip('/')
    path = os.path.dirname(sys.argv[0]) + '/pdfs'

    target = sys.argv[1]

    content = request_content(full_url)
    urls = extract_urls(content, base_url)
    new_fls = download_pdfs(urls, path)
    if not new_fls:
        print('\nNO new PDFs found\n')
        exit(0)

    search(new_fls, target)
