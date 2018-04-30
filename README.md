# About this repo

This repo contains scripts and resources for automated quality assessement of e-books (EPUB, PDF).


## Usage

    ebooksqa.sh rootDirectory prefixOut

## Output

CSV file (`$prefixOut.csv`) with for each EPUB:

- full path to file
- sequence of *unique* Epubcheck validation *error codes* (no warnings!). Multiple error codes are separated by spaces. The meaning of the error (and warning) code is defined by Epubcheck's [default MessageBundle.properties file
](https://github.com/IDPF/epubcheck/blob/master/src/main/resources/com/adobe/epubcheck/messages/MessageBundle.properties).
- word count (based on extracted text with Apache Tika)
