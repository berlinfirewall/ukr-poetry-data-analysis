import pandas
import sys
from langdetect import detect

if (len(sys.argv) < 2):
    print("invalid number of args")
else:
    print("Detecting languages for: %s\n" % sys.argv[1])
    for i in range(1, len(sys.argv)):
        df = pandas.read_csv(sys.argv[i])
        for(idx, row) in df.iterrows():
            try:
                language = detect(row.loc['Poem full text'])
                row.loc['language'] = language
                print(language + "\n");
            except:
                print("Error Detecting Language")
            
    