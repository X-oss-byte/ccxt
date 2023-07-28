# -*- coding: utf-8 -*-

import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(f'{root}/python')

import ccxt  # noqa: E402


exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    # 'options': {
    #     'defaultType': 'spot', // spot, future, margin
    # },
})


exchange.load_markets ()

# exchange.verbose = True  # uncomment for debugging

symbol = 'ETH/BTC'
from_id = '0'
params = { 'fromId': from_id }
previous_from_id = from_id

all_trades = []

while True:

    print('------------------------------------------------------------------')
    print('Fetching with params', params)
    trades = exchange.fetch_my_trades(symbol, None, None, params)
    print('Fetched', len(trades), 'trades')
    if not len(trades):
        break

    # for i in range(0, len(trades)):
    #     trade = trades[i]
    #     print (i, trade['id'], trade['datetime'], trade['amount'])
    last_trade = trades[len(trades) - 1]
    if last_trade['id'] == previous_from_id:
        break
    previous_from_id = last_trade['id']
    params['fromId'] = last_trade['id']
    all_trades = all_trades + trades
print('Fetched', len(all_trades), 'trades')
for i in range(0, len(all_trades)):
    trade = all_trades[i]
    print (i, trade['id'], trade['datetime'], trade['amount'])
