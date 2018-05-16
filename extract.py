#! /usr/bin/env python

import sys
import os
import shutil
import time
import urllib.request
import codecs
import subprocess as sub
import multiprocessing

# Dependencies:
#
# - java
# - EpubCheck
# - tika-server (see link here: https://tika.apache.org/download.html)

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

    return(exitStatus, outputAsString, errorsAsString)


def launchTikaServer():
    args = ['java']
    args.append(''.join(['-jar']))
    args.append(''.join([tikaServerJar]))
    status, out, err = launchSubProcess(args)

def runEpubCheck(epub):
    args = ['java']
    args.append(''.join(['-jar']))
    args.append(''.join([epubcheckJar]))
    args.append(''.join([epub]))
    args.append(''.join(['--out']))
    args.append(''.join(['tmp.xml']))
    status, out, err = launchSubProcess(args)
    return status, out, err

def main():

    global epubcheckJar
    global tikaServerJar
    global tikaServerURL
   
    # Location of EpubCheck Jar
    epubcheckJar = os.path.normpath('/home/johan/epubcheck/epubcheck.jar')

    # Location of Tika server Jar
    tikaServerJar = os.path.normpath('/home/johan/tika/tika-server-1.17.jar')

    # Server URL
    tikaServerURL = 'http://localhost:9998/'

    # Defines no. of seconds script waits to allow the Tika server to initialise   
    sleepValue = 3

    rootDir = sys.argv[1]
    outFile = sys.argv[2]

    # Launch Tika server as a sub process 
    t1 = multiprocessing.Process(target=launchTikaServer)
    t1.start()

    # Allow some time for the server to initialise
    time.sleep(sleepValue)

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
        ecStatus, ecOut, ecErr = runEpubCheck(epub)
        print(str(ecStatus), ecErr)

    t1.terminate()
    t1.join()
    #args = [config.dBpowerampConsoleRipExe]
    #args.append("".join(["--drive=", config.cdDriveLetter]))
    #args.append("".join(["--log=", logFile]))
    #args.append("".join(["--path=", writeDirectory]))

    # Command line as string (used for logging purposes only)
    #cmdStr = " ".join(args)

    #status, out, err = shared.launchSubProcess(args)

main()


