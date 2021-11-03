from typing import Optional, Any, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from order import Order, OrderSide, OrderType
from orderbook import IOrderBook, OrderBook
from matching_engine import MatchingEngine
from trade import Trade


def get_order_type(type: str) -> OrderType:
    if type == 'limit':
        return OrderType.LIMIT
    elif type == 'market':
        return OrderType.MARKET
    else:
        raise ValueError(f"Valor de tipo inválido: <{type}>")

def get_order_side(side: str) -> OrderSide:
    if side == 'buy':
        return OrderSide.BUY
    elif side == 'sell':
        return OrderSide.SELL
    else:
        raise ValueError(f"Valor de side inválido: <{side}>")

def getOrder() -> Order:
    text = input("")
    tokens = text.strip().split()

    if tokens[0] == 'limit':
        return Order(
            type=get_order_type(tokens[0]),
            side=get_order_side(tokens[1]),
            price=float(tokens[2]),
            qty=float(tokens[3])
        )
    elif tokens[0] == 'market':
        return Order(
            type=get_order_type(tokens[0]),
            side=get_order_side(tokens[1]),
            qty=float(tokens[2])
        )

def main():
    sellOrderBook = OrderBook()
    buyOrderBook = OrderBook()
    engine = MatchingEngine(buyOrderBook=buyOrderBook, sellOrderBook=sellOrderBook)

    while True:
        order = getOrder()
        engine.order(order)

if __name__ == '__main__':
    main()
