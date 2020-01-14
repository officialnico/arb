import ccxt
import market_lister
import json
import time
from datetime import datetime
from dateutil import tz
from pytz import timezone


class calculator:

    def __init__(self):
        self.balance = 500 #500$ spending limit


    def write_data(self, symbol):
        temp = ccxt.binance()
        tick = temp.fetch_ticker('BTC/USDT')

        outfile=open('data.txt', 'w')
        json.dump(tick, outfile)
        outfile.close()
        return tick #writes the BTC/USDT tick to data #fetches symbol ticker (binance) and writes it to json file



    def timeMe(self, dt): #returns Eastern Time from UTC, not in use anywhere
        #Hardcode zones:
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/New_York')
        # utc = datetime.utcnow()
        dt = dt[0:18]
        dt = dt.replace("T", " ")
        utc = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        # Tell the datetime object that it's in UTC time zone since
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)
        return central


    def usd_to_btc(self, usd): #estimates the price, used for limiting the book down to your price range
        #not in use yet, still working on it, not crucial
        flag = False
        btc = 0
        symbol = 'BTC/USDT'

        jsonfile=open('data.txt', 'r')

        try: #open data
            data = json.load(jsonfile)
            flag = False

        except Exception as e: #if no json data found
            data = write_data()
            flag = True

        if(flag==False):
            dt = data["datetime"]
            conv = self.timeMe(dt)

            tz = timezone('EST')
            time = datetime.now(tz)
            print("conv:",conv,"\nconv_time:",conv)
            print(time)



        data = {'symbol':14}


    mar = market_lister.market_lister()
    exchangeA = mar.exchangeA
    exchangeB = mar.exchangeB



        #price = ask/usd
        #print(price)

#We need to find out: optimal amount of money needed to make the most profit out of one sale

#1. purchase in lower exchange
#2. tranfer to second exhacnage
#3. sell at second exchange

#profit = HP - Transaction Fee - Withdraw fee -
