import os
import re
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime, date
from argparse import ArgumentParser

fmt = '%Y-%m-%d %H:%M:%S'

def in_range(idx, subset, date_range):
    return date_range[idx] in subset.date.values

def make_plots(data):
    buy = data[data.message.str.contains('Buy')]
    sell = data[data.message.str.contains('Sell')]

    buy = buy.drop_duplicates(subset='date')
    sell = sell.drop_duplicates(subset='date')

    first_date = min(min(buy.date), min(sell.date))
    last_date = max(max(buy.date), max(sell.date))
    date_range = [d.astype('M8[D]').astype('O') for d in np.array(pd.date_range(first_date, last_date))]
    sell_in_range = np.array([in_range(idx, sell, date_range) for idx in range(len(date_range))])
    buy_in_range = np.array([in_range(idx, buy, date_range) for idx in range(len(date_range))])

    # import ipdb; ipdb.set_trace()
    fig = plt.figure()
    ax = fig.add_subplot(111)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_label('Date')
    plt.gca().xaxis.set_ticks([date_range[i] for i in range(5, len(date_range), len(date_range)/10)])
    plt.gca().yaxis.set_label('Successful Transaction')
    plt.gca().set_ylim([-0.5, 2])
    ax.plot(date_range, buy_in_range, label='Buy', ls='-', c='r')
    ax.plot(date_range, sell_in_range, label='Sell', c='g')
    plt.gcf().autofmt_xdate()
    plt.title('Successful Transactions for Neopets/Stocks')
    plt.legend(loc=2)
    plt.savefig('stock_module.png')
    plt.show()

def parse_line(line, sep):
    parts = line.split(sep)
    # I expect 3 parts: time, level, message
    return {
            'date': datetime.strptime(parts[0].split(',')[0], fmt).date(), 
            'level': parts[1],
            'message': parts[2]
            }

def main(path):
    with open(path, 'r') as f:
        lines = []
        for line in f:
            if line.startswith('201'):
                # it's a valid line!!! (has a date at the start)
                lines.append(line.strip())
    
    data = pd.DataFrame(data={
        'datetime': np.array([], dtype=date),
        'level': np.array([], dtype=str),
        'message': np.array([], dtype=str)
        })
    for line in lines:
        if ' - ' in line:
            ld = parse_line(line, ' - ')
            data = data.append(ld, ignore_index=True)
        elif '|' in line:
            ld = parse_line(line, '|')
            data = data.append(ld, ignore_index=True)
        else:
            # I have no idea
            ld = {'datetime':pd.nan, 'level':pd.nan, 'message':line}
            data = data.append(ld, ignore_index=True)

    print data.head()
    print data.tail()
    make_plots(data)

if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('path')
    args = ap.parse_args()

    main(args.path)
