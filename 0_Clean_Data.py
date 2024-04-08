# Filtrating only confirmed pertussis cases, assign year and week of first symptoms 
# years 2007 to 2022. source: SINAN public data
# Similar to my code for measles-BR 
# Developed by Denise Cammarota

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys 
import glob


def clean_data_total():
    files = glob.glob('./Data/raw/*.csv')
    data_full = pd.DataFrame()
    for file in files:
        # reading data 
        data_test = pd.read_csv(file, 
                                delimiter = ',',
                                index_col=False,
                                parse_dates = ['DT_SIN_PRI','DT_NOTIFIC'], encoding="utf8")
        # get the year we are working with in question
        # first column is read differently
        data_test = data_test.drop(columns = ['Unnamed: 0'])
        #last row is weird 
        data_test = data_test[:-1] 
        # filtered confirmed cases
        names_key = data_test.keys()
        confirmed_class =  confirmed_class = ['1', 1, '1 ']
        data_test = data_test[data_test['CLASSI_FIN'].isin(confirmed_class)]
        # define symptom onset week and year
        data_test['SEM_PRI'] = data_test['SEM_PRI'].astype(str)
        data_test = data_test[~data_test['SEM_PRI'].str.contains('/', regex=False)]
        data_test = data_test[~data_test['SEM_PRI'].str.contains(' ', regex=False)]
        data_test = data_test[~data_test['SEM_PRI'].str.contains('.', regex=False)]
        data_test = data_test[~data_test['SEM_PRI'].str.contains('\x12008', regex=False)]
        data_test = data_test[(data_test['SEM_PRI'].str.len() == 6)]
        data_test['SIN_YEAR'] = data_test['SEM_PRI'].str[0:4]
        data_test['SIN_WEEK'] = data_test['SEM_PRI'].str[4:]
        data_test['SIN_YEAR'] = data_test['SIN_YEAR'].astype('int64')
        data_test['SIN_WEEK'] = data_test['SIN_WEEK'].astype('int64')
        # filtered weird data with symptoms after notification
        filt_df1 = (data_test['DT_NOTIFIC'] >= data_test['DT_SIN_PRI'])
        data_filtered_1 = data_test[filt_df1]
        # filtered weird records with symptoms before 2007 (many of these)
        filt_df2 = (data_filtered_1['SIN_YEAR'] >= 2007)
        data_filtered_2 = data_filtered_1[filt_df2]
        # save in a different path
        if(not(os.path.exists('./Data/processed/'))):
            os.makedirs('./Data/processed/')
        path_save = './Data/processed/'+file[11:]
        data_filtered_2.to_csv(path_save, sep=',')
        data_full = data_full.append(data_filtered_2)
    file_final = './Data/processed/pertusssis_total.csv'
    data_full.to_csv(file_final, sep = ',')
            
    
clean_data_total()

