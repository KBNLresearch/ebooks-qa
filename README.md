# About this repo

This repo contains scripts and resources for automated quality assessement of e-books (for now only EPUB; PDF may follow later).

## Dependencies

- java
- [Epubcheck](https://github.com/IDPF/epubcheck) (tested with v. 4.0.2)
- [Apache Tika](https://tika.apache.org)'s *tika-server* JAR (available for download at <https://tika.apache.org/download.html>)
- xmlstarlet
- curl (installed by default on most Unix systems)
- wc (installed by default on most Unix systems)

## Usage

    ebooksqa.sh rootDirectory prefixOut

## Output

Comma-delimited text file (`$prefixOut.csv`) with for each EPUB the following columns:

- **fileName**: full path to file
- **epubVersion**: EPUB version string
- **epubStatus**: EpubCheck validation outcome
- **noErrors**: number of *unique* errors reported by EpubCheck
- **noWarnings**: number of *unique* warnings reported by EpubCheck
- **errors**: space-delimited list of *unique* errors reported by EpubCheck
- **warnings**: space-delimited list of *unique* warnings reported by EpubCheck
- **wordCount**: word count (based on extracted text with Apache Tika)

Errors and warnings are reported as codes; the meaning of these codes can be found in EpubCheck's [default MessageBundle.properties file
](https://github.com/IDPF/epubcheck/blob/master/src/main/resources/com/adobe/epubcheck/messages/MessageBundle.properties).


## Example output

    fileName,epubVersion,epubStatus,noErrors,noWarnings,errors,warnings,wordCount
    ./ebooks-test/test/epub20_crazy_columns.epub,2.0.1,Well-formed,0,1,,CSS-017,45
    ./ebooks-test/test/epub20_crazy_fixed_layout.epub,2.0.1,Well-formed,0,1,,CSS-017,84
    ./ebooks-test/test/epub20_dtbook.epub,2.0.1,Well-formed,0,0,,,0
    ./ebooks-test/test/epub20_encryption_binary_content.epub,2.0.1,Not well-formed,2,1,RSC-004 RSC-012,HTM-023,0
    ./ebooks-test/test/epub20_foreign_resource_no_fallback.epub,2.0.1,Not well-formed,1,0,MED-003,,748
    ./ebooks-test/test/epub20_foreign_resource_with_fallback.epub,2.0.1,Well-formed,0,0,,,749
    ./ebooks-test/test/epub20_foreign_resource_with_fallback_noID.epub,2.0.1,Well-formed,0,0,,,749
    ./ebooks-test/test/epub20_minimal.epub,2.0.1,Well-formed,0,0,,,748
    ./ebooks-test/test/epub20_minimal_encryption.epub,2.0.1,Not well-formed,2,0,RSC-004 RSC-012,,0
    ./ebooks-test/test/epub20_missingfontresource.epub,2.0.1,Not well-formed,1,0,RSC-007,,748
    ./ebooks-test/test/epub20_xpgt.epub,2.0.1,Well-formed,0,0,,,748
    ./ebooks-test/test/epub20__invalid_entity.epub,2.0.1,Not well-formed,2,0,RSC-005 RSC-012,,0
    ./ebooks-test/test/epub30_font_obfuscation.epub,3.0.1,Well-formed,0,0,,,4652
