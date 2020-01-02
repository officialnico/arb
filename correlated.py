# -*- coding: utf-8 -*-
import xlsxwriter

import ccxt

exchange = ccxt.binance()
symbol = 'LTC/USDT'

# each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
index = 4  # use close price from each ohlcv candle

#ignore these, they specify how deep i want to fetch data
length = 80
height = 15

workbook = xlsxwriter.Workbook('mysheet.xlsx')
worksheet = workbook.add_worksheet()


def print_chart(exchange, symbol, timeframe):

    # get a list of ohlcv candles (OHLCV means Open Price, High Price, Low Price, Close Price, Volume Traded within that timeframe.
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

    previous = ohlcv[0]
    # print datetime and other values
    # Start from the first cell. Rows and columns are zero indexed.
    row1 = 0
    row2 = 0
    col = 0

    slope = []
    for x in ohlcv:
        print(exchange.iso8601(x[0]), x, (x[4]/previous[4])-1)
        slope.append((x[4]/previous[4]) - 1)
        worksheet.write(row2, col, exchange.iso8601(x[0]))
        worksheet.write(row2, col + 1, x[4])
        row2 = row2 + 1

    print("\n" + exchange.name + ' ' + symbol + ' ' + timeframe + ' chart:')

    #itterate through list that has all the rates of change.
    for s in slope:
        worksheet.write(row1, col + 2, s)
        row1 = row1 + 1

    #close workbook
    workbook.close()
    last = x[2]
    return last

# 1h is the timeframe. It gives us data from every hour. 1 tick = 1 hour.
last = print_chart(exchange, symbol, '1h')
print("\n" + exchange.name + ' last price: ' + str(last) + "\n")  # print last closing price
