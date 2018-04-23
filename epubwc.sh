#!/bin/bash

# Perform word count on each EPUB file in directory tree; report result as CSV
#
# Dependencies:
#
# - java
# - tika-server (see link here: https://tika.apache.org/download.html)
# - curl (installed by default on most Unix systems)
# - wc (installed by default on most Unix systems)
#

# Location of Tika server Jar
tikaServerJar=~/tika/tika-server-1.17.jar

# Server URL
tikaServerURL=http://localhost:9998/

# Defines no. of seconds script waits to allow the Tika server to initialise   
sleepValue=3

# Check command line args
if [ "$#" -ne 2 ] ; then
  echo "Usage: epubwc.sh rootDirectory outputFile" >&2
  exit 1
fi

if ! [ -d "$1" ] ; then
  echo "rootDirectory must be a directory" >&2
  exit 1
fi

# Root directory
rootDir="$1"

# Output file
outFile="$2"

# File to store stderr output for tika server and extraction process
tikaServerErr=tika-server.stderr
tikaExtractErr=tika-extract.stderr

# Delete output file if it exists already
if [ -f $outFile ] ; then
  rm $outFile
fi

# Delete tika server stderr file if it exists already
if [ -f $tikaServerErr ] ; then
  rm $tikaServerErr
fi

# Delete tika extract stderr file if it exists already
if [ -f $tikaExtractErr ] ; then
  rm $tikaExtractErr
fi

# Launch the Tika server as a subprocess
java -jar $tikaServerJar 2>>$tikaServerErr & export Tika_PID=$!
echo "Tika PID = "$Tika_PID
echo "Waiting for Tika server to initialise ..."
sleep $sleepValue

# Write header line to output file
echo "fileName","wordCount" >> $outFile

echo "Processing directory tree ..."

# Record start time
start=`date +%s`

# This works for filenames that contain whitespace using code adapted from:
# http://stackoverflow.com/questions/7039130/bash-iterate-over-list-of-files-with-spaces/7039579#7039579

while IFS= read -d $'\0' -r file ; do
    # Submit file to Tika server, extract text and count number of words
    wordCount=$(curl -T "$file" "$tikaServerURL"tika --header "Accept: text/plain" 2>> $tikaExtractErr | wc -w)
    # Write result to output file
    echo $file,$wordCount >> $outFile
done < <(find $rootDir -name '*.epub' -type f -print0)
 
# Record end time
end=`date +%s`

runtime=$((end-start))
echo "Running time for processing directory tree:" $runtime "seconds"

# Terminate Tika server
fuser -k 9998/tcp
