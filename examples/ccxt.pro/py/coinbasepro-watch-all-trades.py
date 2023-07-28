# -*- coding: utf-8 -*-

import ccxt.pro
from asyncio import run

async def main():
    exchange = ccxt.pro.coinbasepro()
    method = 'watchTrades'
    print('CCXT Pro version', ccxt.pro.__version__)
    if not exchange.has[method]:
        raise Exception(
            f'{exchange.id} {method} is not supported or not implemented yet'
        )
    last_id = ''
    while True:
        try:
            trades = await exchange.watch_trades('BTC/USD')
            for trade in trades:
                if trade['id'] > last_id:
                    print(exchange.iso8601(exchange.milliseconds()), trade['symbol'], trade['datetime'], trade['price'], trade['amount'])
                    last_id = trade['id']

        except Exception as e:
            # stop
            await exchange.close()
            raise e
            # or retry
            # pass


run(main())
