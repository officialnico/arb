# -*- coding: utf-8 -*-w
import xlsxwriter
import ccxt
from tabulate import tabulate

class market_lister:

    def __init__(self):
        self.exchangeA = ccxt.binance()
        self.exchangeB = ccxt.bittrex()
        self.symbols = ['BTC/USDT','LTC/USDT','ETH/USDT','BCH/USDT','XRP/USDT','RVN/USDT','BCH/USDT'] #add params to add symbols #when this param make sure to check if theyre arbitrage pairs
        self.A = self.exchangeA.name
        self.B = self.exchangeB.name

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


        workbook.close()
        return data_dict

    def print_chart(self):
        data_dict = self.listCreator()

        print('\t\t\t\t     ',self.A,'  ',self.B)
        for x in self.symbols:
            temp = data_dict[x]
            print(temp['timeA'],' ',x,' ',temp['askA'],' ',temp['askB'],' ',temp['diff'],' ',temp['favor'],' ',temp['rating'])
        return data_dict

    def get_symbols(self):
        return self.symbols

    def print_orderbook(self):
        workbook = xlsxwriter.Workbook('book.xlsx')
        worksheet = workbook.add_worksheet()
        symbol = 'BTC/USDT'
        length = 20

        bookA = self.exchangeA.fetch_order_book(symbol, 100)
        bookB = self.exchangeB.fetch_order_book(symbol, 100)
        bidsA = bookA['bids']
        bidsB = bookB['bids']
        #Sort from Ascending order by cost
        bidsA = sorted(bidsA, key = lambda x: float(x[1]))
        bidsB = sorted(bidsB, key = lambda x: float(x[1]))

        bidsA = bidsA[0:30]
        bidsB = bidsB[0:30]


        worksheet.write(0,0,'Amount needed (A)')
        worksheet.write(0,1,"Coin Value (A)")
        worksheet.write(0,2,'Coin Value (B)')
        worksheet.write(0,3,'Amount needed (B)')

        n=1
        for x in bidsA:
            worksheet.write(n,1,x[0])
            worksheet.write(n,0,x[1])
            n+=1

        n=1
        for x in bidsB:
            worksheet.write(n,2,x[0])
            worksheet.write(n,3,x[1])
            n+=1
        workbook.close()
