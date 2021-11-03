import unittest
from orderbook import OrderBook
from order import Order, OrderSide, OrderType
from avl_tree import AVLTree, AVLNode
from typing import Optional
import math

class TestOrderbook(unittest.TestCase):

    def test_add(self):
        ob = OrderBook()

        orders = [
            Order(OrderSide.BUY, OrderType.LIMIT, 50, 10),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 10),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 20)
        ]
        for order in orders:
            ob.add(order)

        prices = [node.key for node in ob.orders.traverse(ob.orders.root)]
        self.assertEqual(prices, [10, 30, 50], "Adicionar ordens com o mesmo preço cria nó adicional.")


        # Checa se ordens todas as ordens adicionadas estão na lista de percorrida
        retrieved_orders = []
        for node in ob.orders.traverse(ob.orders.root):
            for order in node.data:
                retrieved_orders.append(order)

        expected_orders = [
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 10),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 50, 10),
        ]
        self.assertEqual(retrieved_orders, expected_orders, "Ordens não foram adicionadas corretamente.")


    def test_iterFromMin(self):
        ob = OrderBook()

        orders = [
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 23),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 10),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 30),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 50, 23)
        ]

        for order in orders:
            ob.add(order)

        itered_orders = [(order.price, order.qty) for order in ob.iterFromMin()]
        expected_orders = [(10, 10), (10, 30), (10, 20), (30, 20), (30, 23), (50, 23)]
        self.assertEqual(itered_orders, expected_orders, "Ordens não foram iteradas corretamente.")

    def test_iterFromMax(self):
        ob = OrderBook()

        orders = [
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 23),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 10),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 30),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 50, 23)
        ]

        for order in orders:
            ob.add(order)

        itered_orders = [(order.price, order.qty) for order in ob.iterFromMax()]
        expected_orders = [(50, 23), (30, 20), (30, 23), (10, 10), (10, 30), (10, 20)]
        self.assertEqual(itered_orders, expected_orders, "Ordens não foram iteradas corretamente.")

    def test_popFirst(self):
        ob = OrderBook()

        orders = [
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 23),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 10),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 30),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 50, 23)
        ]

        for order in orders:
            ob.add(order)

        ob.popFirst(30)

        itered_orders = [(order.price, order.qty) for order in ob.iterFromMax()]
        expected_orders = [(50, 23), (30, 23), (10, 10), (10, 30), (10, 20)]
        self.assertEqual(itered_orders, expected_orders, "Primeira ordem com preço 30 não foi deletada.")

    def test_popFirstMarket(self):
        ob = OrderBook()

        orders = [
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 23),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 10),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 30),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 50, 23),
            Order(OrderSide.BUY, OrderType.MARKET, math.inf, qty=40)
        ]

        for order in orders:
            ob.add(order)

        ob.popFirst(30)

        itered_orders = [(order.price, order.qty) for order in ob.iterFromMax()]
        expected_orders = [(math.inf, 40), (50, 23), (30, 23), (10, 10), (10, 30), (10, 20)]
        self.assertEqual(itered_orders, expected_orders, "Primeira ordem com preço 30 não foi deletada.")

    def test_popQty(self):
        ob = OrderBook()

        orders = [
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 30, 23),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 10),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 30),
            Order(OrderSide.BUY, OrderType.LIMIT, 10, 20),
            Order(OrderSide.BUY, OrderType.LIMIT, 50, 23)
        ]

        for order in orders:
            ob.add(order)

        ob.popQty(10, 60)
        itered_orders = [(order.price, order.qty) for order in ob.iterFromMin()]
        expected_orders = [(30,20), (30,23), (50,23)]
        self.assertEqual(itered_orders, expected_orders, "Preço não removido ao preencher quantidade.")

        ob.popQty(30, 40)
        itered_orders = [(order.price, order.qty) for order in ob.iterFromMin()]
        expected_orders = [(30,3), (50,23)]
        self.assertEqual(itered_orders, expected_orders, "Ordem (30,23) não teve abatimento correto da quantidade.")


if __name__ == '__main__':
  unittest.main()
