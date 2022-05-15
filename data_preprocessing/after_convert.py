import csv
import re
import pandas as pd
from pandas import Series, DataFrame


########## Function (str to float) ##########
def Pre_str_to_float(data):
    for i in range(len(data)):
        data[i] = float(data[i])
    return data

def Pre_process(data, col_name, func_name):
    data_transformed = func_name(data[col_name])
    data[col_name] = data_transformed
    return data


########## Import Data (variables) ##########

file = open('loan_train_preprocessed.csv', 'r', encoding='UTF-8-SIG')
lines = csv.reader(file)

data = []
for line in lines:
    data.append(line)
file.close()
data = DataFrame(data[1:len(data)], columns=data[0])

print("Print Data Columns Name:\n", data.columns.tolist())
print("\nPrint Data:\n", data)


#################### Pre-processing Data (str to int/float) ####################

pre_float_list = ['loan_amnt', 'funded_amnt'] # str에서 float으로 변환을 원하는 변수들 이름 모두 넣기
for i in pre_float_list:
    data = Pre_process(data, i, Pre_str_to_float)