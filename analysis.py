#! /usr/bin/env python

import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("USAGE: analysis.py <inputFile>\n")
        sys.exit()
    else:
        fileEcResults=sys.argv[1]

    # Read CSV data
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
    df = pd.DataFrame({'fileName' : np.array(fileName),
                        'epubVersion' : np.array(epubVersion),
                        'epubStatus' : np.array(epubStatus),
                        'noErrors' : np.array(noErrors),
                        'noWarnings' : np.array(noWarnings),
                        'wordCount' : np.array(wordCount) })

    # Set data type for each column
    df = df.astype({'fileName': 'U',
                      'epubVersion' : 'U',
                      'epubStatus' : 'U',
                      'noErrors' : 'u2', 
                      'noWarnings' : 'u2',
                      'wordCount' : 'u4'})

    print(df.head())    
    print(df.dtypes)

    """
    print("\nError counts:")
    print(pd.Series(aErrors).value_counts())
    print("\nWarning counts:")
    print(pd.Series(aWarnings).value_counts())
    """
main()

