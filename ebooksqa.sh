#!/bin/bash

# E-book QA
#
# Dependencies:
#
# - java
# - xmlstarlet
# - tika-server (see link here: https://tika.apache.org/download.html)
# - curl (installed by default on most Unix systems)
# - wc (installed by default on most Unix systems)
#

# Location of EpubCheck Jar
epubcheckJar=~/epubcheck/epubcheck.jar

# Location of Tika server Jar
tikaServerJar=~/tika/tika-server-1.17.jar

# Server URL
tikaServerURL=http://localhost:9998/

# Temporary Epubcheck output file
ecTemp=epubcheck_temp.xml

# Defines no. of seconds script waits to allow the Tika server to initialise   
sleepValue=3

# Check command line args
if [ "$#" -ne 2 ] ; then
  echo "Usage: ebooksqa.sh rootDirectory prefixOut" >&2
  exit 1
fi

if ! [ -d "$1" ] ; then
  echo "rootDirectory must be a directory" >&2
  exit 1
fi

# Root directory
rootDir="$1"

# Output file
outFile="$2.csv"

# Files to store stderr output for tika server, extraction process and EpubCheck
tikaServerErr=tika-server.stderr
tikaExtractErr=tika-extract.stderr
eCErr=epubcheck.stderr

# Delete stderr files if they exist already
if [ -f $tikaServerErr ] ; then
  rm $tikaServerErr
fi

if [ -f $tikaExtractErr ] ; then
  rm $tikaExtractErr
fi

if [ -f $eCErr ] ; then
  rm $eCErr
fi

# Launch the Tika server as a subprocess
java -jar $tikaServerJar 2>>$tikaServerErr & export Tika_PID=$!
echo "Tika PID = "$Tika_PID
echo "Waiting for Tika server to initialise ..."
sleep $sleepValue

# Write header line to output file
echo "fileName","identifier","title","author","publisher","epubVersion","epubStatus","noErrors","noWarnings","errors","warnings","wordCount" > $outFile

echo "Processing directory tree ..."

# Record start time
start=`date +%s`

while IFS= read -d $'\0' -r file ; do

    fbasename=$(basename -- "$file")
    extension="${fbasename##*.}"

    if [ $extension == "epub" ] ; then
        # Run Epubcheck
        java -jar $epubcheckJar "$file" -out $ecTemp 2>> $eCErr

        # Extract EPub version and validation oucvome        
        epubVersion=$(xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:version' $ecTemp)
        epubStatus=$(xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:status' $ecTemp)

        # Extract all error codes
        errors=$(xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:messages/_:message[contains(.,"ERROR")]/@subMessage' $ecTemp)

        # Extract all warning codes
        warnings=$(xmlstarlet sel -t -v '/_:jhove/_:repInfo/_:messages/_:message[contains(.,"WARN")]/@subMessage' $ecTemp)

        # Only keep unique errors/warnings
        errorsUnique=$(echo -e -n "${errors// /\\n}" | sort -u)
        warningsUnique=$(echo -e -n "${warnings// /\\n}" | sort -u)

        # Count number of errors and warnings
        errorsArray=( $errorsUnique )
        noErrors=${#errorsArray[@]}

        warningsArray=( $warningsUnique )
        noWarnings=${#warningsArray[@]}

        # Extract identifier (isbn), title, author and publisher name

        identifier=$(xmlstarlet sel -t -v "/_:jhove/_:repInfo/_:properties/_:property[_:name='Info']/_:values/_:property[_:name='Identifier']/_:values/_:value" $ecTemp)
        title=$(xmlstarlet sel -t -v "/_:jhove/_:repInfo/_:properties/_:property[_:name='Info']/_:values/_:property[_:name='Title']/_:values/_:value" $ecTemp)
        author=$(xmlstarlet sel -t -v "/_:jhove/_:repInfo/_:properties/_:property[_:name='Info']/_:values/_:property[_:name='Creator']/_:values/_:value" $ecTemp)
        publisher=$(xmlstarlet sel -t -v "/_:jhove/_:repInfo/_:properties/_:property[_:name='Info']/_:values/_:property[_:name='Publisher']/_:values/_:value" $ecTemp)

        # Submit file to Tika server, extract text and count number of words
        wordCount=$(curl -T "$file" "$tikaServerURL"tika --header "Accept: text/plain" 2>> $tikaExtractErr | wc -w)

        # Write results to output file
        echo \"$file\",\"$identifier\",\"$title\",\"$author\",\"$publisher\",$epubVersion,$epubStatus,$noErrors,$noWarnings,$errorsUnique,$warningsUnique,$wordCount >> $outFile
    fi

    #if [ $extension == "pdf" ] ; then
    #    echo
    #fi

done < <(find $rootDir -type f -print0)

# Clean up
rm $ecTemp

# Record end time
end=`date +%s`

runtime=$((end-start))
echo "Running time for processing directory tree:" $runtime "seconds"

# Terminate Tika server
fuser -k 9998/tcp
