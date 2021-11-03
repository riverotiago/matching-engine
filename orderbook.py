from typing import Generator, Optional, Any, List
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
    def popFirst(self, price: float):
        pass

    @abstractmethod
    def peekFirst(self, price: float):
        pass

    @abstractmethod
    def iterFromMin(self, minPrice: float) -> Optional[List[Order]]:
        pass

    @abstractmethod
    def iterFromMax(self, maxPrice: float) -> Optional[List[Order]]:
        pass
    
    @abstractmethod
    def popQty(self, price: float, qty: int) -> int:
        pass

    @abstractmethod
    def getMinPrice(self) -> Optional[float]:
        pass

    @abstractmethod
    def getMaxPrice(self) -> Optional[float]:
        pass

    @abstractmethod
    def popFirst(self) -> Optional[Order]:
        pass

    @abstractmethod
    def getSize(self) -> int:
        pass

class OrderPriorityQueue():
    def __init__(self, order: Order):
        self.limit_queue = deque()
        self.limit_queue.append(order)

    def appendleft(self , order: Order):
        self.limit_queue.appendleft(order)

    def append(self, order: Order):
        self.limit_queue.append(order)

    def popleft(self) -> Optional[Order]:
        if self.limit_queue:
            return self.limit_queue.popleft()
        else:
            return None 

    def pop(self) -> Optional[Order]:
        if self.limit_queue:
            return self.limit_queue.pop()
        else:
            return None

    def __len__(self):
        return len(self.limit_queue)

    def __iter__(self):
        for order in self.limit_queue:
            yield order


class OrderBook(IOrderBook):
    def __init__(self):
        # Implementação de fila de prioridade com árvore AVL
        # Cada nó da árvore, ordenada por preço, é uma fila de ordens, por tempo de chegada
        self.orders = AVLTree()

    def add(self, order: Order):
        """ Adiciona ordem ao livro. """
        price_node = self.orders.get(key=order.price)
        order_queue = OrderPriorityQueue(order)

        if price_node:
            # Se já existe uma ordem com o mesmo preço, adiciona ordem ao final da fila
            order_queue = price_node.data
            order_queue.append(order)
        else:
            # Se não existe ordem com o mesmo preço, cria uma fila de ordens
            price_node = AVLNode(key=order.price, data=order_queue)
            self.orders.insert(price_node)

    def remove(self, price: float):
        """ Remove ordem do livro. """
        price_node = self.orders.get(key=price)
        if price_node == None:
            return None
        self.orders.delete(price_node)

    def _pop(self, order_queue: OrderPriorityQueue) -> Optional[Order]:
        """ Remove a ordem de primeira chegada. """
        order = order_queue.popleft()
        return order

    def _peek(self, order_queue: OrderPriorityQueue) -> Optional[Order]:
        """ Retorna ordem de primeira chegada. """
        order = order_queue.popleft()
        order_queue.appendleft(order)
        return order

    def getMinPrice(self) -> Optional[float]:
        price_node = self.orders.getMin(self.orders.root)
        if price_node:
            return price_node.key
        else:
            return None

    def getMaxPrice(self) -> Optional[float]:
        price_node = self.orders.getMax(self.orders.root)
        if price_node:
            return price_node.key
        else:
            return None

    def getQueue(self, price: float) -> OrderPriorityQueue:
        """ Retorna fila de ordens. """
        price_node = self.orders.get(key=price)
        if price_node == None:
            return None
        return price_node.data

    def popQty(self, price: float, qty: int) -> int:
        """
            Remove ordens de preço definido da fila até que a quantidade seja abatida,
            ou não haja mais ordens neste preço.
            Retorna a quantidade abatida.
        """
        order_queue = self.getQueue(price)
        if order_queue == None:
            return 0

        qty_removed = 0
        while len(order_queue) > 0 and qty_removed < qty:
            order = self._peek(order_queue)
            # Se ordem tiver quantidade mais que suficiente
            if order.qty > qty - qty_removed:
                sobra = qty - qty_removed
                order.qty -= sobra
                qty_removed += sobra
            else:
                qty_removed += order.qty
                self._pop(order_queue)

        if len(order_queue) == 0:
            self.remove(price)

        return  qty_removed

    def iterFromMax(self, minPrice: float = 0) -> Optional[Order]:
        """ Itera as ordens do livro a partir do máximo até o mínimo preço. """
        node = self.orders.getMax(self.orders.root)
        while node != None:
            if node.key > minPrice:
                for order in node.data:
                    yield order
            node = self.orders.getPredecessor(node)

    def iterFromMin(self, maxPrice: float = float('inf')) -> Optional[Order]:
        """ Itera as ordens do livro a partir do mínimo até o máximo preço. """
        node = self.orders.getMin(self.orders.root)
        while node != None:
            if node.key < maxPrice:
                for order in node.data:
                    yield order
            node = self.orders.getSuccessor(node)

    def popFirst(self, price: Optional[float]):
        if price == None:
            return None
        return self._pop(self.getQueue(price))

    def peekFirst(self, price: Optional[float]):
        if price == None:
            return None
        return self._peek(self.getQueue(price))

    def getSize(self) -> int:
        """ Retorna o tamanho do livro. """
        size = 0
        for price_node in self.orders.traverse(self.orders.root):
            size += len(price_node.data)
        return size


    def __str__(self):
        return "\n".join(map(lambda node: str(node.key), self.orders.traverse(self.orders.root)))
