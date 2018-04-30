#!/bin/bash

# Location of EpubCheck Jar
epubcheckJar=~/epubcheck/epubcheck.jar

file=./test/epub20_encryption_binary_content.epub
outFile=bullsh.csv

rm $outFile

ecMessages=$(java -jar $epubcheckJar "$file" -e -out - | \
xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:messages/_:message/@subMessage' \
- 2>>"epubcheck.err")

echo $ecMessages >> $outFile

# Only kreep unique messsages
ecMessagesUnique=$(echo -e -n "${ecMessages// /\\n}" | sort -u)

# Write line to output file        
echo "$file",$ecMessagesUnique >> $outFile

