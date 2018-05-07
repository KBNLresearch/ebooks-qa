#! /usr/bin/env python

import sys
import os
import urllib.request
import codecs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from tabulate import tabulate

"""
Analyses output CSV generated by Bash script, and generates Markdown-formatted report
"""

# Set defaults for pyplot
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (8, 6),
         'axes.labelsize': '18',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

def dfToMarkdown(dataframe, headers='keys'):
    """Convert Data Frame to Markdown table with optionally custom headers"""
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

    # Read CSV to Data Frame
    epubsAll = pd.read_csv(fileEcResults, index_col=0, encoding="utf-8")

    # Create lists to store all individual error and warning codes
    errorsAll = []
    warningsAll = []

    # Iterate over rows and extract errors and warnings fields
    for index, row in epubsAll.iterrows():
        errorsRow = row["errors"]
        warningsRow = row["warnings"]
        
        if not pd.isnull(errorsRow):
            # Split individual error codes into list
            errorsAsList = errorsRow.split(' ')

            # Add error codes to errorsAll
            for error in errorsAsList:
                if error != '':
                    errorsAll.append(error)

        if not pd.isnull(warningsRow):
            # Split individual warning codes into list
            warningsAsList = warningsRow.split(' ')

            # Add warning codes to warningAll
            for warning in warningsAsList:
                if warning != '':
                    warningsAll.append(warning)

    
    # Errors and Warnings lists have different size and are not linked to a file,
    # so we create separate series for them
    errors = pd.Series(np.array(errorsAll))
    warnings = pd.Series(np.array(warningsAll))

    # Number of files
    noEpubs = len(epubsAll)

    fOut.write('\n\n## All EPUBs\n\n')
    fOut.write(dfToMarkdown(epubsAll.describe()))

    # EPUBs with errors
    epubsWithErrors = epubsAll[epubsAll.noErrors > 0]
    fOut.write('\n\n## EPUBs with errors\n\n')
    fOut.write(dfToMarkdown(epubsWithErrors.describe()))
    noEpubsWithErrors = len(epubsWithErrors)

    # EPUBs with warnings
    epubsWithWarnings = epubsAll[epubsAll.noWarnings > 0]
    fOut.write('\n\n## EPUBs with warnings\n\n')
    fOut.write(dfToMarkdown(epubsWithWarnings.describe()))
    noEpubsWithWarnings = len(epubsWithWarnings)

    # EPUBs with errors or warnings
    epubsWithErrorsOrWarnings = epubsAll[(epubsAll.noErrors > 0) | (epubsAll.noWarnings > 0)]
    fOut.write('\n\n## EPUBs with errors or warnings\n\n')
    fOut.write(dfToMarkdown(epubsWithErrorsOrWarnings.describe()))
    noEpubsWithErrorsOrWarnings = len(epubsWithErrorsOrWarnings)

    # EPUBs with word count < 1000
    epubsWithWClt1000 = epubsAll[epubsAll.wordCount < 1000]
    fOut.write('\n\n## EPUBs with less than 1000 words\n\n')
    fOut.write(dfToMarkdown(epubsWithWClt1000.describe()))
    noEpubsWithWClt1000 = len(epubsWithWClt1000)

    # Frequency of EPUB versions
    epubVCounts = epubsAll['epubVersion'].value_counts().to_frame()

    # Add column with relative frequencies
    versionRelFrequencies = []
    for i, row in epubVCounts.iterrows():
        relFrequency = 100*row[0]/noEpubs
        versionRelFrequencies.append(round(relFrequency, 2))
    
    epubVCounts.insert(1, '%', versionRelFrequencies)

    fOut.write('\n\n## EPUB versions\n\n')
    fOut.write(dfToMarkdown(epubVCounts,['epubVersion', 'Count', '% of all EPUBs']))

    # Frequency of errors
    errorCounts = errors.value_counts().to_frame(name="count")

    # Insert columns with error descriptions and relative frequencies
    errorDescriptions = []
    errorRelFrequencies = []

    for i, row in errorCounts.iterrows():
        description = messageLookup.get(i, "n/a")
        errorDescriptions.append(description)

        relFrequency = 100*row["count"]/noEpubs
        errorRelFrequencies.append(round(relFrequency, 2))
        
    errorCounts.insert(0, 'description', errorDescriptions)
    errorCounts.insert(2, '%', errorRelFrequencies)

    fOut.write('\n\n## Frequency of validation errors\n\n')
    fOut.write(dfToMarkdown(errorCounts,['Code', 'Description', 'Count', '% of all EPUBs']))

    ecPlot = errorCounts.sort_values(by="count").plot(kind='barh',
                                                      y='count',
                                                      lw=2.5,
                                                      figsize=(8,8))

    ecPlot.set_xlabel('Count')
    ecPlot.set_ylabel('Error') 

    fig = ecPlot.get_figure()
    fig.savefig(os.path.join(dirOut, 'errors.png'))

    fOut.write('\n\n![](errors.png)\n')

    # Frequency of warnings
    warningCounts = warnings.value_counts().to_frame(name="count")

    # Insert columns with warning descriptions and relative frequencies
    warningDescriptions = []
    warningRelFrequencies = []

    for i, row in warningCounts.iterrows():
        description = messageLookup.get(i, "n/a")
        warningDescriptions.append(description)

        relFrequency = 100*row["count"]/noEpubs
        warningRelFrequencies.append(round(relFrequency, 2))

    warningCounts.insert(0, 'description', warningDescriptions)
    warningCounts.insert(2, '%', warningRelFrequencies)

    fOut.write('\n\n## Frequency of validation warnings\n\n')
    fOut.write(dfToMarkdown(warningCounts,['Code', 'Description', 'Count', '% of all EPUBs']))

    wcPlot = warningCounts.sort_values(by="count").plot(kind='barh',
                                                        y='count',
                                                        lw=2.5,
                                                        figsize=(8,8))

    wcPlot.set_xlabel('Count')
    wcPlot.set_ylabel('Warning') 
   
    fig = wcPlot.get_figure()
    fig.savefig(os.path.join(dirOut, 'warnings.png'))

    fOut.write('\n\n![](warnings.png)\n')

    # Close report
    fOut.close()

main()

