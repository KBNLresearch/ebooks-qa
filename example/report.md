# EPUB analysis report

Report generated: 2018-05-08 17:11:22


## Summary

|                                 |   Count | % of all EPUBs   |
|:--------------------------------|--------:|:-----------------|
| EPUBs                           |     808 |                  |
| EPUBs with errors               |     260 | 32.18            |
| EPUBs with warnings             |     285 | 35.27            |
| EPUBs with errors or warnings   |     455 | 56.31            |
| EPUBs with less than 1000 words |       5 | 0.62             |

## CSV subsets

|                                 | File                                         |
|:--------------------------------|:---------------------------------------------|
| EPUBs with errors               | [errors.csv](errors.csv)                     |
| EPUBs with warnings             | [warnings.csv](warnings.csv)                 |
| EPUBs with errors or warnings   | [errorsorwarnings.csv](errorsorwarnings.csv) |
| EPUBs with less than 1000 words | [wordcountlt1000.csv](wordcountlt1000.csv)   |

## EPUB versions

| epubVersion   |   Count |   % of all EPUBs |
|:--------------|--------:|-----------------:|
| 2.0.1         |     808 |              100 |

## Frequency of validation errors

| Code    | Description                                                                       |   Count |   % of all EPUBs |
|:--------|:----------------------------------------------------------------------------------|--------:|-----------------:|
| RSC-005 | Error while parsing file: %1$s                                                    |     219 |            27.1  |
| RSC-007 | Referenced resource '%1$s' could not be found in the EPUB.                        |      44 |             5.45 |
| RSC-020 | '%1$s' is not a valid URI.                                                        |       9 |             1.11 |
| CSS-008 | An error occurred while parsing the CSS: %1$s.                                    |       3 |             0.37 |
| HTM-004 | Irregular DOCTYPE: found '%1$s', expected '%2$s'.                                 |       2 |             0.25 |
| OPF-054 | Date value '%1$s' is not valid as per http://www.w3.org/TR/NOTE-datetime:%2$s.    |       2 |             0.25 |
| RSC-008 | Referenced resource '%1$s' is not declared in the OPF manifest.                   |       2 |             0.25 |
| OPF-031 | File listed in reference element in guide was not declared in OPF manifest: %1$s. |       1 |             0.12 |

![](errors.png)


## CSV subsets for each error

| Code    | File                                   |
|:--------|:---------------------------------------|
| RSC-005 | [error-RSC-005.csv](error-RSC-005.csv) |
| RSC-007 | [error-RSC-007.csv](error-RSC-007.csv) |
| RSC-020 | [error-RSC-020.csv](error-RSC-020.csv) |
| CSS-008 | [error-CSS-008.csv](error-CSS-008.csv) |
| HTM-004 | [error-HTM-004.csv](error-HTM-004.csv) |
| OPF-054 | [error-OPF-054.csv](error-OPF-054.csv) |
| RSC-008 | [error-RSC-008.csv](error-RSC-008.csv) |
| OPF-031 | [error-OPF-031.csv](error-OPF-031.csv) |

## Frequency of validation warnings

| Code    | Description                                                                                            |   Count |   % of all EPUBs |
|:--------|:-------------------------------------------------------------------------------------------------------|--------:|-----------------:|
| PKG-010 | Filename contains spaces, therefore URI escaping is necessary. Consider removing spaces from filename. |     269 |            33.29 |
| PKG-014 | The EPUB contains empty directory '%1$s'.                                                              |      16 |             1.98 |
| CSS-017 | CSS selector specifies absolute position.                                                              |      11 |             1.36 |
| OPF-003 | Item '%1$s' exists in the EPUB, but is not declared in the OPF manifest.                               |       9 |             1.11 |

![](warnings.png)


## CSV subsets for each warning

| Code    | File                                       |
|:--------|:-------------------------------------------|
| PKG-010 | [warning-PKG-010.csv](warning-PKG-010.csv) |
| PKG-014 | [warning-PKG-014.csv](warning-PKG-014.csv) |
| CSS-017 | [warning-CSS-017.csv](warning-CSS-017.csv) |
| OPF-003 | [warning-OPF-003.csv](warning-OPF-003.csv) |

## Detailed statistics


### All EPUBs

|       |   noErrors |   noWarnings |   wordCount |
|:------|-----------:|-------------:|------------:|
| count | 808        |   808        |       808   |
| mean  |   0.34901  |     0.377475 |     94794.1 |
| std   |   0.531043 |     0.540629 |     57001.4 |
| min   |   0        |     0        |         0   |
| 25%   |   0        |     0        |     58295.8 |
| 50%   |   0        |     0        |     87829.5 |
| 75%   |   1        |     1        |    117224   |
| max   |   2        |     3        |    479886   |

### EPUBs with errors

|       |   noErrors |   noWarnings |   wordCount |
|:------|-----------:|-------------:|------------:|
| count | 260        |   260        |       260   |
| mean  |   1.08462  |     0.392308 |     99150   |
| std   |   0.278845 |     0.595947 |     49837.7 |
| min   |   1        |     0        |         0   |
| 25%   |   1        |     0        |     67491   |
| 50%   |   1        |     0        |     94759   |
| 75%   |   1        |     1        |    119047   |
| max   |   2        |     3        |    403903   |

### EPUBs with warnings

|       |   noErrors |   noWarnings |   wordCount |
|:------|-----------:|-------------:|------------:|
| count | 285        |   285        |       285   |
| mean  |   0.350877 |     1.07018  |     99372.1 |
| std   |   0.546797 |     0.294291 |     51074.3 |
| min   |   0        |     1        |         0   |
| 25%   |   0        |     1        |     66394   |
| 50%   |   0        |     1        |     95998   |
| 75%   |   1        |     1        |    126173   |
| max   |   2        |     3        |    446298   |

### EPUBs with errors or warnings

|       |   noErrors |   noWarnings |   wordCount |
|:------|-----------:|-------------:|------------:|
| count | 455        |   455        |       455   |
| mean  |   0.61978  |     0.67033  |    100545   |
| std   |   0.577138 |     0.568152 |     50948.7 |
| min   |   0        |     0        |         0   |
| 25%   |   0        |     0        |     68045   |
| 50%   |   1        |     1        |     97117   |
| 75%   |   1        |     1        |    123271   |
| max   |   2        |     3        |    446298   |

### EPUBs with less than 1000 words

|       |   noErrors |   noWarnings |   wordCount |
|:------|-----------:|-------------:|------------:|
| count |   5        |     5        |        5    |
| mean  |   0.4      |     0.4      |      601.2  |
| std   |   0.894427 |     0.547723 |      359.51 |
| min   |   0        |     0        |        0    |
| 25%   |   0        |     0        |      598    |
| 50%   |   0        |     0        |      659    |
| 75%   |   0        |     1        |      837    |
| max   |   2        |     1        |      912    |
