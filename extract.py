#! /usr/bin/env python

import sys
import os
from epubcheck import EpubCheck
import csv
from lxml import etree
from tika import parser


def validate(epub):
        """Validate file with Epubcheck"""
        ecOut = EpubCheck(epub)
        ecOutMeta = ecOut.meta
        ecOutMessages = ecOut.messages

        # Dictionary for Epubcheck results 
        ecResults = {}

        ecResults['file'] = epub
        ecResults['valid'] = ecOut.valid

        # Metadata
        meta = {}            

        meta['publisher'] = ecOutMeta.publisher
        meta['title'] = ecOutMeta.title
        meta['creator'] = ecOutMeta.creator
        meta['date'] = ecOutMeta.date
        meta['subject'] = ecOutMeta.subject
        meta['description'] = ecOutMeta.description
        meta['rights'] = ecOutMeta.rights
        meta['identifier'] = ecOutMeta.identifier
        meta['language'] = ecOutMeta.language
        meta['nSpines'] = ecOutMeta.nSpines
        meta['checkSum'] = ecOutMeta.checkSum
        meta['renditionLayout'] = ecOutMeta.renditionLayout
        meta['renditionOrientation'] = ecOutMeta.renditionOrientation
        meta['renditionSpread'] = ecOutMeta.renditionSpread
        meta['ePubVersion'] = ecOutMeta.ePubVersion
        meta['isScripted'] = ecOutMeta.isScripted
        meta['hasFixedFormat'] = ecOutMeta.hasFixedFormat
        meta['isBackwardCompatible'] = ecOutMeta.isBackwardCompatible
        meta['hasAudio'] = ecOutMeta.hasAudio
        meta['hasVideo'] = ecOutMeta.hasVideo
        meta['charsCount'] = ecOutMeta.charsCount
        meta['embeddedFonts'] = ecOutMeta.embeddedFonts
        meta['refFonts'] = ecOutMeta.refFonts
        meta['hasEncryption'] = ecOutMeta.hasEncryption
        meta['hasSignatures'] = ecOutMeta.hasSignatures
        meta['contributors'] = ecOutMeta.contributors

        # Validation errors and warnings
        errors = []
        warnings = []
        infos = []
        for ecOutMessage in ecOutMessages:
            message = {}
            message['id'] = ecOutMessage.id
            message['level'] = ecOutMessage.level
            message['location'] = ecOutMessage.location
            message['message'] = ecOutMessage.message
            if ecOutMessage.level in ['ERROR', 'FATAL']:
                errors.append(message)
            elif ecOutMessage.level == 'WARNING':
                warnings.append(message)
            else:
                infos.append(message)
        
        ecResults['valid'] = ecOut.valid
        ecResults['meta'] = meta
        ecResults['errors'] = errors
        ecResults['warnings'] = warnings
        ecResults['infos'] = infos

        return ecResults


def main():

    if len(sys.argv) < 3:
        sys.stderr.write("USAGE: extract.py <rootDir> <prefixOut>\n")
        sys.exit()
    else:
        # Command line args
        rootDir = sys.argv[1]
        prefixOut = sys.argv[2]

    # Output files
    outFile = prefixOut + ".csv"
    ecFile = prefixOut + "_ec.txt"

    # Open output CSV file
    fOut = open(outFile, 'w', encoding='utf-8')

    # Open file with full epubcheck output
    fECFull = open(ecFile, 'w', encoding='utf-8')

    # Create CSV writer object
    csvOut = csv.writer(fOut, lineterminator='\n')

    # Write header row
 
    headerItems = ['fileName', 'identifier', 'title' ,'author', 'publisher', 'epubVersion', 'epubStatus', 'noErrors', 'noWarnings', 'errors', 'warnings', 'wordCount']
    csvOut.writerow(headerItems)

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
        ecResults = validate(epub)

        epubStatus = ecResults['valid']
        epubMeta = ecResults['meta']
        epubErrors = ecResults['errors']
        epubWarnings = ecResults['warnings']

        epubVersion = epubMeta['ePubVersion']
        identifier = epubMeta['identifier']
        title = epubMeta['title']
        author = epubMeta['creator']
        publisher = epubMeta['publisher']

        # Unique error and warning codes
        epubErrorsUnique = []
        for epubError in epubErrors:
            if epubError['id'] not in epubErrorsUnique:
                epubErrorsUnique.append(epubError['id'])

        epubWarningsUnique = []
        for epubWarning in epubWarnings:
            if epubWarning['id'] not in epubWarningsUnique:
                epubWarningsUnique.append(epubWarning['id'])

        # Number of unique error and warning codes
        noErrors = len (epubErrorsUnique)
        noWarnings = len(epubWarningsUnique)

        # Create space-separated strings of unique errors / warnings
        errors = ' '.join(epubErrorsUnique)
        warnings = ' '.join(epubWarningsUnique)

        # Extract text with Tika and count words
        parsed = parser.from_file(os.path.normpath(epub))
        extractedText = parsed["content"].strip()
        noWords = len(extractedText.split())

        # Put all items that are to be written to a list and write row
        rowItems = [epub, identifier, title , author, publisher, epubVersion, epubStatus, noErrors, noWarnings, errors, warnings, noWords]
        csvOut.writerow(rowItems)
        """
        # TODO update this
        # Write full Epubcheck output for this file
        fECFull.write('****\n')
        fECFull.write(epub + '\n')
        fECFull.write(ecOut + '\n')
        fECFull.write(ecErr + '\n')
        """

    # Close output file
    fOut.close()
    fECFull.close()

main()