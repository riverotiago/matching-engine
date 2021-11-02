from typing import Optional, Any, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from order import Order, OrderSide, OrderType
from orderbook import IOrderBook, OrderBook

@dataclass
class Trade:
    ordersFilled: List[Order]
    price: float
    qty: int
