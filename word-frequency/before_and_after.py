import pandas
poem_before_df = pandas.read_csv('before.csv', sep=',')
poem_after_df = pandas.read_csv('after.csv', sep=',')

combined = []
poem_before_list = list(poem_before_df.itertuples(index=False, name=None))
poem_after_list = list(poem_after_df.itertuples(index=False, name=None))
before_count_count= 375
after_poem_count = 357
before_wc = 50029
after_wc = 46184
before_words = []
for i in range (0, len(poem_before_list)):
    before_words.append(poem_before_list[i][1])
    percent_before = poem_before_list[i][2]/before_wc
    combined.append([poem_before_list[i][1], poem_before_list[i][2], 0, percent_before, 0, 0])

for i in range (0, len(poem_after_list)):
    if poem_after_list[i][1] in before_words:
        for j in range(0, len(combined)):
            if poem_after_list[i][1] == combined[j][0]:
                combined[j][2] = poem_after_list[i][2]
                percent_after = poem_after_list[i][2]/after_wc
                combined[j][4] = percent_after
                combined[j][5] = combined[j][4] - combined[j][3]

dataframe_ua_compare = pandas.DataFrame.from_records(combined, columns=['Word', 'Occurences_Before', 'Occurences_After', 'Percent_Before', 'Percent_After', 'Delta'])
dataframe_ua_compare.to_csv('compared.csv')