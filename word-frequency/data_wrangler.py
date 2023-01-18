import pandas
from datetime import datetime

# Verifies dates
#
# Returns boolean

def checkDate(date_str):
    result = True
    try:
        result = bool(datetime.strptime(date_str, "%m/%d/%Y"))
    except Exception as e:
        result = False
    
    return result

# Combines all poems from one set into one string
#
# Returns string

def concatenate_all_poems(list_of_dicts):
    all_poems = ""
    for i in range(0, len(list_of_dicts)):
        all_poems += list_of_dicts[i]['poem_full_text']

    return all_poems    

# Gets list of unique characters and number of occurences in a string.
#
# Returns dictionary, with characters being keys, and values being occurences

def unique_chars(input_str):
    chars = {}
    input_str = input_str.lower()
    for i in range(0, len(input_str)):
        if input_str[i] in chars:
            chars[input_str[i]] += 1
        else:
            chars[input_str[i]] = 1
    
    return chars

# Creates dictionary of words corresponding with frequencies in a string.
#
# Returns dictionary, words being keys, and values being occurences
def gen_word_dict(words):
    words_dict = {}
    for i in range(0, len(words)):
        words[i] = words[i].lower()
        if words[i] in words_dict:
            words_dict[words[i]] += 1
        else:
            words_dict[words[i]] = 1

    return words_dict

# Takes input string, converts all characters to lowercase, and splits into words.
# also removes all items in the words list words consisting of just a dash or empty
# spaces.
#
# Returns list of words
def split_words(input_str):
    input_str = input_str.lower()
    input_str = input_str.replace('\n',' ')
    words = input_str.split(" ")
    words_length = len(words)
    i = 0
    while(i < words_length):
        if words[i] == '-' or words[i] == '':
            del words[i]
            if (i > 0):
                i = i - 1
                words_length = words_length - 1
        else:
            i = i + 1
    return words

# Filter for words in list of words which do not have letters in the Ukrainian alphabet
#
# returns list of words
def filter_non_ukrainian(words):
    filtered = []
    alphabet = ['а','б','в','г','ґ','д','е','є','ж','з','и','і','ї','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ш','щ','ь','ю','я']
    for i in range(0, len(words)):
        for j in range(0, len(alphabet)):
            if alphabet[j] in words[i]:
                filtered.append(words[i])
                break
    return filtered

# Removes punctuation from array of words, which could interfere with data
#
# Returns list of words
def remove_punctuation(words):
    punctuation = ['.',':','?','!','*',',','"',"#"]
    for i in range(0, len(words)):
        for j in range(0, len(punctuation)):
            words[i] = words[i].replace(punctuation[j], '')
    return words

# Takes dictionary of keys and values, converts to list of tuples,
# uses bubble sort to sort by values.
#
# Returns list of tuples
def sort_dict(dict):
    new_list = []
    for key, value in dict.items():
        new_list.append((key, value))

    for i in range (0, len(new_list)):
        swapped = False
        for j in range (len(new_list)-1):
            if (new_list[j][1]< new_list[j+1][1]):
                swapped = True
                temp = new_list[j]
                new_list[j] = new_list[j+1]
                new_list[j+1] = temp
        if swapped == False:
            break

    return new_list

# Main code, imports data from CSV file into pandas dataframe, sorts into 4 lists of poem data,
# based on language (Ukrainian/Russian) and time relative to 2022. Prints statistics and creates two
# csv output files for, in our case, Ukrainian language poems, from before and after 2022, which have
# a list of words and the number of occurences in the two data sets.

poem_df = pandas.read_csv('2022_JAN_15_poem_data.csv', sep=';')

war_year = datetime.strptime("1/1/2022", "%m/%d/%Y")

ukr_before_2022 = []
ukr_after_2022 = []

rus_before_2022 = []
rus_after_2022 = []

invalid_dates = 0
not_counted = 0

for i in range(0,len(poem_df)):
    row_dict = poem_df.iloc[i].to_dict()
    if (checkDate(row_dict['date_posted']) == True):
            poem_date = datetime.strptime(row_dict['date_posted'], "%m/%d/%Y")
            if(row_dict['language'] == 'Ukrainian'):
                if (poem_date > war_year):
                    ukr_after_2022.append(row_dict)
                else:
                    ukr_before_2022.append(row_dict)
            if(row_dict['language'] == 'Russian'):
                if (poem_date > war_year):
                    rus_after_2022.append(row_dict)
                else:
                    rus_before_2022.append(row_dict)
            else:
                not_counted = not_counted + 1
    else:
        invalid_dates = invalid_dates + 1

print('=================STATISTICS=================')
print('Total Poems: %d' % len(poem_df))
print('Poems with Invalid Dates %d' % invalid_dates)
print('Total Not Counted: %d' % not_counted);
print('Total Poems in Ukrainian: %d' % (len(ukr_before_2022) + len(ukr_after_2022)))
print("\tUkrainian Poems before 2022: %d" % len(ukr_before_2022))
print("\tUkrainian Poems after 2022: %d" % len(ukr_after_2022))
print("Total Poems in Russian: %d" % (len(rus_before_2022) + len(rus_after_2022)))
print("\tRussian Poems before 2022: %d" % len(rus_before_2022))
print("\tRussian Poems after 2022: %d" % len(rus_after_2022))
print("Total Words Ukrainian Before %d" % len(filter_non_ukrainian(split_words(concatenate_all_poems(ukr_before_2022)))))
print("Total Words Ukrainian After %d" % len(filter_non_ukrainian(split_words(concatenate_all_poems(ukr_after_2022)))))
print('============================================')
print('\n')

print("Processing poems before 2022")
words_ua_after_2022 = sort_dict(gen_word_dict(remove_punctuation(filter_non_ukrainian(split_words(concatenate_all_poems(ukr_after_2022))))))
words_ua_before_2022 = sort_dict(gen_word_dict(remove_punctuation(filter_non_ukrainian(split_words(concatenate_all_poems(ukr_before_2022))))))


dataframe_ua_before = pandas.DataFrame.from_records(words_ua_before_2022, columns=['Word', 'Occurences'])
dataframe_ua_after = pandas.DataFrame.from_records(words_ua_after_2022, columns=['Word', 'Occurences'])
dataframe_ua_before.to_csv('before.csv')
dataframe_ua_after.to_csv('after.csv')
