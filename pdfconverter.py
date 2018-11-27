#!/usr/bin/env python3

import re
import argparse
import sys, subprocess, os
import time
import urllib.request
import shutil
import PyPDF2
from nltk import download as nltk_downloader
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# download needed nltk packages
nltk_downloader('punkt')
nltk_downloader('stopwords')


def check_python_version(v):
    v = str(v).split('.')
    try:
        if not 1 < int(v[0]) <= 3:
            raise ValueError('Error: You are requiring invalid Python version',v[0])
    except ValueError as e:
        print(e)
        sys.exit(1)
    if sys.version_info[0] != int(v[0]):
        print('This script requires Python version',v[0] + '+')
        print('You are using {0}.{1}.{2} {3}'.format(sys.version_info[0], sys.version_info[1], sys.version_info[2],sys.version_info[3]))
        sys.exit(1)


def download_file(url, file_name):
    print()
    print(time.strftime("%Y-%m-%d %H:%M:%S"), '|| Starting download of', url)
    try:
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print('\nCreated',  file_name)
        print()
        print(time.strftime("%Y-%m-%d %H:%M:%S"), '|| Finished downloading', url)
    except Exception as error:
        print('Error: Download failed\n', error)
        exit(1)


def os_extract_text(filename):
    args = ["pdftotext",
            '-enc',
            'UTF-8',
            "{0}".format(filename),
            '-']
    res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = res.stdout.decode('utf-8')

    return output


def pypdf_extract_text(filename):
    pdfFileObj = open(filename,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    if pdfReader.isEncrypted:
        pdfReader.decrypt("")

    num_pages = pdfReader.numPages
    count = 0
    text = ""

    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()

    pdfFileObj.close()

    if text != "":
        return text
    else:
        print("Empty file or unable to extract text from " + filename)
        exit(1)


def image_extract_text(filename):
    fl = filename.split('.')[-2].split('/')[-1]

    print('\n', time.strftime("%Y-%m-%d %H:%M:%S"), "|| Converting PDF to Image")
    args = ["convert",
            '-density',
            '300',
            filename,
            '-depth',
            '8',
            '-strip',
            '-background',
            'white',
            '-alpha',
            'off',
            "/tmp/" + fl + ".tiff"]
    print(' '.join(args))
    subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print('\n', time.strftime("%Y-%m-%d %H:%M:%S"), "|| Converting Image to Text")
    args = ["tesseract",
            "/tmp/" + fl + ".tiff",
            '/tmp/' + fl]
    print(' '.join(args))
    subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print('\n', time.strftime("%Y-%m-%d %H:%M:%S"), "|| Deleting", "/tmp/" + fl + ".tiff")
    os.remove("/tmp/" + fl + ".tiff")

    print('\n', time.strftime("%Y-%m-%d %H:%M:%S"), "|| Conversion Completed")
    print("Created file:", '/tmp/' + fl + '.txt\n')

    with open('/tmp/' + fl + '.txt', 'r') as f:
        text = f.read()

    return text


def tokenize_text(text):
    tokens = word_tokenize(text)
    punctuations = ['(', ')', ';', ':', '[', ']', ',', '.']
    stop_words = stopwords.words('english')
    kws = [word for word in tokens if not word in stop_words and not word in punctuations]

    return kws


def search(keywords, target, fl):
    match = ''

    for item in keywords:
        if item.find(target) != -1:
            match = item

    if match:
        print('\n\033[1;31mFound match for {0} \033[0;m\n\033[1;43m{1} in {2}\033[0;m'.format(target, match, fl))
        return fl, True
    else:
        print('\nNo match found for ' + target)
        return fl, False


if __name__ == "__main__":
    check_python_version('3')

    parser = argparse.ArgumentParser(description='Converts PDF file to text and allows searching for string. Uses pdftotext binary by default',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-d', '--download',
                        type=str,
                        help='''URL from where to download PDF file'                                        
                             ''', default='')
    parser.add_argument('--save-path',
                        type=str,
                        help='''Path where to save downloaded PDF file. Default is /tmp
                             ''', default='/tmp')
    parser.add_argument('-p', '--path',
                        type=str,
                        help='''Path from where to read locally saved PDF file
                             ''', default='')
    parser.add_argument('-s', '--search',
                        type=str,
                        help='''Search for string in PDF file
                             ''', default='')
    parser.add_argument('-r', '--raw-text',
                        action='store_true',
                        help='''Enable to output raw text to screen. Default is False
                             ''', default=False)
    parser.add_argument('--pypdf-converter',
                        action='store_true',
                        help='''(Optional) Enable to use PyPDF2 instead of system\'s pdftotext converter. Default is False
                             ''', default=False)
    parser.add_argument('--image-converter',
                        action='store_true',
                        help='''(optional) Enable to use ImageMagic and Tesseract for image to text conversion. Default is False
                             ''', default=False)
    args = parser.parse_args()

    if args.download:
        s_path = args.save_path
        file_url = args.download
        pdf_fle = file_url.split('/')[-1]
        file_path = str(s_path).rstrip('/') + '/' + pdf_fle
        download_file(file_url, file_path)
    elif args.path:
        file_path = args.path

    if not args.download and not args.path:
        print("\nError: Pass either download URL or path to locally saved PDF file\n")
        parser.print_help()
        exit(1)

    if args.pypdf_converter and args.image_converter:
        print('\nError: Pick either --pypdf-converter or --image-converter, not both!\nDon\'t specify either one to use standard pdftotext\n')
        exit(1)

    if args.pypdf_converter:
        txt = pypdf_extract_text(file_path)
    elif args.image_converter:
        txt = image_extract_text(file_path)
    else:
        txt = os_extract_text(file_path)

    if args.raw_text or not args.search:
        for line in txt.split('\n'):
            if not re.match(r'^\s*$', line):
                print(line)

    if args.search:
        tr = args.search
        words = tokenize_text(txt)
        search(words, tr, file_path)
