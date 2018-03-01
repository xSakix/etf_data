import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

prefix = 'xetra_'

df_open = pd.read_csv(prefix + 'etf_data_open.csv')
df_close = pd.read_csv(prefix + 'etf_data_close.csv')
df_high = pd.read_csv(prefix + 'etf_data_high.csv')
df_low = pd.read_csv(prefix + 'etf_data_low.csv')
df_adj_close = pd.read_csv(prefix + 'etf_data_adj_close.csv')

if prefix == '':
    with open('etfs.txt', 'r') as fd:
        etfs = list(fd.read().splitlines())

    etfs = list(set(etfs))
    inception = pd.read_csv('etf_inc_date.csv', sep=';')

    count = 1
    for etf in etfs:
        print(str(count) + '/' + str(len(etfs)))
        count += 1
        if etf not in inception.ticket.values:
            continue
        inception_date = inception[inception.ticket == etf].inc_date.values[0]
        df_open.loc[df_open.Date <= inception_date, etf] = 0.
        df_high.loc[df_high.Date <= inception_date, etf] = 0.
        df_low.loc[df_low.Date <= inception_date, etf] = 0.
        df_adj_close.loc[df_adj_close.Date <= inception_date, etf] = 0.
        df_close.loc[df_close.Date <= inception_date, etf] = 0.

df_open.fillna(0., inplace=True)
df_high.fillna(0., inplace=True)
df_low.fillna(0., inplace=True)
df_adj_close.fillna(0., inplace=True)
df_close.fillna(0., inplace=True)

if prefix != '':
    df_open.to_csv(prefix + 'etf_data_open.csv')
    df_close.to_csv(prefix + 'etf_data_close.csv')
    df_high.to_csv(prefix + 'etf_data_high.csv')
    df_low.to_csv(prefix + 'etf_data_low.csv')
    df_adj_close.to_csv(prefix + 'etf_data_adj_close.csv')
else:
    df_open.to_csv('etf_data_open.csv')
    df_close.to_csv('etf_data_close.csv')
    df_high.to_csv('etf_data_high.csv')
    df_low.to_csv('etf_data_low.csv')
    df_adj_close.to_csv('etf_data_adj_close.csv')
