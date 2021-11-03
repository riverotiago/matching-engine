from typing import Optional, Any, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from avl_tree import AVLNode, AVLTree
from order import Order, OrderSide, OrderType
from collections import deque

class IOrderBook(ABC):
    @abstractmethod
    def add(self, order: Order):
        pass

    @abstractmethod
    def remove(self, order: Order):
        pass

    @abstractmethod
    def iterFromMin(self, minPrice: float) -> Optional[List[Order]]:
        pass

    @abstractmethod
    def iterFromMax(self, maxPrice: float) -> Optional[List[Order]]:
        pass


class OrderBook(IOrderBook):
    def __init__(self):
        # Implementação de fila de prioridade com árvore AVL
        # Cada nó da árvore, ordenada por preço, é uma fila de ordens, por tempo de chegada
        self.orders = AVLTree()

    def add(self, order: Order):
        """ Adiciona ordem ao livro. """
        price_node = self.orders.get(key=order.price)
        order_queue = deque(order)

        if price_node:
            # Se já existe uma ordem com o mesmo preço, adiciona ordem ao final da fila
            order_queue = price_node.data
            order_queue.appendleft(order)
        else:
            # Se não existe ordem com o mesmo preço, cria uma fila de ordens
            price_node = AVLNode(key=order.price, data=order_queue)
            self.orders.insert(price_node)

    def _pop(self, order_queue: deque) -> Optional[Order]:
        """ Remove a ordem de primeira chegada. """
        order = order_queue.popleft()
        return order

    def _peek(self, order_queue: deque) -> Optional[Order]:
        """ Retorna ordem de primeira chegada. """
        order = order_queue.popleft()
        order_queue.appendleft(order)
        return order

    def getQueue(self, price: float) -> deque:
        """ Retorna fila de ordens. """
        price_node = self.orders.get(key=price)
        if price_node == None:
            return None
        return price_node.data

    def iterFromMax(self, minPrice: float = 0) -> Optional[Order]:
        """ Itera as ordens do livro a partir do máximo até o mínimo preço. """
        node = self.orders.getMax(self.orders.root)
        while node != None:
            if node.key > minPrice:
                for order in node.data:
                    yield order
            node = self.orders.getPredecessor(node)

    def iterFromMin(self, maxPrice: float = 0) -> Optional[Order]:
        """ Itera as ordens do livro a partir do mínimo até o máximo preço. """
        node = self.orders.getMin(self.orders.root)
        while node != None:
            if node.key < maxPrice:
                for order in node.data:
                    yield order
            node = self.orders.getSuccessor(node)

    def __str__(self):
        return "\n".join(map(lambda node: str(node.key), self.orders.traverse(self.orders.root)))
