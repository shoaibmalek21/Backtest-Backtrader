from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime, timedelta
import math

import argparse
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind


class TestStrategy(bt.Strategy):
    params = (
        ('period', 20),
        ('pfast', 5),
        ('pslow', 10),
    )
    
    def log(self, txt, dt=None):
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))
    
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        sma1 = bt.ind.SMA(period=self.p.pslow, plotname='Lower Low Price')
        sma2 = bt.ind.SMA(self.datas[0].high, period=self.params.period, plotname='High')
        sma3 = bt.ind.SMA(period=self.p.pfast, plotname='Higher High Price')
        sma4 = bt.ind.SMA(self.datas[0].low, period=self.params.period, plotname='Low')
        
        self.crossover = bt.ind.CrossOver(sma1, sma2)  
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            self.order = order
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self) 

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
                # Not yet ... we MIGHT BUY if ...
                if self.dataclose[0] < self.dataclose[-1]:
                        if self.dataclose[-1] < self.dataclose[-2]:
                                self.log('Higher High Price Channel, %.2f' % self.dataclose[0])
                                self.buy()
        else:
                if len(self) >= (self.bar_executed + 5):
                        self.log('Lower Low Price Channel, %.2f' % self.dataclose[0])
                        self.sell()