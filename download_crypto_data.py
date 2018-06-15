import quandl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# symbol='GDAX/EUR'
symbol='BCHARTS/BITSTAMPUSD'

df = quandl.get(symbol)
df = df['Open']
df.fillna(method='bfill',inplace=True)
df = pd.DataFrame(df)
print(df.head())
df = pd.pivot_table(df,index='Date').reset_index()
print(df.head())

df.to_csv('btc_data_open.csv',index=False)

plt.plot(df['Open'])
plt.show()

sns.kdeplot(df['Open'])
plt.show()


