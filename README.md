# ukr-poetry-data-analysis
Repository for storing my scripts and data relating to the Ukrainian poetry archival and analysis project.

## word-frequency
Set of two python scripts.

`data_wrangler.py` takes in a csv file (which was converted and cleaned from original spreadsheet and uses semicolon as delimiter), of the poetry, cleans the data, and generates two output files of poems before 2022 and after 2022, entitled `before.csv` and `after.csv` respectively. These files have one column for words, and another for occurences.

`before_and_after.py` takes both csv files, and combines their output into a CSV file consisting of a columns for words, occurences in the before set, occurences in the after set, percentage of total words in the before set, percentage of total words in the after set,
and finally, the change in after-before percentage.