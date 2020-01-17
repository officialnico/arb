import ccxt
import market_lister
import json
import time
from datetime import datetime
from dateutil import tz
from pytz import timezone


class calculator:

    def __init__(self, usd_cap=8000):
        self.usd_cap = usd_cap

    def write_data(self, symbol): #writes the BTC/USDT tick to data #fetches symbol ticker (binance) and writes it to json file
        temp = ccxt.binance()
        tick = temp.fetch_ticker('BTC/USDT')

        outfile=open('data.txt', 'w')
        json.dump(tick, outfile)
        outfile.close()
        return tick #will be good for use later when we want to cache a ticker to save tike

    def timeMe(self, dt): #returns Eastern Time from UTC, not in use anywhere, would be handy for knowing how old datetime's are
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

    def usd_to_btc(self, usd): #estimates the price, STRICTLY used for limiting the book down to your price range
        #not in use yet, still working on it, not crucial
        flag = False
        btc = 0
        symbol = 'BTC/USDT'

        temp = ccxt.binance()
        tick = temp.fetch_ticker('BTC/USDT')
        ask = tick["ask"]
        quantity = usd/ask
        return quantity

    def analyze(self, asks, bids): # O(N^2)  Not terrribly efficient...
        cap = self.usd_to_btc(self.usd_cap) #cap the plus minus to 5$... for now
        total = []
        first_flag = False #flag to determine whether first compatible element found


        for y in range(0,len(asks)):
            Ap = asks[y][0]
            Aq = asks[y][1]

            for x in range(0,len(bids)):
                temp=[]
                Bp = bids[x][0]
                Bq = bids[x][1]

                # print("Bp ->",Bp)
                # print("Bq ->",Bq)
                # print("Ap ->",Ap)
                # print("Aq ->",Aq)
                # print((Ap<Bp), (Aq>=Bq))
                if((Ap<Bp)and(Aq>=Bq)):

                    first_flag=first_flag^1
                    if(first_flag):
                        pair = [asks[y]]
                        temp.append(bids[x])
                        first_flag=False
                    else:
                        temp.append(bids[x])
                if(len(temp)>0):
                    total.append([pair,temp])
        return total


mar = market_lister.market_lister()
exchangeA = mar.exchangeA
exchangeB = mar.exchangeB

#We need to find out: optimal amount of money needed to make the most profit out of one sale

#1. purchase in lower exchange
#2. tranfer to second exhacnage
#3. sell at second exchange
