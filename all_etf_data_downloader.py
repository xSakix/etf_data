from pandas_datareader import data as data_reader
import pandas
import os

from pandas_datareader._utils import RemoteDataError


def load_all_data(assets, end_date, start_date, max_size=50,prefix=None):
    data_source = 'yahoo'
    file_open = 'etf_data_open.csv'
    file_close = 'etf_data_close.csv'
    file_low = 'etf_data_low.csv'
    file_high = 'etf_data_high.csv'
    file_adj_close = 'etf_data_adj_close.csv'
    if prefix != '':
        file_open = prefix+file_open
        file_close = prefix+file_close
        file_low = prefix+file_low
        file_high = prefix+file_high
        file_adj_close = prefix+file_adj_close
    panel_data = None
    if len(assets) > max_size:
        times = int(len(assets) / max_size)
        sub_assets = load_sub_assets_list(assets, max_size, times)
        open, close, high, low, adj_close = load_panel_data_many(data_source, end_date, panel_data, start_date,
                                                                 sub_assets)
        open.to_csv(file_open)
        close.to_csv(file_close)
        high.to_csv(file_high)
        low.to_csv(file_low)
        adj_close.to_csv(file_adj_close)
    else:
        panel_data = data_reader.DataReader(assets, data_source, start_date, end_date)
        panel_data.ix['Open'].to_csv(file_open)
        panel_data.ix['Close'].to_csv(file_close)
        panel_data.ix['High'].to_csv(file_high)
        panel_data.ix['Low'].to_csv(file_low)
        panel_data.ix['Adj Close'].to_csv(file_adj_close)


def load_panel_data_many(data_source, end_date, panel_data, start_date, sub_assets):
    open, close, high, low, adj_close,panel_data = None, None, None, None, None, None

    for sub in sub_assets:
        print('loading :' + str(sub))
        adj_close, close, high, low, open,panel_data = load_sub_set(adj_close, close, data_source, end_date, high, low, open,
                                                         panel_data, start_date, sub)


    return open, close, high, low, adj_close


def load_sub_set(adj_close, close, data_source, end_date,  high, low, open, panel_data, start_date, sub):
    err = True
    while (err):
        try:
            if panel_data is None:
                panel_data = data_reader.DataReader(sub, data_source, start_date, end_date)
                open = panel_data.ix['Open']
                close = panel_data.ix['Close']
                high = panel_data.ix['High']
                low = panel_data.ix['Low']
                adj_close = panel_data.ix['Adj Close']
            else:
                panel_data = data_reader.DataReader(sub, data_source, start_date, end_date)
                open = open.join(panel_data.ix['Open'])
                close = close.join(panel_data.ix['Close'])
                high = high.join(panel_data.ix['High'])
                low = low.join(panel_data.ix['Low'])
                adj_close = adj_close.join(panel_data.ix['Adj Close'])
            err = False
        except RemoteDataError:
            err = True

    return adj_close, close, high, low, open,panel_data


def load_sub_assets_list(assets, max_size, times):
    sub_assets = []
    for i in range(times):
        bottom = i * max_size
        top = (i + 1) * max_size
        if top > len(assets):
            top = -1
        sub_assets.append(assets[bottom: top])
    return sub_assets


prefix = 'xetra_'
if prefix != '':
    with open(prefix+'etfs.txt', 'r') as fd:
        etf_list = list(fd.read().splitlines())

    etf_list = list(set(etf_list))
    start_date = '1993-01-01'
    end_date = '2017-12-31'
    load_all_data(etf_list, end_date, start_date, max_size=5,prefix=prefix)
    data = pandas.read_csv(prefix+'etf_data_open.csv')
    print(data.keys())
    print(data.index)

else:
    inception = pandas.read_csv('etf_inc_date.csv', sep=';')
    inception = inception.sort_values(by=['inc_date'])
    etfs = inception['ticket'].values
    print(etfs)
    start_date = min(inception.inc_date.values)
    print(start_date)
    end_date = '2017-12-31'
    print(end_date)
    load_all_data(etfs, end_date, start_date, max_size=5)
    data = pandas.read_csv('etf_data_open.csv')
    print(data.keys())
    print(data.index)
