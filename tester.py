import ccxt
import market_lister
import calculator
import time
import Box

#Initialize objects
mar = market_lister.market_lister()
symbols = mar.get_symbols()
calc = calculator.calculator()
symbol = 'BTC/USDT'
depth = 100

lim = calc.usd_to_btc(200) #get $X  and return XBTC, use this to limit
mar.limit_book = False #if False, the order book will not be limited, you will recieve all values

# A = ccxt.binance({
#  
# B = ccxt.kraken({'enableRateLimit': True})

box = Box.Box()
box.run()
