import unittest
from matching_engine import MatchingEngine
from orderbook import OrderBook
from order import Order, OrderSide, OrderType
from trade import Trade
import math


class TestMatchingEngine(unittest.TestCase):

    def setUp(self) -> None:
        self.sellBook = OrderBook()
        self.buyBook = OrderBook()
        self.engine = MatchingEngine(self.buyBook, self.sellBook)

    def test_order(self):
        o1 = Order(type=OrderType.LIMIT, side=OrderSide.BUY, price=100, qty=10)
        o2 = Order(type=OrderType.LIMIT, side=OrderSide.SELL, price=100, qty=10)
        self.engine.order(o1)
        self.engine.order(o2)
        expected_o1 = self.buyBook.popFirst(self.buyBook.getMaxPrice())
        expected_o2 = self.sellBook.popFirst(self.sellBook.getMinPrice())
        self.assertEqual(expected_o1, o1, "Inserção não é feita corretamente")
        self.assertEqual(expected_o2, o2, "Inserção não é feita corretamente")


    def test_match_with_multiple_trades(self):
        o1 = Order(type=OrderType.MARKET, side=OrderSide.BUY, qty=10)
        o2 = Order(type=OrderType.LIMIT, side=OrderSide.SELL, price=100, qty=5)
        o3 = Order(type=OrderType.LIMIT, side=OrderSide.SELL, price=100, qty=5)
        self.engine.order(o2)
        self.engine.order(o3)
        self.engine.order(o1)

        expectedTradeList = [Trade(price=100, qty=10)]
        self.assertEqual(self.engine.previousTrades, expectedTradeList, "Order MARKET não é preenchida assim que possível.")

    def test_match_partial_fill(self):
        o1 = Order(type=OrderType.MARKET, side=OrderSide.BUY, price=math.inf, qty=10)
        o2 = Order(type=OrderType.LIMIT, side=OrderSide.SELL, price=100, qty=5)
        self.engine.order(o2)
        self.engine.order(o1)

        expectedTradeList = [Trade(price=100, qty=5)]
        self.assertEqual(self.engine.previousTrades, expectedTradeList, "Ordens não são completadas parcialmente.")

    def test_exemplo(self):
        orders = [
            Order(type=OrderType.LIMIT, side=OrderSide.BUY, price=10, qty=100),
            Order(type=OrderType.LIMIT, side=OrderSide.SELL, price=20, qty=100),
            Order(type=OrderType.LIMIT, side=OrderSide.SELL, price=20, qty=200),
            Order(type=OrderType.MARKET, side=OrderSide.BUY, qty=150),
            Order(type=OrderType.MARKET, side=OrderSide.BUY, qty=200),
            Order(type=OrderType.MARKET, side=OrderSide.SELL, price=0, qty=200),
        ]
        for o in orders:
            self.engine.order(o)

        expectedTradeList = [
            Trade(price=20, qty=150),   
            Trade(price=20, qty=150),   
            Trade(price=10, qty=100),   
        ]
        self.assertEqual(self.engine.previousTrades, expectedTradeList, "Ordens não são completadas parcialmente.")


if __name__ == '__main__':
    unittest.main()
