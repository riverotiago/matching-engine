from typing import Optional, Any, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum


class OrderType(Enum):
    LIMIT = 0
    MARKET = 1


class OrderSide(Enum):
    BUY = 0
    SELL = 1


@dataclass
class Order:
    id: int
    type: OrderType
    side: OrderSide
    price: float
    qty: float
