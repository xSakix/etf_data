from yahoo_fin.stock_info import get_data
import time
import pandas as pd
import matplotlib.pyplot as plt
import os

prefix = 'mil_'
with open(prefix + 'etfs.txt', 'r') as fd:
    asset_list = list(fd.read().splitlines())

file = prefix + 'etf_data_adj_close.csv'

if os.path.isfile(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame()

start_date = '1993-01-01'
end_date = '2018-06-15'

counter = 0

for ticker in asset_list:
    print('\rprocessed %d/%d: ' % (counter, len(asset_list)), end='')
    if ticker in df.columns:
        continue
    err = True
    err_counter = 5
    while (err and err_counter > 0):
        try:
            # "date","open","high","low","close","adjclose","volume"
            data = get_data(ticker, start_date=start_date, end_date=end_date)
            df[ticker] = data.adjclose
            df = df.fillna(method='bfill')
            df = df.reindex(method='bfill')
            df.to_csv(file)
            counter += 1
            if counter > 0 and counter % 5 == 0:
                time.sleep(1)
            err = False
        except Exception as e:
            print('\r%s failed : %s' % (ticker, e), end='')
            err_counter -= 1
            err = True

print('\n')
print(df.head())
print(df.tail())
print(df.columns)

df = pd.read_csv(file)

print(df.head())
print(df.tail())
print(df.columns)
