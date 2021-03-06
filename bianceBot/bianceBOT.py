# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 19:56:19 2021
@author: Oliver
"""

import websocket, json, pprint, talib, numpy
import APIkeys
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"


RSI_PERIOD = 5
RSI_OVERBOUGHT = 60
RSI_OVERSOLD = 40
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.005 #~90 SEK
ORDER_TYPE_MARKET = ''
cashwallet = 100
closes = []
in_position = False

client = Client(APIkeys.API_KEY, APIkeys.API_SECRET, tld='us')

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    global cashwallet
    try:
        print("sending order")
        order = client.create_test_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
        
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return True

    
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_position, cashwallet
    
    
    #print('received message')
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close)) #convert from string to float
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell! Sell! Sell!")
                    
                    # put binance sell logic here
                    order_succeeded = 1#order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False
                        cashwallet = cashwallet + TRADE_QUANTITY*float(close)
                        print("Total token value in wallet: ", in_position*TRADE_QUANTITY*float(close))
                        print(cashwallet)
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold! Buy! Buy! Buy!")
                    
                    # put binance buy order logic here
                    order_succeeded = 1 #order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True
                        cashwallet = cashwallet - TRADE_QUANTITY*float(close)
                        print("Total cash in wallet: ", cashwallet)
                        print("Total token value in wallet: ", in_position*TRADE_QUANTITY*float(close))

                
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
