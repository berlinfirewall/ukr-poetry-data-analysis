# ukr-poetry-data-analysis
Repository for storing my scripts and data relating to the Ukrainian poetry archival and analysis project.

## word-frequency
Set of two python scripts.

`data_wrangler.py` takes in a csv file (which was converted and cleaned from original spreadsheet and uses semicolon as delimiter), of the poetry, cleans the data, and generates two output files of poems before 2022 and after 2022, entitled `before.csv` and `after.csv` respectively. These files have one column for words, and another for occurences.

`before_and_after.py` takes both csv files, and combines their output into a CSV file `compared.csv`. This file consists of columns for words, occurences in the before set, occurences in the after set, percentage of total words in the before set, percentage of total words in the after set,
and finally, the change in after minus before percentage.

## sentiment-analysis
`sentiment_analysis_radcliffe.py` was used to run tone analysis on each poem in a CSV file. Determines the language of each poem, and uses either the [lang-uk model](https://lang.org.ua/en/models) for Ukrainian-language poems, or the [`rubert-tiny2-russian-sentiment`](https://huggingface.co/seara/rubert-tiny2-russian-sentiment) model for Russian-language texts mized for the Contemporary Ukrainian Poetry Archive.

`sentiment_analysis_telegram.py` was used to perform the task stated above, but for telegram scraped datasets.

`graph/graph_sentiment.py` used to generate images using matplotlib. Contains a lot of commented out code for different graphs which I created.