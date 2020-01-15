# -*- coding: utf-8 -*-w
import xlsxwriter
import ccxt
import json
import time
import signal
import sys

class market_lister:

    def __init__(self):
        self.exchangeA = ccxt.binance({
                                        'enableRateLimit': True  # this option enables the built-in rate limiter (no ip ban)
                                        })
        self.exchangeB = ccxt.kraken({
                                        'enableRateLimit': True  # this option enables the built-in rate limiter (no ip ban)
                                        })
        self.symbols = ['BTC/USDT','ETH/USDT'] #add params to add symbols #when this param make sure to check if theyre arbitrage pairs
        self.A = self.exchangeA.name
        self.B = self.exchangeB.name
        self.USD_limit = 30 #USD$
        self.IP_banned = False
        self.timeout_on = False
        self.depth = 100
        self.limit_book = True

    def listCreator(self):
        workbook = xlsxwriter.Workbook('mysheet.xlsx')
        worksheet = workbook.add_worksheet()

        A=self.A
        B=self.B

        data_dict = {}
        timeA = []
        symbolsAB = []
        askA = [] #A
        askB = [] #B
        timeB = []
        diff = []
        favor = []
        rating = []

        worksheet.write(0,2,self.A)
        worksheet.write(0,3,self.B)
        worksheet.write(0,4,"Diff")
        worksheet.write(0,5,"Favor")
        worksheet.write(0,6,"diff/Full_coin_value") #diff/Full_coin_value

        for x in range(0,len(self.symbols)):

            dataA = self.exchangeA.fetch_ticker(self.symbols[x])
            dataB = self.exchangeB.fetch_ticker(self.symbols[x])
            #if dataA

            timeA.append(dataA['datetime'])
            symbolsAB.append(dataA['symbol'])
            askA.append(dataA['ask'])
            askB.append(dataB['ask'])
            timeB.append(dataB['datetime'])
            d=dataA['ask']-dataB['ask']
            #profit = revenue - cost
            #costs = purchase_fee + withdraw fee + coin_purchase_price ### you have to have a range of prices and find the optimal amount and price
            #revenue = coin_sell_price
            print('hi')
            if(d>0):
                higher_price = dataA['ask']
                lower_price = dataB['ask']
                favor.append(A)
            elif(d<0):
                lower_price = dataB['ask']
                higher_price = dataA['ask']
                favor.append(B)
            elif(d==0):
                higher_price = None
                lower_price = None
                favor.append('0')
            diff.append(abs(d))

            rat = (abs(d)/higher_price)*100
            rating.append(rat)
            #coin_sell_price = higher_price

            worksheet.write(x+1,0,timeA[x])
            worksheet.write(x+1,1,self.symbols[x])
            worksheet.write(x+1,2,askA[x])
            worksheet.write(x+1,3,askB[x])
            worksheet.write(x+1,4,diff[x])
            worksheet.write(x+1,5,favor[x])
            worksheet.write(x+1,6,rating[x])

            data_dict.update({self.symbols[x]:{'timeA':timeA[x],'timeB':timeB[x],'askA':askA[x],'askB':askB[x],'diff':diff[x],'rating':rating[x],'favor':favor[x]}})
            #{'BTC/USDT' :{'timeA':timeA,'timeB':timeB,'askA':askA,'askB':askB,'diff':diff,'favor':favor}}
            self.BTC_last = data_dict['BTC/USDT']['askA']
            print(self.BTC_last)
        workbook.close()

        return data_dict

    def print_chart(self): #Prints chart with useful values in terminal
        data_dict = self.listCreator()

        print('\t\t\t\t     ',self.A,'  ',self.B)
        for x in self.symbols:
            temp = data_dict[x]
            print(temp['timeA'],' ',x,' ',temp['askA'],' ',temp['askB'],' ',temp['diff'],' ',temp['favor'],' ',temp['rating'])
        return data_dict

    def get_data(self):
        return self.listCreator()

    def get_symbols(self):
        return self.symbols

    def print_orderbook(self, symbol,lim):

        workbook = xlsxwriter.Workbook('book.xlsx')
        worksheet = workbook.add_worksheet()
        symbol = 'BTC/USDT'
        length = 20
        if(self.timeout_on):
            signal.alarm(5) #Timeout after 5 seconds
        try: #Try getting book
            bookA = self.exchangeA.fetch_order_book(symbol, self.depth)
            #print("BookA recieved")
            bookB = self.exchangeB.fetch_order_book(symbol, self.depth)
            #print("BookB recieved")

        except Exception: #if longer than ~3seconds assume IP Banned
            print("Error fetching book, check IP")
            self.IP_banned = True
            sys.exit(0)

        self.BTC_last = bookA['bids'][0][1]
        bidsA = bookA['bids']
        bidsB = bookB['bids']

        # #Sort from Ascending order by cost Error: Gives incorrect answers for B
        # bidsA = sorted(bidsA, key = lambda x: float(x[1]))
        # bidsB = sorted(bidsB, key = lambda x: float(x[1]))

        bidsA = bidsA[0:self.USD_limit]
        bidsB = bidsB[0:self.USD_limit]
        worksheet.write(0,0,'Amount needed (A)')
        worksheet.write(0,1,"Coin Value (A)")
        worksheet.write(0,2,'Coin Value (B)')
        worksheet.write(0,3,'Amount needed (B)')
        refined_a = []
        refined_b = []

        n=1
        for x in bidsA:
            if(x[1]<=lim or self.limit_book==False):
                worksheet.write(n,1,x[0])
                worksheet.write(n,0,x[1])
                refined_a.append([x[0],x[1]])
                n+=1

        n=1
        for x in bidsB:
            if(x[1]<=lim or self.limit_book==False):
                worksheet.write(n,2,x[0])
                worksheet.write(n,3,x[1])
                refined_b.append([x[0],x[1]])
                n+=1
        print(refined_a)
        print(refined_b)
        workbook.close()
        return (bookA, bookB)

    def handler(signum, frame):
        raise Exception("Timeout")

    def get_exchangeA(self):
        return self.exchangeA

    def get_exchangeB(self):
        return self.exchangeB

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    signal.signal(signal.SIGALRM, handler)
