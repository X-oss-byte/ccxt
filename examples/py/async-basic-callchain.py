# -*- coding: utf-8 -*-

import asyncio
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(f'{root}/python')

import ccxt.async_support as ccxt  # noqa: E402


async def run_all_exchanges(exchange_ids):
    results = {}

    symbol = 'ETH/BTC'
    for exchange_id in exchange_ids:

        exchange = getattr(ccxt, exchange_id)({
            'options': {
                'useWebapiForFetchingFees': False,
            }
        })

        print('Exchange:', exchange_id)

        print(exchange_id, 'symbols:')
        markets = await load_markets(exchange, symbol)  # ←----------- STEP 1
        print(list(markets.keys()))

        print(symbol, 'ticker:')
        ticker = await fetch_ticker(exchange, symbol)  # ←------------ STEP 2
        print(ticker)

        print(symbol, 'orderbook:')
        orderbook = await fetch_orderbook(exchange, symbol)  # ←------ STEP 3
        print(orderbook)

        await exchange.close()  # ←----------- LAST STEP GOES AFTER ALL CALLS

        results[exchange_id] = ticker

    return results


async def load_markets(exchange, symbol):
    try:
        return await exchange.load_markets()
    except ccxt.BaseError as e:
        print(type(e).__name__, e, e.args)
        raise e


async def fetch_ticker(exchange, symbol):
    try:
        return await exchange.fetch_ticker(symbol)
    except ccxt.BaseError as e:
        print(type(e).__name__, e, e.args)
        raise e


async def fetch_orderbook(exchange, symbol):
    try:
        return await exchange.fetch_order_book(symbol)
    except ccxt.BaseError as e:
        print(type(e).__name__, e, e.args)
        raise e


if __name__ == '__main__':
    exchange_ids = ['bitfinex', 'okex', 'exmo']
    exchanges = []
    results = asyncio.run(run_all_exchanges(exchange_ids))
    print(list(results.items()))
