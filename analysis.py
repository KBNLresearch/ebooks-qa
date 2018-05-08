#! /usr/bin/env python

import sys
import os
import urllib.request
import codecs
import datetime
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

        fOut.write('\nReport generated: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
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

    # EPUBs with errors
    epubsWithErrors = epubsAll[epubsAll.noErrors > 0]
    noEpubsWithErrors = len(epubsWithErrors)
    # Write to CSV
    epubsWithErrors.to_csv(os.path.join(dirOut, 'errors.csv'), encoding='utf-8')

    # EPUBs with warnings
    epubsWithWarnings = epubsAll[epubsAll.noWarnings > 0]
    noEpubsWithWarnings = len(epubsWithWarnings)
    # Write to CSV
    epubsWithWarnings.to_csv(os.path.join(dirOut, 'warnings.csv'), encoding='utf-8')

    # EPUBs with errors or warnings
    epubsWithErrorsOrWarnings = epubsAll[(epubsAll.noErrors > 0) | (epubsAll.noWarnings > 0)]
    noEpubsWithErrorsOrWarnings = len(epubsWithErrorsOrWarnings)
    # Write to CSV
    epubsWithErrorsOrWarnings.to_csv(os.path.join(dirOut, 'errorsorwarnings.csv'), encoding='utf-8')

    # EPUBs with word count < 1000
    epubsWithWClt1000 = epubsAll[epubsAll.wordCount < 1000]
    noEpubsWithWClt1000 = len(epubsWithWClt1000)
    # Write to CSV
    epubsWithWClt1000.to_csv(os.path.join(dirOut, 'wordcountlt1000.csv'), encoding='utf-8')

    # Create summary table
    summaryTable = [
                    ['EPUBs', noEpubs, ''],
                    ['EPUBs with errors', noEpubsWithErrors, round(100*noEpubsWithErrors/noEpubs, 2)],
                    ['EPUBs with warnings', noEpubsWithWarnings, round(100*noEpubsWithWarnings/noEpubs, 2)],
                    ['EPUBs with errors or warnings', noEpubsWithErrorsOrWarnings, round(100*noEpubsWithErrorsOrWarnings/noEpubs, 2)],
                    ['EPUBs with less than 1000 words', noEpubsWithWClt1000, round(100*noEpubsWithWClt1000/noEpubs, 2)]]

    headers = ['', 'Count', '% of all EPUBs']

    fOut.write('\n\n## Summary\n\n')
    fOut.write(tabulate(summaryTable, headers, tablefmt='pipe'))

    # Create table with links to generated CSV files
    csvTable = [
                ['EPUBs with errors', '[errors.csv](errors.csv)'],
                ['EPUBs with warnings', '[warnings.csv](warnings.csv)'],
                ['EPUBs with errors or warnings', '[errorsorwarnings.csv](errorsorwarnings.csv)'],
                ['EPUBs with less than 1000 words', '[wordcountlt1000.csv](wordcountlt1000.csv)']]

    headers = ['', 'File']

    fOut.write('\n\n## CSV subsets\n\n')
    fOut.write(tabulate(csvTable, headers, tablefmt='pipe'))

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
    # also report CSV file of all EPUBs for each error code
    errorDescriptions = []
    errorRelFrequencies = []

    for i, row in errorCounts.iterrows():
        description = messageLookup.get(i, "n/a")
        errorDescriptions.append(description)

        relFrequency = 100*row["count"]/noEpubs
        errorRelFrequencies.append(round(relFrequency, 2))

        # Select all corresponding records with this error and write to CSV
        records = epubsWithErrors[epubsWithErrors['errors'].str.contains(str(i))]
        fName = 'error-' + str(i) + '.csv'
        records.to_csv(os.path.join(dirOut, fName), encoding='utf-8')

    errorCounts.insert(0, 'description', errorDescriptions)
    errorCounts.insert(2, '%', errorRelFrequencies)

    fOut.write('\n\n## Frequency of validation errors\n\n')
    fOut.write(dfToMarkdown(errorCounts,['Code', 'Description', 'Count', '% of all EPUBs']))

    fOut.write('\n\n![](errors.png)\n')

    # Frequency of warnings
    warningCounts = warnings.value_counts().to_frame(name="count")

    # Insert columns with warning descriptions and relative frequencies
    # also report CSV file of all EPUBs for each warning code
    warningDescriptions = []
    warningRelFrequencies = []

    for i, row in warningCounts.iterrows():
        description = messageLookup.get(i, "n/a")
        warningDescriptions.append(description)

        relFrequency = 100*row["count"]/noEpubs
        warningRelFrequencies.append(round(relFrequency, 2))

        # Select all corresponding records with this warning and write to CSV
        records = epubsWithWarnings[epubsWithWarnings['warnings'].str.contains(str(i))]
        fName = 'warning-' + str(i) + '.csv'
        records.to_csv(os.path.join(dirOut, fName), encoding='utf-8')

    warningCounts.insert(0, 'description', warningDescriptions)
    warningCounts.insert(2, '%', warningRelFrequencies)

    fOut.write('\n\n## Frequency of validation warnings\n\n')
    fOut.write(dfToMarkdown(warningCounts,['Code', 'Description', 'Count', '% of all EPUBs']))

    fOut.write('\n\n![](warnings.png)\n')

    # Plots of errors and warnings
    ecPlot = errorCounts.sort_values(by="count").plot(kind='barh',
                                                      y='count',
                                                      lw=2.5,
                                                      figsize=(8,8))

    ecPlot.set_xlabel('Count')
    ecPlot.set_ylabel('Error') 

    fig = ecPlot.get_figure()
    fig.savefig(os.path.join(dirOut, 'errors.png'))

    wcPlot = warningCounts.sort_values(by="count").plot(kind='barh',
                                                        y='count',
                                                        lw=2.5,
                                                        figsize=(8,8))

    wcPlot.set_xlabel('Count')
    wcPlot.set_ylabel('Warning') 
   
    fig = wcPlot.get_figure()
    fig.savefig(os.path.join(dirOut, 'warnings.png'))

    # Write detailed statistics
    fOut.write('\n\n## Detailed statistics\n\n')

    fOut.write('\n\n### All EPUBs\n\n')
    fOut.write(dfToMarkdown(epubsAll.describe()))

    fOut.write('\n\n### EPUBs with errors\n\n')
    fOut.write(dfToMarkdown(epubsWithErrors.describe()))

    fOut.write('\n\n### EPUBs with warnings\n\n')
    fOut.write(dfToMarkdown(epubsWithWarnings.describe()))

    fOut.write('\n\n### EPUBs with errors or warnings\n\n')
    fOut.write(dfToMarkdown(epubsWithErrorsOrWarnings.describe()))

    fOut.write('\n\n### EPUBs with less than 1000 words\n\n')
    fOut.write(dfToMarkdown(epubsWithWClt1000.describe()))

    fOut.write('\n')

    # Close report
    fOut.close()

main()

