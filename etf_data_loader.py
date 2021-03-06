import pandas as pd
import numpy as np
import os
import sys


def load_data(assets, start_date, end_date):
    df_open = load_data_from_file('etf_data_open.csv', assets, start_date, end_date)
    df_close = load_data_from_file('etf_data_close.csv', assets, start_date, end_date)
    df_high = load_data_from_file('etf_data_high.csv', assets, start_date, end_date)
    df_low = load_data_from_file('etf_data_low.csv', assets, start_date, end_date)
    df_adj_close = load_data_from_file('etf_data_adj_close.csv', assets, start_date, end_date)
    return df_open, df_close, df_high, df_low, df_adj_close


def load_data_from_file(file, assets, start_date, end_date):
    if not os.path.isfile(file):
        file = '../etf_data/' + file
    if not os.path.isfile(file):
        file = '../../etf_data/' + file
    if not os.path.isfile(file):
        file = '../../../etf_data/' + file

    print('Loading file ',file)

    df = pd.read_csv(file)
    df = df.loc[df.Date > start_date]
    df = df.loc[df.Date < end_date]
    df = df[assets]

    indexes = []

    for key in df.keys():
        for i in df[key].index:
            val = df[key][i]
            try:
                if np.isnan(val) and not indexes.__contains__(i):
                    indexes.append(i)
            except TypeError:
                if not indexes.__contains__(i):
                    indexes.append(i)
    df.drop(indexes, inplace=True)

    return df

def load_data_from_file2(file, assets, start_date, end_date):
    if not os.path.isfile(file):
        file = '../etf_data/' + file
    if not os.path.isfile(file):
        file = '../../etf_data/' + file
    if not os.path.isfile(file):
        file = '../../../etf_data/' + file

    print('Loading file ',file)

    df = pd.read_csv(file)
    df = df.loc[df.date > start_date]
    df = df.loc[df.date < end_date]
    df = df[assets]

    indexes = []

    for key in df.keys():
        for i in df[key].index:
            val = df[key][i]
            try:
                if np.isnan(val) and not indexes.__contains__(i):
                    indexes.append(i)
            except TypeError:
                if not indexes.__contains__(i):
                    indexes.append(i)
    df.drop(indexes, inplace=True)

    return df




def load_all_data_from_file(file, start_date, end_date):
    if not os.path.isfile(file):
        file = '../etf_data/' + file
    if not os.path.isfile(file):
        file = '../' + file
    if not os.path.isfile(file):
        file = '../' + file

    print('Loading file ',file)


    df = pd.read_csv(file)
    df = df.loc[df.Date > start_date]
    df = df.loc[df.Date < end_date]

    # indexes = []
    #
    # for key in df.keys():
    #     for i in df[key].index:
    #         val = df[key][i]
    #         try:
    #             if np.isnan(val) and not indexes.__contains__(i):
    #                 indexes.append(i)
    #         except TypeError:
    #             if not indexes.__contains__(i):
    #                 indexes.append(i)
    # df.drop(indexes, inplace=True)

    return df

def load_all_data_from_file2(file, start_date, end_date):
    if not os.path.isfile(file):
        file = '../etf_data/' + file
    if not os.path.isfile(file):
        file = '../' + file
    if not os.path.isfile(file):
        file = '../' + file

    print('Loading file ',file)


    df = pd.read_csv(file)
    df = df.loc[df.date > start_date]
    df = df.loc[df.date < end_date]

    return df



def load_all_data(start_date, end_date):
    df_open = load_all_data_from_file('etf_data_open.csv', start_date, end_date)
    df_close = load_all_data_from_file('etf_data_close.csv', start_date, end_date)
    df_high = load_all_data_from_file('etf_data_high.csv', start_date, end_date)
    df_low = load_all_data_from_file('etf_data_low.csv', start_date, end_date)
    df_adj_close = load_all_data_from_file('etf_data_adj_close.csv', start_date, end_date)
    return df_open, df_close, df_high, df_low, df_adj_close
