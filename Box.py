import calculator
import time
import ccxt

class Box:
    #a node that can be imlanted on any computer, for each node on every computer you can divide the time of sample by using different IP's

    def __init__(self, enable_limit = False, usd_limit =  5, reverse = False, depth = 100, symbol = "BTC/USDT", enable_recursion= False):
        self.usd_limit = usd_limit
        self.enable_limit = enable_limit
        self.reverse = reverse
        self.depth = depth
        self.symbol = symbol
        self.inOrder = False
        self.enable_recursion = enable_recursion

        if(reverse):
            self.A = ccxt.kraken({
                                            'enableRateLimit': True  # this option enables the built-in rate limiter (no ip ban)
                                            })
            self.B = ccxt.binance({
                                            'enableRateLimit': True  # this option enables the built-in rate limiter (no ip ban)
                                            })
        else:
            self.A = ccxt.binance({
                                            'enableRateLimit': True  # this option enables the built-in rate limiter (no ip ban)
                                            })
            self.B = ccxt.kraken({
                                            'enableRateLimit': True  # this option enables the built-in rate limiter (no ip ban)
                                            })

    def run(self):
        
        #while(self.inOrder==False):
        bookA = self.A.fetch_order_book(self.symbol, self.depth)
        bookB = self.B.fetch_order_book(self.symbol, self.depth)

        asks = bookA["asks"]
        bids = bookB["bids"]

        results = calc.analyze(asks, bids)

        print(results)

        if(self.enable_recursion):
            time.sleep(6)
            self.run()

    def get_inOrder(self):
        return self.get_inOrder

    def set_inOrder(self, bool):
        self.inOrder = bool


calc = calculator.calculator()
