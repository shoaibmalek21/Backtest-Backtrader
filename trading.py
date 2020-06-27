from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
from strategies import TestStrategy
from trading_data import df
import argparse
                
cerebro = bt.Cerebro()
cerebro.broker.setcash(100000.0)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

data = bt.feeds.PandasData(dataname=df)
cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)

cerebro.run()   

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()