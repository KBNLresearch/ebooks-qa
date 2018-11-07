#!/bin/bash


# DAISY Run ace for all EPUB files in a directory (no recursion)

if [ "$#" -ne 2 ] ; then
  echo "Usage: run-ace.sh dirIn dirOut" >&2
  exit 1
fi

if ! [ -d "$1" ] ; then
  echo "dirIn must be a directory" >&2
  exit 1
fi

dirIn="$1"
# dirOut, normalise to absolute path
dirOut="$(readlink -f $2)"

while IFS= read -d $'\0' -r file ; do
    # File basename, extension removed
    bName=$(basename "$file" | cut -f 1 -d '.')
    # Submit file to Tika server, using bName as filename hint
    dirOutEpub="$dirOut""/""$bName"
    ace -o "$dirOutEpub" "$file"
    #echo "$dirOutEpub" "$file"
done < <(find $dirIn -name '*.epub' -type f -print0)
