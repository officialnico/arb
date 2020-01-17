# Arbitrage opportinity seeker and performer

## The purpose of this project is to create a bot that identifies and profits off of arbitrage opportunities in the voatile crypto markets. The project will have the following phases:

**Phase 1:**
Identification of opportunities.

The program is run every few seconds and detects profitable price differences on two crypto markets. Once the price difference is identified, the program logs the event in a .xlsx file. Costs associated with transactions NEED TO BE CONSIDERED! These include trading, deposit and withdrawal fees.

**Phase 2:**
Micro trading

The program is able to execute identified oppertunities on the markets. Initially this will be done through small trades of values like _10USD_. Hopefully at this stage it will start generating profit.

**Phase 3**
To be determined...

## Exchanges
Initially, opportunities will be identified on **Kraken** and **Binance**.

## Update: Boxes
A box will be our little bot objects that will be fetching and analyzing, then returning a report to the transaction handler that will be used in decision making


Setting up the box:

`import Box`

`box = Box.Box()`

`box = Box.Box(enable_limit = False, usd_limit =  5, reverse = False, depth = 100, symbol = "BTC/USDT", enable_recursion= False))`

if you set recursion to true in the setup `box.run()` will start a recursive loop, printing the report every 6 seconds



