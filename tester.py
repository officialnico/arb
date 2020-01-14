import ccxt
import market_lister
import calculator

mar = market_lister.market_lister()
balance = 500 #500$ spending limit
symbols = mar.get_symbols()


# mar.print_orderbook('BTC/USDT')
# print('hi')
print(len('2020-01-13'))
calc = calculator.calculator()
calc.write_data('BTC/USDT')
print("->",calc.timeMe('2020-01-14T02:51:44'))
calc.usd_to_btc(50)
