#!/bin/bash

# Location of EpubCheck Jar
epubcheckJar=~/epubcheck/epubcheck.jar

file=./test/epub20_encryption_binary_content.epub
outFile=bullsh.csv
# Temporary Epubcheck output file
ecTemp=epubcheck_temp.xml

rm $outFile


# Run Epubcheck
#java -jar $epubcheckJar "$file" -e -out $ecTemp 2>>"epubcheck.err"
java -jar $epubcheckJar "$file" -out $ecTemp 2>>"epubcheck.err"

# Extract Epub version and validation oucvome        
epubVersion=$(xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:version' $ecTemp)
epubStatus=$(xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:status' $ecTemp)

# Extract all error codes
errors=$(xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:messages/_:message[contains(.,"ERROR")]/@subMessage' $ecTemp)

# Extract all warning codes
warnings=$(xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:messages/_:message[contains(.,"WARN")]/@subMessage'  $ecTemp)


# Only keep unique errors and warnings
errorsUnique=$(echo -e -n "${errors// /\\n}" | sort -u)
warningsUnique=$(echo -e -n "${warnings// /\\n}" | sort -u)

echo $errors >> $outFile
echo $warnings >> $outFile
echo $epubVersion >> $outFile
echo $epubStatus >> $outFile
echo $epubCreated >> $outFile


# Write line to output file        
echo "$file",$errorsUnique,$warningsUnique >> $outFile

rm $ecTemp

