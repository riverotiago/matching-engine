from typing import Optional, Any, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from order import Order, OrderSide, OrderType
from binary_search_tree import BinarySearchTree, Node

class IOrderBook(ABC):

  @abstractmethod
  def add(self, order: Order):
    pass

  @abstractmethod
  def get(self, price: float) -> Node:
    pass

  @abstractmethod
  def remove(self, order: Order):
    pass

  @abstractmethod
  def getFromMin(self, minPrice: float) -> Optional[List[Order]]:
    pass

  @abstractmethod
  def getFromMax(self, maxPrice: float) -> Optional[List[Order]]:
    pass


class OrderBook(IOrderBook):
  def __init__(self):
    self.orders = BinarySearchTree()

  def add(self, order: Order):
    node = Node(key=order.price, content=[order])
    self.orders.insert(node)

  def remove(self, order: Order):
    pass

  def getFromMin(self, minPrice: float = 0) -> Optional[List[Order]]:
    node = self.orders.getMin(self.orders.root, minPrice)

    if node == None:
      return None

    while node != None:
      yield from node.content
      node = self.orders.getSuccessor(node)

  def getFromMax(self, maxPrice: float = float('inf')) -> Optional[List[Order]]:
    node = self.orders.getMax(self.orders.root, maxPrice)

    if node == None:
      return None

    while node != None:
      yield from node.content
      node = self.orders.getPredecessor(node) 

  def __str__(self):
    return "\n".join(map(lambda node: str(node.content), self.orders.traverse(self.orders.root)))