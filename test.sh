#!/bin/bash

# Location of EpubCheck Jar
epubcheckJar=~/epubcheck/epubcheck.jar

file=./test/epub20_encryption_binary_content.epub
outFile=bullsh.csv

rm $outFile

#ecMessages=$(java -jar $epubcheckJar "$file" -e -out - | \
#xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:messages/_:message/@subMessage' \
#- 2>>"epubcheck.err")

# Run Epubcheck
epubCheckOut=$(java -jar $epubcheckJar "$file" -e -out - 2>>"epubcheck.err")

# Extract EPub version and validation oucvome        
epubVersion=$(echo $epubCheckOut | xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:version')
epubStatus=$(echo $epubCheckOut | xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:status')

# Extract all values of subMessage attribute (report errors only, no warnings)
ecMessages=$(echo $epubCheckOut | xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:messages/_:message/@subMessage')


echo $ecMessages >> $outFile
echo $epubVersion >> $outFile
echo $epubStatus >> $outFile
echo $epubCreated >> $outFile

# Only kreep unique messsages
ecMessagesUnique=$(echo -e -n "${ecMessages// /\\n}" | sort -u)

# Write line to output file        
echo "$file",$ecMessagesUnique >> $outFile

