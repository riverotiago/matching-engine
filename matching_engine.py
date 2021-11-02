from typing import Optional, Any, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from order import Order, OrderSide, OrderType
from orderbook import IOrderBook, OrderBook
from trade import Trade

@dataclass
class MatchingEngine:

    buyOrderBook: IOrderBook
    sellOrderBook: IOrderBook

    def _add(self, order: Order):
        if order.side == OrderSide.BUY:
            self.buyOrderBook.add(order)
        else:
            self.sellOrderBook.add(order)

    def fillLimit(self, order: Order, price: float, qty: int):
        pass

    def fillMarket(self, orderBook: IOrderBook, qty: int):
        orders = []
        for order in orderBook.getFromMin():
            if order.qty >= qty:
                orders.append(order)
            else:
                qty -= order.qty
                orders.append(order)
        return orders if orders else None

    def fill(self, orderBook: IOrderBook, price: float, qty: int, limit: bool) -> Optional[Trade]:
        """ Try to fill order price and quantity. """
        orders = self.fillMarket(orderBook, qty)

    def match(self, order: Order):
        if order.side == OrderSide.BUY:
            trade = self.fill(self.sellOrderBook, order.price,
                              order.qty, order.type == OrderType.LIMIT)
            self.exec(trade)
        else:
            trade = self.fill(self.buyOrderBook, order.price,
                              order.qty, order.type == OrderType.LIMIT)
            self.exec(trade)

    # make order
    def order(self, order: Order):
        self._add(order)
        self.match(order)

    def exec(self, trade: Trade):
        print("Trade", trade)
