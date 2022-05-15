import csv
import re
import pandas as pd
from pandas import Series, DataFrame
from sklearn.preprocessing import StandardScaler


########## Import Data (variables) ##########

file = open('data_convert1.csv', 'r', encoding='UTF-8-SIG')
lines = csv.reader(file)

data = []
for line in lines:
    data.append(line)
file.close()
data = DataFrame(data[1:len(data)], columns=data[0])

print("Print Data Columns Name:\n", data.columns.tolist())
print("\nPrint Data:\n", data)


########## Extract Data Columns ##########

extract_list = ['id', 'loan_status', 'term', 'home_ownership', 'purpose',
                'earliest_cr_line', 'initial_list_status']
data_extract = data[extract_list] # 6 columns
data_trans = data
data_trans.drop(columns = extract_list, axis = 1, inplace = True) # 23 columns


########## Feature Scaling ##########

scaler = StandardScaler()
scaler.fit(data_trans)
data_transformed = scaler.transform(data_trans)
data_transformed = DataFrame(data_transformed, columns=data_trans.columns)

data = pd.concat([data_extract, data_transformed], axis = 1) # Concat data


#################### Print and save to csv file ####################

print("Print Data Columns Name:\n", data.columns.tolist())
print("\nPrint Data:\n", data)

data.to_csv('data_convert2.csv', sep=',', na_rep='NaN',
            float_format = '%.3f', # 3 decimal places
            columns = data.columns, index = False)