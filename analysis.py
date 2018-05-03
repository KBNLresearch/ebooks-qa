#! /usr/bin/env python

import sys
import csv
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

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("USAGE: analysis.py <inputFile>\n")
        sys.exit()
    else:
        fileEcResults=sys.argv[1]

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

    # Errors and Warnings lists have different size and are not linked to a file,
    # so we create separate arrays for them
    aErrors = np.array(errorsAll)
    aWarnings = np.array(warningsAll)

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

    epubsAll.describe().to_csv('epub-all.csv')

    # EPUBs with errors
    epubsWithErrors = epubsAll[epubsAll.noErrors > 0]
    epubsWithErrors.describe().to_csv('epub-errors.csv')

    # EPUBs with warnings
    epubsWithWarnings = epubsAll[epubsAll.noWarnings > 0]
    epubsWithWarnings.describe().to_csv('epub-warnings.csv')

    # EPUBs with errors or warnings
    epubsWithErrorsOrWarnings = epubsAll[(epubsAll.noErrors > 0) | (epubsAll.noWarnings > 0)]
    epubsWithErrorsOrWarnings.describe().to_csv('epub-errors-or-warnings.csv')

    # EPUBs with word count < 1000
    epubsWithWClt1000 = epubsAll[epubsAll.wordCount < 1000]
    epubsWithWClt1000.describe().to_csv('epub-wc-gt-1000.csv')

    # Frequency of errors
    errorCounts = pd.Series(aErrors).value_counts()
    errorCounts.to_csv('error-counts.csv')
    ecPlot = errorCounts.sort_values().plot(kind='barh',
                              lw=2.5,
                              figsize=(12,9))

    ecPlot.set_xlabel('Count')
    ecPlot.set_ylabel('Error Code') 

    fig = ecPlot.get_figure()
    fig.savefig('errors.png')    

    # Frequency of warnings
    warningCounts = pd.Series(aWarnings).value_counts()
    warningCounts.to_csv('warning-counts.csv')
    wcPlot = warningCounts.sort_values().plot(kind='barh',
                              lw=2.5,
                              figsize=(12,9))

    wcPlot.set_xlabel('Count')
    wcPlot.set_ylabel('Warning Code') 
   
    fig = wcPlot.get_figure()
    fig.savefig('warnings.png')
 

main()

