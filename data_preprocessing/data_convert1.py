import csv
import re
import pandas as pd
from pandas import Series, DataFrame


########## Pre-processing Function - column's characteristic ##########

def Pre_str_to_int(data):
    for i in range(len(data)):
        data[i] = int(data[i])
    return data

def Pre_str_to_float(data):
    for i in range(len(data)):
        data[i] = float(data[i])
    return data

def Pre_term(data):
    for i in range(len(data)):
        if data[i][1:3] == '36': data[i] = int(1)
        elif data[i][1:3] == '60': data[i] = int(0)
    return data

def Pre_sub_grade(data):
    for i in range(len(data)):
        if data[i][0] is 'A':
            data[i] = int(data[i][1]) * 7
        elif data[i][0] is 'B':
            data[i] = int(data[i][1]) * 6
        elif data[i][0] is 'C':
            data[i] = int(data[i][1]) * 5
        elif data[i][0] is 'D':
            data[i] = int(data[i][1]) * 4
        elif data[i][0] is 'E':
            data[i] = int(data[i][1]) * 3
        elif data[i][0] is 'F':
            data[i] = int(data[i][1]) * 2
        else: data[i] = int(data[i][1])
    return data

def Pre_emp_length(data):
    for i in range(len(data)):
        data[i] = re.sub('< 1 year', '0', data[i]) # 1 이하면 0
        data[i] = re.sub('10\+', '10', data[i]) # 10 이상이면 10
        data[i] = re.sub('n/a', '-1', data[i]) # n/a면 -1
        data[i] = re.sub(r'[^0-9]', '', data[i])
        data[i] = int(data[i])
    return data

def Pre_home_ownership(data):
    for i in range(len(data)):
        if data[i] == 'OWN': data[i] = int(5)
        elif data[i] == 'MORTGAGE': data[i] = int(4)
        elif data[i] == 'RENT': data[i] = int(3)
        elif data[i] == 'OTHER': data[i] = int(2)
        elif data[i] == 'NONE': data[i] = int(1)
    return data

def Pre_earliest_cr_line(data):
    for i in range(len(data)):
        if int(data[i][-2:]) < 10:
            data[i] = int(2000)
        elif int(data[i][-2:]) < 20:
            data[i] = int(2010)
        elif int(data[i][-2:]) < 60:
            data[i] = int(1950)
        elif int(data[i][-2:]) < 70:
            data[i] = int(1960)
        elif int(data[i][-2:]) < 80:
            data[i] = int(1970)
        elif int(data[i][-2:]) < 90:
            data[i] = int(1980)
        else: data[i] = int(1990)
    return data

def Pre_initial_list_status(data):
    for i in range(len(data)):
        if data[i] is 'w': data[i] = int(1)
        elif data[i] is 'f': data[i] = int(0)
    return data


########## Pre-processing Function - transformation process ##########

def Pre_process(data, col_name, func_name):
    data_transformed = func_name(data[col_name])
    data[col_name] = data_transformed
    return data



################################################################################
##################################### MAIN #####################################
################################################################################

########## Import Data (variables) ##########

file = open('train/loan_train.csv', 'r', encoding='UTF-8-SIG')
lines = csv.reader(file)

data = []
for line in lines:
    for i in range(len(line)):
        if line[i] is '':
            line[i] = '0'
    data.append(line)
file.close()
data = DataFrame(data[1:len(data)], columns=data[0])


########## Import Data (loan_status) ##########

file = open('train/loan_train_label.csv', 'r', encoding='UTF-8-SIG')
lines = csv.reader(file)

data_label = []
for line in lines:
    data_label.append(line)
file.close()
data_label = DataFrame(data_label[1:len(data_label)], columns=data_label[0])

data = pd.merge(data, data_label, how='outer', on='id') # Merging data

print("Print Data Columns Name:\n", data.columns.tolist())
print("\nPrint Data:\n", data)


########## Delete Columns of Data ##########

drop_list = ['grade', 'emp_title', 'pymnt_plan',
             'title', 'addr_state', 'policy_code']
data.drop(columns = drop_list, axis = 1, inplace = True)


#################### Pre-processing Data (str to int/float) ####################

## For str to int
# pre_int_list = ['loan_status', 'loan_amnt', 'funded_amnt', 'funded_amnt_inv',
#                 'delinq_2yrs', 'inq_last_6mths', 'open_acc', 'pub_rec',
#                 'revol_bal', 'total_acc', 'tot_cur_bal', 'total_rev_hi_lim']
# for i in pre_int_list:
#     data = Pre_process(data, i, Pre_str_to_int)

## For str to float
# pre_float_list = ['int_rate', 'installment', 'annual_inc', 'dti', 'revol_util',
#                   'out_prncp', 'out_prncp_inv' 'recoveries', 'collection_recovery_fee']
# for i in pre_float_list:
#     data = Pre_process(data, i, Pre_str_to_float)


#################### Pre-processing Data (data type) ####################

data = Pre_process(data, 'term', Pre_term)
data = Pre_process(data, 'sub_grade', Pre_sub_grade)
data = Pre_process(data, 'emp_length', Pre_emp_length)
# data = Pre_process(data, 'home_ownership', Pre_home_ownership)
data = Pre_process(data, 'earliest_cr_line', Pre_earliest_cr_line)
data = Pre_process(data, 'initial_list_status', Pre_initial_list_status)


#################### Print and save to csv file ####################

print("Print Data Columns Name:\n", data.columns.tolist())
print("\nPrint Data:\n", data)

data.to_csv('data_convert1.csv', sep=',', na_rep='NaN',
            float_format = '%.3f', # 3 decimal places
            columns = data.columns, index = False)