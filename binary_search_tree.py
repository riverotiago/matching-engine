from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional
from order import Order, OrderSide, OrderType


@dataclass
class Node:
    key: Any
    content: List[Any] = field(default_factory=list)
    parent: Optional['Node'] = None
    left: Optional['Node'] = None
    right: Optional['Node'] = None


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
        else:
            raise Exception('Invalid node')

    def traverse(self, node: Optional[Node]):
        if node:
            self.traverse(node.left)
            print(node.key)
            self.traverse(node.right)

    def getMin(self, node: Node, limit: Any = float('-inf')) -> Node:
        while node.left != None and node.left.key[0] <= limit:
            node = node.left
        return node

    def getMax(self, node: Node, limit: Any = float('inf')) -> Node:
        while node.right != None and node.right.key[0] >= limit:
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
