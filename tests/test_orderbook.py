import unittest
from orderbook import OrderBook
from order import Order, OrderSide, OrderType
from avl_tree import AVLTree, AVLNode
from typing import Optional

class TestOrderbook(unittest.TestCase):

    def test_add(self):
        ob = OrderBook()

        for i in range(10,14):
            ob.add(Order(OrderSide.BUY, OrderType.LIMIT, i, 10))
            ob.add(Order(OrderSide.BUY, OrderType.LIMIT, i, 20))

        print(ob)
        

    def test_remove(self):
        pass

if __name__ == '__main__':
  unittest.main()
