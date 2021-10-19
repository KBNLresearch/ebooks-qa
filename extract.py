#! /usr/bin/env python

import sys
import os
import shutil
import time
import codecs
import multiprocessing
import subprocess as sub
import psutil
import csv
import requests
from lxml import etree
import tika
from tika import parser

# Dependencies:
#
# - java
# - EpubCheck

def launchSubProcess(args):
    """Launch subprocess and return exit code, stdout and stderr"""
    try:
        # Execute command line; stdout + stderr redirected to objects
        # 'output' and 'errors'.
        # Setting shell=True avoids console window poppong up with pythonw
        p = sub.Popen(args, stdout=sub.PIPE, stderr=sub.PIPE, shell=False)
        output, errors = p.communicate()

        # Decode to UTF8
        outputAsString = output.decode('utf-8')
        errorsAsString = errors.decode('utf-8')

        exitStatus = p.returncode

    except Exception:
        # I don't even want to to start thinking how one might end up here ...

        exitStatus = -99
        outputAsString = ""
        errorsAsString = ""

    return(p, exitStatus, outputAsString, errorsAsString)


def runEpubCheck(epub):
    args = ['java']
    args.append(''.join(['-jar']))
    args.append(''.join([epubcheckJar]))
    args.append(''.join([epub]))
    args.append(''.join(['-q']))
    args.append(''.join(['--out']))
    args.append(''.join(['-']))
    p, status, out, err = launchSubProcess(args)
    return p, status, out, err


def main():

    global epubcheckJar

    if len(sys.argv) < 4:
        sys.stderr.write("USAGE: extract.py <rootDir> <outCSV> <outErr>\n")
        sys.exit()
    else:
        # Command line args
        rootDir = sys.argv[1]
        outFile = sys.argv[2]
        errFile = sys.argv[3]

    # Location of EpubCheck Jar
    epubcheckJar = os.path.normpath('/home/johan/epubcheck/epubcheck.jar')

    # Open output CSV file
    fOut = open(outFile, 'w', encoding='utf-8')

    # Open error file
    fErr = open(errFile, 'w', encoding='utf-8')

    # Create CSV writer object
    csvOut = csv.writer(fOut, lineterminator='\n')

    # Write header row
 
    headerItems = ['fileName', 'identifier', 'title' ,'author', 'publisher', 'epubVersion', 'epubStatus', 'noErrors', 'noWarnings', 'errors', 'warnings', 'wordCount']
    csvOut.writerow(headerItems)

    # Configure XML parser
    utf8_parser = etree.XMLParser(encoding='utf-8', remove_blank_text=True)

    # Namespaces
    NSMAP = {'j': 'http://schema.openpreservation.org/ois/xml/ns/jhove'}

    # Set up list that will contain all EPUBs
    epubs= []

    # Recursively walk through directory tree
    for root, subdirs, files in os.walk(rootDir):

        for subdir in subdirs:
            dirPath = os.path.join(root, subdir)

        for filename in files:
            filePath = os.path.join(root, filename)
            
            if filePath.endswith(('.epub', '.EPUB')):
                epubs.append(filePath)

    for epub in epubs:
        # Run Epubcheck
        ecP, ecStatus, ecOut, ecErr = runEpubCheck(epub)
        # Parse output
        ecOutUTF8 = ecOut.encode('utf-8')
        ecRoot = etree.fromstring(ecOutUTF8, parser=utf8_parser)

        # EPUB version
        epubVersions = ecRoot.xpath('//j:jhove/j:repInfo/j:version',
                                   namespaces=NSMAP)

        # Validation status
        epubStatuses = ecRoot.xpath('//j:jhove/j:repInfo/j:status',
                                   namespaces=NSMAP)

        # Error codes
        
        epubErrors = ecRoot.xpath('//j:jhove/j:repInfo/j:messages/j:message[@severity="error"]/@id',
                                   namespaces=NSMAP)

        # Warning codes

        epubWarnings = ecRoot.xpath('//j:jhove/j:repInfo/j:messages/j:message[@severity="warning"]/@id',
                                   namespaces=NSMAP)

        # Unique error and warning codes
        epubErrorsUnique = list(set(epubErrors))
        epubWarningsUnique = list(set(epubWarnings))

        # Number of unique error and warning codes
        noErrors = len (epubErrorsUnique)
        noWarnings = len(epubWarningsUnique)

        # Create space-separated strings of unique errors / warnings
        errors = ' '.join(epubErrorsUnique)
        warnings = ' '.join(epubWarningsUnique)

        # Extract identifier, title, author and publisher names
        identifiers = ecRoot.xpath('//j:jhove/j:repInfo/j:properties/j:property[j:name="Info"]/j:values/j:property[j:name="Identifier"]/j:values/j:value',
                                   namespaces=NSMAP)
        titles = ecRoot.xpath('//j:jhove/j:repInfo/j:properties/j:property[j:name="Info"]/j:values/j:property[j:name="Title"]/j:values/j:value',
                                   namespaces=NSMAP)
        authors = ecRoot.xpath('//j:jhove/j:repInfo/j:properties/j:property[j:name="Info"]/j:values/j:property[j:name="Creator"]/j:values/j:value',
                                   namespaces=NSMAP)
        publishers = ecRoot.xpath('//j:jhove/j:repInfo/j:properties/j:property[j:name="Info"]/j:values/j:property[j:name="Publisher"]/j:values/j:value',
                                   namespaces=NSMAP)

        if len(epubVersions) != 0:
            epubVersion = epubVersions[0].text
        else:
            epubVersion = ''

        if len(epubStatuses) != 0:
            epubStatus = epubStatuses[0].text
        else:
            epubStatus = ''

        if len(identifiers) != 0:
            identifier = identifiers[0].text
        else:
            identifier = ''

        if len(titles) != 0:
            title = titles[0].text
        else:
            title = ''

        if len(authors) != 0:
            author = authors[0].text
        else:
            author = ''

        if len(publishers) != 0:
            publisher = publishers[0].text
        else:
            publisher = ''

        # Extract text with Tika and count words
        parsed = parser.from_file(os.path.normpath(epub))
        extractedText = parsed["content"].strip()
        noWords = len(extractedText.split())

        # Put all items that are to be written to a list and write row
        rowItems = [epub, identifier, title , author, publisher, epubVersion, epubStatus, noErrors, noWarnings, errors, warnings, noWords]
        csvOut.writerow(rowItems)

        # Write error file
        fErr.write('****\n')
        fErr.write(epub + '\n')
        fErr.write(ecOut + '\n')
        fErr.write(ecErr + '\n')

    # Close output file
    fOut.close()
    fErr.close()

main()