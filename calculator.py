import ccxt
import market_lister



mar = market_lister.market_lister()

#data_dict = mar.print_chart()
balance = 500 #500$ spending limit
symbols = mar.get_symbols()
#function, to calculate using the 500$ spending limit, find out the maximum amount of profit from one cycle

#We need to find out: optimal amount of money needed to make the most profit out of one sale

#1. purchase in lower exchange
#2. tranfer to second exhacnage
#3. sell at second exchange

mar.print_orderbook()


#for x in symbols:
    #print(data_dict[x])

#profit = HP - Transaction Fee - Withdraw fee -
