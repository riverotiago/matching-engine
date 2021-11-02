import unittest
from orderbook import OrderBook
from order import Order, OrderSide, OrderType
from binary_search_tree import Node
from typing import Optional

def DFS(node: Optional[Node]):
  pass


class TestOrderbook(unittest.TestCase):

  def test_orderbook(self):
    ob = OrderBook()
    ob.add(Order(0, OrderSide.BUY, OrderType.LIMIT, 100, 10))
    ob.add(Order(1, OrderSide.BUY, OrderType.LIMIT, 100, 20))
    ob.add(Order(2, OrderSide.BUY, OrderType.LIMIT, 100, 30))
    ob.add(Order(3, OrderSide.BUY, OrderType.LIMIT, 120, 30))

    ob.orders.traverse(ob.orders.root)


if __name__ == '__main__':
  unittest.main()
