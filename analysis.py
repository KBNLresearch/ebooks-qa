#! /usr/bin/env python

import sys
import os
import csv
import urllib.request
import codecs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from tabulate import tabulate

# Set defaults for pyplot
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (12, 9),
         'axes.labelsize': '18',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

def dfToMarkdown(dataframe, headers='keys'):
    mdOut = dataframe.pipe(tabulate, headers=headers, tablefmt='pipe')
    return mdOut

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("USAGE: analysis.py <inputFile> <dirOut>\n")
        sys.exit()
    else:
        fileEcResults=sys.argv[1]
        dirOut=os.path.normpath(sys.argv[2])

    if not os.path.isfile(fileEcResults):
        sys.stderr.write("Input file does not exist\n")
        sys.exit()

    if not os.path.isdir(dirOut):
        os.makedirs(dirOut)

    # Download Epubcheck MessageBundle.properties file
    try:        
        response = urllib.request.urlopen('https://raw.githubusercontent.com/IDPF/epubcheck/master/src/main/resources/com/adobe/epubcheck/messages/MessageBundle.properties')
        mbProperties = response.read().decode("utf-8", errors="ignore").split('\n')

    except:
        sys.stderr.write("Cannot read Epubcheck MessageBundle.properties file\n")
        sys.exit()

    # Dictionary that links error/warning codes to descriptions
    messageLookup={}

    for line in mbProperties:
        line.strip()
        if not line.startswith('#') and line != '':
            lineSplit = line.split('=')
            # Replace underscores with '-' (which are output by Epubcheck)
            code = lineSplit[0].replace('_', '-')
            desc = lineSplit[1]
            messageLookup[code] = desc

    # Open output report for writing
    try:
        fOut = codecs.open(os.path.join(dirOut, 'report.md'), "w", "utf-8")
        fOut.write('# EPUB analysis report\n')
    except:
        sys.stderr.write("Cannot write output report\n")
        sys.exit()

    # Read CSV data
    # TODO: might be simpler to use IO tools: https://pandas.pydata.org/pandas-docs/stable/io.html
    fEcResults = open(fileEcResults, "r", encoding="utf-8")
    fEcResultsCSV = csv.reader(fEcResults)
    headerEcResults = next(fEcResultsCSV)
    rowsEcResults = [row for row in fEcResultsCSV]
    fEcResults.close()

    # Lists to store fields
    fileName = []
    epubVersion = []
    epubStatus = []
    noErrors = []
    noWarnings = []
    errorsAll = []
    warningsAll = []
    wordCount = []

    for row in rowsEcResults:
        fileName.append(row[0])
        epubVersion.append(row[1])
        epubStatus.append(row[2])
        noErrors.append(row[3])
        noWarnings.append(row[4])
        wordCount.append(row[7])

        # Split errors, warnings
        errorsAsList = row[5].split(' ')
        warningsAsList = row[6].split(' ')

        for error in errorsAsList:
            if error != '':
                errorsAll.append(error)
        for warning in warningsAsList:
            if warning != '':
                warningsAll.append(warning)


    # Put all attributes that are linked to one file in an array (transpose to make each list a column)
    myArray = np.transpose([epubVersion, epubStatus, noErrors, noWarnings, wordCount])

    # Create data frame
    epubsAll = pd.DataFrame({'fileName' : np.array(fileName),
                        'epubVersion' : np.array(epubVersion),
                        'epubStatus' : np.array(epubStatus),
                        'noErrors' : np.array(noErrors),
                        'noWarnings' : np.array(noWarnings),
                        'wordCount' : np.array(wordCount) })

    # Set data type for each column
    epubsAll = epubsAll.astype({'fileName': 'U',
                      'epubVersion' : 'U',
                      'epubStatus' : 'U',
                      'noErrors' : 'u2', 
                      'noWarnings' : 'u2',
                      'wordCount' : 'u4'})

    
    # Errors and Warnings lists have different size and are not linked to a file,
    # so we create separate series for them
    errors = pd.Series(np.array(errorsAll))
    warnings = pd.Series(np.array(warningsAll))

    fOut.write('\n\n## All EPUBs\n\n')
    fOut.write(dfToMarkdown(epubsAll.describe()))

    # EPUBs with errors
    epubsWithErrors = epubsAll[epubsAll.noErrors > 0]
    fOut.write('\n\n## EPUBs with errors\n\n')
    fOut.write(dfToMarkdown(epubsWithErrors.describe()))

    # EPUBs with warnings
    epubsWithWarnings = epubsAll[epubsAll.noWarnings > 0]
    fOut.write('\n\n## EPUBs with warnings\n\n')
    fOut.write(dfToMarkdown(epubsWithWarnings.describe()))

    # EPUBs with errors or warnings
    epubsWithErrorsOrWarnings = epubsAll[(epubsAll.noErrors > 0) | (epubsAll.noWarnings > 0)]
    fOut.write('\n\n## EPUBs with errors or warnings\n\n')
    fOut.write(dfToMarkdown(epubsWithErrorsOrWarnings.describe()))

    # EPUBs with word count < 1000
    epubsWithWClt1000 = epubsAll[epubsAll.wordCount < 1000]
    fOut.write('\n\n## EPUBs with less than 1000 words\n\n')
    fOut.write(dfToMarkdown(epubsWithWClt1000.describe()))

    # Frequency of EPUB versions
    ebupVCounts = pd.Series(epubVersion).value_counts().to_frame()
    fOut.write('\n\n## EPUB versions\n\n')
    fOut.write(dfToMarkdown(ebupVCounts,['Version', 'Frequency']))

    # Frequency of errors
    errorCounts = errors.value_counts().to_frame(name="count")

    # Insert column with error descriptions
    errorDescriptions = []
    for i, row in errorCounts.iterrows():
        description = messageLookup.get(i, "n/a")
        errorDescriptions.append(description)
    errorCounts.insert(0, 'description', errorDescriptions)

    fOut.write('\n\n## Frequency of validation errors\n\n')
    fOut.write(dfToMarkdown(errorCounts,['Code', 'Description', 'Frequency']))

    ecPlot = errorCounts.sort_values(by="count").plot(kind='barh',
                              lw=2.5,
                              figsize=(12,9))

    ecPlot.set_xlabel('Frequency')
    ecPlot.set_ylabel('Error') 

    fig = ecPlot.get_figure()
    fig.savefig(os.path.join(dirOut, 'errors.png'))

    fOut.write('\n\n![](errors.png)\n')

    # Frequency of warnings
    warningCounts = warnings.value_counts().to_frame(name="count")

    # Insert column with warning descriptions
    warningDescriptions = []
    for i, row in warningCounts.iterrows():
        description = messageLookup.get(i, "n/a")
        warningDescriptions.append(description)
    warningCounts.insert(0, 'description', warningDescriptions)

    fOut.write('\n\n## Frequency of validation warnings\n\n')
    fOut.write(dfToMarkdown(warningCounts,['Code', 'Description', 'Frequency']))

    wcPlot = warningCounts.sort_values(by="count").plot(kind='barh',
                              lw=2.5,
                              figsize=(12,9))

    wcPlot.set_xlabel('Frequency')
    wcPlot.set_ylabel('Warning') 
   
    fig = wcPlot.get_figure()
    fig.savefig(os.path.join(dirOut, 'warnings.png'))

    fOut.write('\n\n![](warnings.png)\n')

    # Close report
    fOut.close()

main()

