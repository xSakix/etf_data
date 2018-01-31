import urllib3
from html.parser import HTMLParser
from datetime import datetime
import pandas as pd
import os
import time
import sys
import traceback

class ETFParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.was_row = False
        self.was_label = False
        self.was_label_inc_date = False
        self.was_inc_date = False
        self.inc_date = None

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'rowText':
                    self.was_row = True

        if tag == 'label' and self.was_row:
            self.was_label = True
        if tag == 'span' and self.was_label_inc_date:
            self.was_inc_date = True

    def handle_data(self, data):
        if self.was_label and data == 'Inception Date':
            self.was_label_inc_date = True
        if self.was_inc_date:
            self.inc_date = data
            self.was_inc_date = False
            self.was_label_inc_date = False



loaded = pd.read_csv('etf_inc_date.csv', sep=';')

with open('etf_inc_date.csv', 'a+') as csv_file:
    if not os.path.isfile('etf_inc_date.csv'):
        csv_file.write('ticket;inc_date\n')

with open('etfs.txt', 'r') as fd:
    etfs = list(fd.read().splitlines())

etfs = list(set(etfs))

while len(etfs)-len(loaded.ticket) != 0:

    try:
        count = 1
        for etf in etfs:
            if etf in list(loaded.ticket):
                continue
            count += 1
            print(str(count)+'/'+str(len(etfs)-len(loaded.ticket)))
            http = urllib3.PoolManager()
            response = http.request('GET', 'http://www.etf.com/' + etf)
            if b'Inception Date' not in response.data:
                continue
            parser = ETFParser()
            parser.feed(str(response.data))
            inception_date = parser.inc_date
            d = datetime.strptime(inception_date, '%m/%d/%y')
            with open('etf_inc_date.csv', 'a+') as csv_file:
                csv_file.write(str(etf) + ';' + str(d.date()) + '\n')
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print(''.join('!! ' + line for line in lines)) # Log it or whatever here
        time.sleep(2)
        loaded = pd.read_csv('etf_inc_date.csv', sep=';')
