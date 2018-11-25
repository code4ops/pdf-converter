# PDF to Text Converter

#### Features:
* Convert PDF into text by using standard pdftotext binary
* Optionally convert PDF into text by using PyPDF2 module
* Optionally convert PDF into text by using ImageMagick and Tesseract
* Choose to download PDF from URL or convert locally saved PDF
* Search PDF text for a string


### Prerequisites:
* Python version => 3
#### External dependencies:
1. PyPDF2
2. nltk
3. ImageMagick
4. Tesseract OCR

#### Getting Started:

*Make sure that you have ***pdftotext*** installed and binary is in your PATH*

`yum install poppler-utils`
or
`apt-get install poppler-utils`

*Install ***PyPDF2*** and ***nltk*** modules*

`pip3 install PyPDF2 nltk --user`

##### * Optional installation for `--image-converter` to work *
*Install ***ImageMagick*** for your OS*

`http://www.imagemagick.org/script/download.php`

*Install ***Tesseract OCR*** for your OS*

`https://github.com/tesseract-ocr/tesseract/wiki`


#### List all options:
*Execute `--help` to display options*

```
shell#: python3 pdfconverter.py --help
usage: pdfconverter.py [-h] [-d DOWNLOAD] [--save-path SAVE_PATH] [-p PATH]
                    [-s SEARCH] [-r] [--pypdf-converter] [--image-converter]

Converts PDF file to text and allows searching for string. Uses
pdftotext binary by default

optional arguments:
  -h, --help            show this help message and exit
  -d DOWNLOAD, --download DOWNLOAD
                        URL from where to download PDF file
  --save-path SAVE_PATH
                        Path where to save downloaded PDF file. Default is
                        /tmp
  -p PATH, --path PATH  Path from where to read locally saved PDF file
  -s SEARCH, --search SEARCH
                        Search for string in PDF file
  -r, --raw-text        Enable to output raw text to screen. Default is False
  --pypdf-converter     Enable to use PyPDF2 instead of system's pdftotext
                        converter. Default is False
  --image-converter     Enable to use ImageMagic and Tesseract for image to
                        text conversion. Default is False
```
