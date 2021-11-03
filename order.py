from datetime import datetime
from typing import Optional, Any, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime as dt


class OrderType(Enum):
    LIMIT = 0
    MARKET = 1


class OrderSide(Enum):
    BUY = 0
    SELL = 1


@dataclass
class Order:
    type: OrderType
    side: OrderSide
    price: float
    qty: float
