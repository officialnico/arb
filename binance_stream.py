from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from unicorn_fy.unicorn_fy import UnicornFy
import pprint
import xlsxwriter

binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
binance_websocket_api_manager.create_stream(['trade', 'kline_1m'], ['bnbbtc'])


# while True:
#     oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
#     if oldest_stream_data_from_stream_buffer:
#         #print(oldest_stream_data_from_stream_buffer)
#         unicorn_fied_stream_data = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)
#         print(unicorn_fied_stream_data)

workbook = xlsxwriter.Workbook('trades.xlsx')
worksheet = workbook.add_worksheet()

n = 0
worksheet.write(n,0,"costs")
worksheet.write(n,1,"quantity")
n+=1
while True:
    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
    if oldest_stream_data_from_stream_buffer:
        stream_data = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)
        pprint.pprint(stream_data)
        if(stream_data['event_type']=='trade'):
            print("HELO")
            worksheet.write(n,0,stream_data["price"])
            worksheet.write(n,1,stream_data["quantity"])
            n+=1
        if(n>8):
            workbook.close()
            break
