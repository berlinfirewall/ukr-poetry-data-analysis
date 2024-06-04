import pandas
import sys
import os
import numpy as np
import msgpack
import tokenize_uk
from langdetect import detect
from keras.models import Sequential
from keras.layers import Dense, Dropout
from transformers import pipeline

ru_model = pipeline("text-classification", model="seara/rubert-tiny2-russian-sentiment")
input_csv_file = 'change_this.csv'
output_csv_file = 'xxx_analysis.csv'
df_poems = pandas.read_csv(input_csv_file)
data = []

data_folder = os.path.join(os.getcwd(), 'data/')
result_folder = data_folder + 'result/'

ua_model = Sequential()
ua_model.add(Dense(800, activation='relu', input_shape=(600,)))
ua_model.add(Dropout(0.5))
ua_model.add(Dense(300, activation='tanh'))
ua_model.add(Dropout(0.5))
ua_model.add(Dense(1, activation='sigmoid'))
ua_model.compile(optimizer='adam', loss='mse')

ua_model.load_weights(result_folder + 'predict/model.h5')

with open(result_folder + 'joined_dict', 'rb') as f:
	joined_dict = msgpack.unpack(f)

def get_tone(poem):
	X = np.array( [ joined_dict[word] ] )
	pred = ua_model.predict(X, verbose=0)
	tone = (pred[0][0] - 0.5) * 4
	return(tone)
    

for(id, row) in df_poems.iterrows():
    lang = ""
    try:
        lang = detect(row.loc['Poem full text (copy and paste)'])
    except:
        print("Language not found")

    id_row = 0


    if (lang == 'uk'):
        tone = 0
        score = 0.0
        poem_words = tokenize_uk.tokenize_words(row.loc['Poem full text (copy and paste)'])
        wc = 0
        for word in poem_words:
            try:
                tone = tone + get_tone(word)
                wc = wc+1
            except:
                continue
        
        score = tone/wc
        try:
            id_row = int(str((row.loc['ID'])).replace(',',''))
            data.append([
                            id_row,
                            str(score),
                            "tonal_model_UA",
                            row.loc['Date posted']
                        ])
        except:
            print("invalid ID")
    
    elif (lang == 'ru'):
        poem = row.loc['Poem full text (copy and paste)']
        lines = poem.splitlines()
        score = 0.0
        lc = 0

        for line in lines:            
            result = ru_model(line)
            if (result[0]['label'] == 'positive'):
                score = score + result[0]['score']
            elif (result[0]['label'] == 'negative'):
                score = score - result[0]['score']
            lc = lc + 1

        score = score/lc
        try:
            id_row = int(str((row.loc['ID'])).replace(',',''))
            data.append([
                            id_row,
                            score,
                            "rubert_tiny2",
                            row.loc['Date posted']
                        ])
        except:
            print("invalid ID")
    else:
        print("Language not included")

df = pandas.DataFrame(data, columns=["ID", "score", "method", "date"])
df.to_csv(output_csv_file, sep=';')