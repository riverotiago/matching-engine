from typing import Optional, Any, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from order import Order, OrderSide, OrderType
from orderbook import IOrderBook, OrderBook
from matching_engine import MatchingEngine
from trade import Trade


buyBook = OrderBook()
sellBook = OrderBook()

MatchingEngine(buyBook, sellBook).order(
    Order(id=1, type=OrderType.LIMIT, side=OrderSide.BUY, price=10, qty=10))
MatchingEngine(buyBook, sellBook).order(
    Order(id=1, type=OrderType.LIMIT, side=OrderSide.BUY, price=10, qty=10))
MatchingEngine(buyBook, sellBook).order(
    Order(id=1, type=OrderType.LIMIT, side=OrderSide.SELL, price=5, qty=20))

print("BUY", buyBook)
print("SELL", sellBook)
