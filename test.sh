#!/bin/bash

# Location of EpubCheck Jar
epubcheckJar=~/epubcheck/epubcheck.jar

file=./test/epub20_encryption_binary_content.epub
outFile=bullsh.csv

# Run Epubcheck and extract all values of subMessage attribute (report errors only, no warnings) 
ecMessages=$(java -jar $epubcheckJar "$file" -e -out - | xmllint --xpath \
"//*[local-name()='jhove']/*[local-name()='repInfo']/*[local-name()='messages']/*[local-name()='message']/@subMessage" \
- 2>>"epubcheck.err")
# Delete quotation marks
ecMessages="${ecMessages//'"'}"

# Only keep unique subMessage values
#echo $ecMessages  > $outFile

ecMessagesUnique=$(echo -e "${ecMessages// /\\n}" | sort -u)
#echo $ecMessagesUnique  >> $outFile
# Only keep actual subMessage codes
ecMessagesUnique="${ecMessagesUnique//subMessage=/}"
echo $ecMessagesUnique > $outFile
#echo $ecMessagesUnique,"$file"  >> $outFile
#echo $ecMessagesUnique,$ecMessagesUnique  >> $outFile

bar="RSC-004 RSC-012"
foo="${bar// /:}"
foo2="${ecMessagesUnique// /:}"

echo $bar >> $outFile

echo ${#ecMessagesUnique} >> $outFile
echo ${#bar} >> $outFile

#echo $foo >> $outFile
#echo $foo2 >> $outFile

# Write line to output file        
echo "$file",$ecMessagesUnique >> $outFile
#echo "bla",$foo >> $outFile
