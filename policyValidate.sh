#!/bin/bash

# Simple demo script that demonstrates minimal workflow for policy-based validation of PDFs 
# using veraPDF. Requirements:
#
# * veraPDF
# * Python with lxml (tested with Python 2.7) 

# **************
# CONFIGURATION
# **************

# Installation directory
instDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Location of VeraPDF CLI script -- update according to your local installation!
veraPDF=~/verapdf/verapdf

# Location of post-processing script
extractScript=$instDir/postprocessing.py

# Do not edit anything below this line (unless you know what you're doing) 

# **************
# USER I/O
# **************

# Check command line args
if [ "$#" -ne 3 ] ; then
  echo "Usage: policyValidate.sh pdfDir policy prefixOut" >&2
  exit 1
fi

if ! [ -d "$1" ] ; then
  echo "pdfDir must be a directory" >&2
  exit 1
fi

if ! [ -f "$2" ] ; then
  echo "policy must be a file" >&2
  exit 1
fi

# PDF directory
pdfDir="$1"

# Schema
schema="$2"

# Output file prefix
prefixOut="$3"

# **************
# OUTPUT FILES
# **************

veraOut=$prefixOut"_out.xml"
veraCleaned=$prefixOut"_san.xml"
# File that summarises failed tests for PDFs that didn't pass policy-based validation
summaryFile=$prefixOut"_summary.csv"

# **************
# PROCESSING
# **************

# Run VeraPDF
$veraPDF -x --maxfailuresdisplayed 1 --policyfile $schema $pdfDir/* > $veraOut

# Run post-processing script
python $extractScript $veraOut $veraCleaned $summaryFile

