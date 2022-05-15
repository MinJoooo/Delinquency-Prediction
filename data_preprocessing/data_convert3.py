import csv
import re
import pandas as pd
from pandas import Series, DataFrame


########## One-Hot Encoding Function##########

def Word_to_index(words):
    word_to_index = {}
    for word in words:
        word_to_index[word] = len(word_to_index)
    return word_to_index

def One_hot_encoding(word, word_to_index):
    one_hot_vector = [0]*(len(word_to_index))
    index = word_to_index[word]
    one_hot_vector[index] = 1
    return one_hot_vector

def One_hot_encoding_process(data, col_name, words):
    new_data = []
    word_to_index = Word_to_index(words)
    for i in range(len(data)):
        new_data.append(One_hot_encoding(data[i], word_to_index))
    for i in range(len(words)):
        words[i] = col_name + words[i]
    new_data = DataFrame(new_data, columns=words)
    return new_data

########## Import Data (variables) ##########

file = open('data_convert2.csv', 'r', encoding='UTF-8-SIG')
lines = csv.reader(file)

data = []
for line in lines:
    data.append(line)
file.close()
data = DataFrame(data[1:len(data)], columns=data[0])

print("Print Data Columns Name:\n", data.columns.tolist())
print("\nPrint Data:\n", data)


########## Extract Data Columns ##########

extract_list = ['id', 'home_ownership', 'purpose', 'earliest_cr_line']
data_extract = data[extract_list] # 4 columns

drop_list = ['home_ownership', 'purpose', 'earliest_cr_line']
data.drop(columns = drop_list, axis = 1, inplace = True) # 26 columns


########## Feature Scaling ##########

home_keys = pd.unique(data_extract['home_ownership'])
home_one_hot = One_hot_encoding_process(data_extract['home_ownership'], 'home_ownership', home_keys)
purpose_keys = pd.unique(data_extract['purpose'])
purpose_one_hot = One_hot_encoding_process(data_extract['purpose'], 'purpose', purpose_keys)
earliest_keys = pd.unique(data_extract['earliest_cr_line'])
earliest_one_hot = One_hot_encoding_process(data_extract['earliest_cr_line'], 'earliest_cr_line', earliest_keys)

data = pd.concat([data, home_one_hot, purpose_one_hot, earliest_one_hot], axis = 1) # Concat data


#################### Print and save to csv file ####################

print("Print Data Columns Name:\n", data.columns.tolist())
print("\nPrint Data:\n", data)

data.to_csv('data_convert3.csv', sep=',', na_rep='NaN',
            float_format = '%.3f', # 3 decimal places
            columns = data.columns, index = False)