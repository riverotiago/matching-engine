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

@dataclass
class Trade:
  ordersFilled: List[Order]
  price: float
  qty: int

@dataclass
class Node:
  key: Any 
  content: List[Any] = field(default_factory=list)
  parent: Optional['Node'] = None
  left: Optional['Node'] = None
  right: Optional['Node'] = None

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

@dataclass
class BinarySearchTree:
  root: Node = None

  def insert(self, node: Node):
    y = None
    x = self.root

    # find the parent node
    while x != None:
      y = x
      if node.key < x.key:
        x = x.left
      else:
        x = x.right
    node.parent = y

    # insert the node
    if y == None:
      self.root = node
    elif node.key < y.key:
      y.left = node
    elif node.key > y.key:
      y.right = node
    elif node.key == y.key:
      y.content += node.content

  def traverse(self, node: Node):
    if node != None:
      self.traverse(node.left)
      yield node
      self.traverse(node.right)

  def getMin(self, node: Node, limit: Any = float('-inf')) -> Node:
    while node.left != None and node.left.key <= limit:
      node = node.left
    return node

  def getMax(self, node: Node, limit: Any = float('inf')) -> Node:
    while node.right != None and node.right.key >= limit:
      node = node.right
    return node

  def getSuccessor(self, node: Node) -> Node:
    if node.right != None:
      return self.getMin(node.right)
    y = node.parent
    while y != None and node == y.right:
      node = y
      y = y.parent
    return y

  def getPredecessor(self, node: Node) -> Node:
    if node.left != None:
      return self.getMax(node.left)
    y = node.parent
    while y != None and node == y.left:
      node = y
      y = y.parent
    return y


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
      trade = self.fill(self.sellOrderBook, order.price, order.qty, order.type == OrderType.LIMIT)
      self.exec(trade)
    else:
      trade = self.fill(self.buyOrderBook, order.price, order.qty, order.type == OrderType.LIMIT)
      self.exec(trade)

  # make order
  def order(self, order: Order):
    self._add(order)
    self.match(order)

  def exec(self, trade: Trade):
    print("Trade", trade)


buyBook = OrderBook()
sellBook = OrderBook()

MatchingEngine(buyBook, sellBook).order(Order(id=1, type=OrderType.LIMIT, side=OrderSide.BUY, price=10, qty=10))
MatchingEngine(buyBook, sellBook).order(Order(id=1, type=OrderType.LIMIT, side=OrderSide.BUY, price=10, qty=10))
MatchingEngine(buyBook, sellBook).order(Order(id=1, type=OrderType.LIMIT, side=OrderSide.SELL, price=5, qty=20))

print("BUY", buyBook)
print("SELL", sellBook)
