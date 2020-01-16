import ccxt
import market_lister
import calculator

#Initialize objects
mar = market_lister.market_lister()
symbols = mar.get_symbols()
calc = calculator.calculator()


lim = calc.usd_to_btc(200) #get $X  and return XBTC, use this to limit 
print("lim->",lim)
mar.limit_book = False #if False, the order book will not be limited, you will recieve all values
mar.print_orderbook("BTC/USDT",lim) #generate order book taking away only those orders under the limit
