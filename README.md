# About this repo

This repo contains scripts and resources for automated quality assessement of e-books (for now only EPUB; PDF may follow later). Scripts require Python 3.x and do *not* work with Python 2.x!

## Dependencies

- java
- [Epubcheck](https://github.com/IDPF/epubcheck) (tested with v. 4.0.2)
- [tika-python](https://github.com/chrismattmann/tika-python) (`pip install tika`)
- [pandas](https://pandas.pydata.org/) (`pip install pandas`)
- [matplotlib](https://matplotlib.org/) (`pip install matplotlib`)
- [python-tabulate](https://github.com/astanin/python-tabulate) (`pip install tabulate`)


## extract.py

This script recursively walks through a directory tree, and runs Epubcheck for each EPUB file (identified by its file extension). It then extracts all validation error and warning codes, removing duplicate codes, and writes them to a comma-delimited text file. Note that the script only reports on *unique* errors and warnings. For example, if an EPUB contains multiple missing referenced resources (error code `RSC-007`), any duplicate instances are removed.

The script also reports some basic metadata (identifier, author, title, publisher) and a word count for each file. The word count can be a useful heuristic for identifying EPUBs that contain only images without any actual text (particularly common for illustrated childrens books of some publishers). For these books the word count is typically less than 1000.

### Epubcheck and Java locations

Since the script wraps around Java and Epubcheck, it needs to know the location of the Epubcheck JAR and Java. Both can be set in the `config.py` script:

```Python
# Epubcheck JAR
epubcheckJar = "~/epubcheck/epubcheck.jar"

# Java interpreter (leave empty to use default java interpreter)
java = ""
```

By default the "java" variable is set to an empty string, in which case the script uses the default "java" command. This usually does the trick on Linux-based systems, but for Windows you may need to specify the full path to the "java" executable. 

### Usage
```
python3 extract.py rootDir prefixOut
```

### Output

The script generates two output files (the names are based on the user-specified value of prefixOut):

1. A comma-delimited text file (\$prefixOut.csv) with, for each EPUB, the following columns:

    - **fileName**: full path to file
    - **identifier**: identifier
    - **title**: title
    - **author**: author name
    - **publisher**: publisher name
    - **epubVersion**: EPUB version string
    - **epubStatus**: EpubCheck validation outcome
    - **noErrors**: number of *unique* errors reported by EpubCheck
    - **noWarnings**: number of *unique* warnings reported by EpubCheck
    - **errors**: space-delimited list of *unique* errors reported by EpubCheck
    - **warnings**: space-delimited list of *unique* warnings reported by EpubCheck
    - **wordCount**: word count (based on extracted text with Apache Tika)

    Errors and warnings are reported as codes; the meaning of these codes can be found in EpubCheck's [default MessageBundle.properties file
    ](https://github.com/IDPF/epubcheck/blob/master/src/main/resources/com/adobe/epubcheck/messages/MessageBundle.properties).

2. A text file (\$prefixOut_ec.txt) with the full Epubcheck output of all proceessed files.

## report.py

### Usage

```
python3 report.py inputFile dirOut
```

Here *inputFile* is the CSV file produced by *extract.py*, and *dirOut* is the name of a directory where all output is written.

## Output

- **report.md**: report in Markdown format
- **report.html**: report in HTML format
- **csv**: directory with CSV files (description can be found in the report, which also links to these files)

## run-ace.sh

Runs DAISY Ace tool on all EPUBs in a directory.

## License

[github-markdown-css](https://github.com/sindresorhus/github-markdown-css) by [Sindre Sorhus](https://sindresorhus.com/), released under the MIT license.
