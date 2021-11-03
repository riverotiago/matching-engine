from typing import Optional, Any, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from order import Order, OrderSide, OrderType
from orderbook import IOrderBook, OrderBook
from trade import Trade
import math

@dataclass
class MatchingEngine:

    buyOrderBook: IOrderBook
    sellOrderBook: IOrderBook
    previousTrades: List[Trade] = field(default_factory=list)

    def _add(self, order: Order):
        if order.side == OrderSide.BUY:
            self.buyOrderBook.add(order)
        else:
            self.sellOrderBook.add(order)


    def _fillBuyOrder(self, order: Order):
        """
            Tenta completar a ordem até não haver mais ordens no livro,
            ou ultrapassar o valor limite (se for um limit order).
        """
        # Acha a ordem de venda com menor valor
        minPrice = self.sellOrderBook.getMinPrice()
        qty = order.qty

        # Enquanto houver ordens disponíveis dentro do melhor preço 
        # e a quantidade de ordens não for atingida, executar a compra
        filled = self.sellOrderBook.popQty(minPrice, qty)

        # Se não foi possível completar a ordem, sai do loop
        if filled > 0:
            self.exec(Trade(price=minPrice, qty=filled))


    def _fillSellOrder(self, order: Order):
        """
            Tenta completar a ordem até não haver mais ordens no livro,
            ou ultrapassar o valor limite (se for um limit order).
        """
        # Acha a ordem de compra com maior valor
        maxPrice = self.buyOrderBook.getMaxPrice()
        qty = order.qty


        # Enquanto houver ordens disponíveis dentro do preço máximo
        # e a quantidade de ordens não for atingida, executar a compra
        filled = self.buyOrderBook.popQty(maxPrice, qty)

        if filled > 0:
            self.exec(Trade(price=maxPrice, qty=filled))


    def match(self, order: Order):
        """
            Acha um match para a ordem de mercado.
        """
        if order.side == OrderSide.BUY:
            self._fillBuyOrder(order)
        else:
            self._fillSellOrder(order)

    def order(self, order: Order):
        if order.type == OrderType.MARKET:
            self.match(order)
        else:
            self._add(order)

    def exec(self, trade: Trade):
        self.previousTrades.append(trade)
        print(f"Trade, price: {trade.price}, qty: {trade.qty}")
